// ==UserScript==
// @name         网页导出 (Export Page to Markdown/HTML)
// @namespace    https://wps.cn/userscripts/page-export
// @version      2.5.5
// @description  在任意页面点击 Tampermonkey 菜单，导出正文为干净 Markdown/HTML。Readability 提取正文+元数据（标题/作者/摘要/站点/时间），keepClasses 保留代码语言与数学公式，Turndown 转换。
// @author       灵犀
// @license      MIT
// @match        *://*/*
// @exclude      *://*/*.pdf
// @grant        GM_registerMenuCommand
// @run-at       document-idle
// @noframes
// @require      https://fastly.jsdelivr.net/npm/turndown/dist/turndown.js
// @require      https://fastly.jsdelivr.net/npm/turndown-plugin-gfm/dist/turndown-plugin-gfm.js
// @require      https://fastly.jsdelivr.net/npm/@mozilla/readability@latest/Readability.js
// ==/UserScript==

(function () {
    'use strict';

    const NAME = '[网页导出]';

    /* ------------------------------------------------------------------ *
     *  1. 正文提取（唯一路径）：Readability + keepClasses
     *     keepClasses 保留 code 的 language-* 与 MathJax/KaTeX class，
     *     使代码语言、数学公式、复杂表格在转换后得以保留。
     *     Readability 会删 input（任务列表），用 data-task 中转恢复。
     *     同时提取元数据（标题/作者/摘要/站点/发布时间）。
     * ------------------------------------------------------------------ */

    function getArticle() {
        try {
            const docClone = document.cloneNode(true);
            docClone.querySelectorAll('li').forEach((li) => {
                const cb = li.querySelector('input[type=checkbox]');
                if (cb) li.setAttribute('data-task', cb.checked ? 'x' : ' ');
            });
            const article = new Readability(docClone, { keepClasses: true }).parse();
            if (!article || !article.content) return null;
            const tmp = document.createElement('div');
            tmp.innerHTML = article.content;
            // 恢复任务列表 checkbox（Readability 删了 input）
            tmp.querySelectorAll('li[data-task]').forEach((li) => {
                const cb = document.createElement('input');
                cb.type = 'checkbox';
                if (li.getAttribute('data-task') === 'x') cb.checked = true;
                li.insertBefore(cb, li.firstChild);
                li.removeAttribute('data-task');
            });
            // 懒加载图片：data-src/data-original 优先覆盖占位 src
            tmp.querySelectorAll('img').forEach((img) => {
                const src = img.getAttribute('data-src') || img.getAttribute('data-original');
                if (src) img.setAttribute('src', src);
            });
            // 轻量剔除正文内残留杂质（广告/弹窗/分享等）
            tmp.querySelectorAll('script,style,iframe,form,.advertisement,.ad,.cookie-banner,.popup,.modal,.social-share,.toolbar,.breadcrumb,.pagination').forEach((el) => el.remove());
            return {
                dom: tmp,
                meta: {
                    title: article.title,
                    byline: article.byline,
                    excerpt: article.excerpt,
                    siteName: article.siteName,
                    publishedTime: article.publishedTime,
                    length: article.length
                }
            };
        } catch (e) {
            return null;
        }
    }

    /* ------------------------------------------------------------------ *
     *  2. Markdown：Turndown 成熟库 + 自定义规则
     * ------------------------------------------------------------------ */

    function toMD(clean) {
        if (!clean) return '';
        const td = new TurndownService({
            headingStyle: 'atx',
            codeBlockStyle: 'fenced',
            bulletListMarker: '-',
            emDelimiter: '*',
            strongDelimiter: '**'
        });
        if (typeof turndownPluginGfm !== 'undefined') td.use(turndownPluginGfm.gfm);
        // 表格：转义单元格/表头内的竖线（gfm 默认不转义）
        td.addRule('tableCell', {
            filter: ['th', 'td'],
            replacement: function (content, node) {
                const index = Array.prototype.indexOf.call(node.parentNode.childNodes, node);
                const esc = content.replace(/\|/g, '\\|');
                return (index === 0 ? '| ' : ' ') + esc + ' |';
            }
        });
        // 代码块语言：keepClasses 保留了 code 的 language-* class → ```lang 围栏
        td.addRule('codeBlockLang', {
            filter: function (n) { return n.nodeName === 'PRE'; },
            replacement: function (content, node) {
                const code = node.querySelector('code');
                const cls = (code && code.getAttribute('class')) || '';
                const lang = (cls.match(/language-([\w-]+)/) || [])[1] || '';
                const text = (code ? code.textContent : node.textContent).trim();
                return '```' + lang + '\n' + text + '\n```\n\n';
            }
        });
        // 链接：过滤 javascript: 伪协议
        td.addRule('linkFilter', {
            filter: function (n) { return n.nodeName === 'A'; },
            replacement: function (content, node) {
                const href = node.getAttribute('href') || '';
                if (/^\s*javascript:/i.test(href)) return content;
                return '[' + content + '](' + href + ')';
            }
        });
        // keep：数学公式（MathJax/KaTeX）与含合并单元格的复杂表格（Markdown 无法表达）
        td.keep(function (n) { return n.classList && /MathJax|katex/i.test(n.className); });
        td.keep(function (n) { return n.nodeName === 'TABLE' && n.querySelector('[colspan],[rowspan]'); });
        return td.turndown(clean);
    }

    /* ------------------------------------------------------------------ *
     *  3. 下载（纯浏览器原生 API）
     * ------------------------------------------------------------------ */

    function pageTitle() {
        return document.title || location.hostname || 'page';
    }

    function safeName(s) {
        return (s || 'page').replace(/[\\/:*?"<>|\s]+/g, '_').slice(0, 60).replace(/\.+$/, '') || 'page';
    }

    function escapeHTML(s) {
        return String(s).replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;').replace(/"/g, '&quot;');
    }

    // 保存文件：唯一路径 = 浏览器原生 a[download]（无需用户手势，Tampermonkey 菜单命令可用）。
    // 注意：showSaveFilePicker 需用户手势激活，在油猴菜单命令中不可用，故不采用。
    function downloadFile(filename, content, mime) {
        const blob = new Blob([content], { type: mime });
        const url = URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = filename;
        document.body.appendChild(a);
        a.click();
        a.remove();
        setTimeout(() => URL.revokeObjectURL(url), 5000);
        console.log(`${NAME} 已导出：${filename}`);
    }

    /* ------------------------------------------------------------------ *
     *  4. 导出（单一路径：正文 → Readability → Turndown / HTML）
     *     利用 Readability 元数据增强导出头部。
     * ------------------------------------------------------------------ */

    // 组装 Markdown 头部（标题 + 来源/作者/时间/站点元数据）
    function mdMeta(meta) {
        const lines = [];
        if (meta.byline) lines.push(`> 作者：${meta.byline}`);
        if (meta.publishedTime) lines.push(`> 时间：${meta.publishedTime}`);
        if (meta.siteName) lines.push(`> 站点：${meta.siteName}`);
        lines.push(`> 来源：${location.href}`);
        return lines.join('\n');
    }

    // 组装 HTML 头部元信息
    function htmlMeta(meta) {
        const items = [];
        if (meta.byline) items.push(`<meta name="author" content="${escapeHTML(meta.byline)}">`);
        if (meta.publishedTime) items.push(`<meta name="date" content="${escapeHTML(meta.publishedTime)}">`);
        if (meta.siteName) items.push(`<meta name="site" content="${escapeHTML(meta.siteName)}">`);
        if (meta.excerpt) items.push(`<meta name="description" content="${escapeHTML(meta.excerpt)}">`);
        return items.join('\n');
    }

    function exportMarkdown() {
        const art = getArticle();
        if (!art) {
            alert(`${NAME} 未能识别到可导出的文章正文。请打开单篇帖子/文章详情页后再导出（当前可能为列表页/首页）。`);
            return;
        }
        const title = art.meta.title || pageTitle();
        const body = toMD(art.dom).replace(/\n{3,}/g, '\n\n').trim();
        const md = `# ${title}\n\n${mdMeta(art.meta)}\n\n---\n\n${body}\n`;
        downloadFile(`${safeName(title)}.md`, md, 'text/markdown;charset=utf-8');
    }

    function exportHTML() {
        const art = getArticle();
        if (!art) {
            alert(`${NAME} 未能识别到可导出的文章正文。请打开单篇帖子/文章详情页后再导出（当前可能为列表页/首页）。`);
            return;
        }
        const title = art.meta.title || pageTitle();
        // 移除中间标记（data-task 已删；保留 class 供 MathJax/代码高亮渲染）
        const clean = art.dom;
        clean.querySelectorAll('[data-src],[onclick]').forEach((el) => {
            el.removeAttribute('data-src');
            el.removeAttribute('onclick');
        });
        const html = `<!DOCTYPE html>
<html lang="${art.meta.lang || document.documentElement.lang || 'zh-CN'}">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>${escapeHTML(title)}</title>
${htmlMeta(art.meta)}
<style>
  body { max-width: 860px; margin: 2rem auto; padding: 0 1rem; line-height: 1.7; color: #222; font-family: system-ui, -apple-system, "Segoe UI", Roboto, sans-serif; }
  img { max-width: 100%; height: auto; }
  pre { background: #f6f8fa; padding: 1em; border-radius: 6px; overflow-x: auto; white-space: pre-wrap; }
  code { background: #f6f8fa; padding: .15em .4em; border-radius: 4px; }
  pre code { background: none; padding: 0; }
  blockquote { border-left: 4px solid #ddd; margin: 0; padding-left: 1em; color: #555; }
  table { border-collapse: collapse; width: 100%; }
  th, td { border: 1px solid #ddd; padding: .4em .6em; }
  a { color: #0366d6; }
  input[type=checkbox] { margin-right: .4em; }
</style>
</head>
<body>
${clean.innerHTML}
</body>
</html>`;
        downloadFile(`${safeName(title)}.html`, html, 'text/html;charset=utf-8');
    }

    /* ------------------------------------------------------------------ *
     *  5. 入口（单一路径：正文 Markdown / 正文 HTML）
     * ------------------------------------------------------------------ */

    if (typeof GM_registerMenuCommand === 'function') {
        GM_registerMenuCommand('📄 导出正文为 Markdown', exportMarkdown);
        GM_registerMenuCommand('🌐 导出正文为 HTML', exportHTML);
    }

    console.log(`${NAME} 已加载（Readability 提取+元数据 + Turndown 转换），可通过 Tampermonkey 图标菜单导出正文。`);
})();
