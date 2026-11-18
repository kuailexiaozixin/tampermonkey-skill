---
name: tampermonkey
description: "Tampermonkey / ScriptCat 用户脚本开发全流程统一技能，覆盖：用户脚本的编写（GM_* 与 GM.* API、元数据块、TypeScript、跨浏览器兼容）、调试与测试（页面分析、校验脚本、常见坑）、优化（性能、安全）、以及自动化部署（通过 Tampermonkey MCP 直接读写浏览器脚本，免确认页安装/更新/删除）。当用户提到油猴、Tampermonkey、ScriptCat、脚本猫、用户脚本、userscript、GM API、网页自动化脚本、把网页导出为 Markdown 时使用。触发词：油猴、tampermonkey、scriptcat、脚本猫、用户脚本、userscript、GM_registerMenuCommand、GM_xmlhttpRequest、@match、网页导出。"
---

# Tampermonkey（油猴 / ScriptCat 用户脚本）开发

> 覆盖 **脚本猫/油猴脚本开发、Tampermonkey 编写调试、开发测试调试工具、MCP 自动化部署** 四类能力的完整开发流程，统一为**一个入口 + 一条完整工作流**：`需求 → 页面分析 → 编写 → 调试 → 部署 → 优化`。
>
> 所有资源文件按用途分布在工作流各步骤中，随用随取：
> - 参考文档在 `references/`，按主题文件夹存放，每篇一个子主题、可精确检索：`api/` GM API、`header/` 脚本头部、`patterns/` 代码模式、`runtime/` 运行环境、`quality/` 质量调试、`mcp/` MCP 部署、`typescript.md` TypeScript
> - 模板在 `templates/`（3 个）、工具脚本在 `scripts/`（4 个：analyze_page.js / generate-userscript.sh / validate-userscript.sh / sync_upstream.py）
> - 完整示例在 `examples/`（1 个）
> - 教程全量镜像在 `references/guide/`（油猴教程学习指南 95 篇 + 配图，路由索引 `references/guide-index.md`）；TM 与 ScriptCat 的差异判据集中在
>   `references/runtime/tampermonkey-vs-scriptcat.md`——写跨端脚本前先读这一页

## 完整工作流

### 1. 需求澄清

确认目标网站、要做的功能，并判断是否需要 **ScriptCat 特有功能**（后台脚本、定时任务、Agent API、文件存储）——这些是 Tampermonkey 不兼容的能力，按需查 `references/api/scriptcat-api.md`（相关代码标注 `// ScriptCat only`）。

### 2. 页面分析

若用户已打开目标页，用 `scripts/analyze_page.js` 分析页面 DOM 结构（框架、选择器、动态元素、全局变量），为选择器和注入时机提供依据。

### 3. 编写脚本

**起步（选一种）**：
- 用模板骨架：`templates/basic-template.user.js`（最小骨架）、`templates/advanced-template.user.js`（含完整 GM API 与结构）、`templates/spa-compatible.user.js`（适配单页应用动态渲染）。
- 或用生成器：`bash scripts/generate-userscript.sh <name> <url>` 一键生成结构化脚本。

**写元数据块**（`==UserScript==` 头部）：
- 字段含义查 `references/header/metadata.md`、精细头部标签（@grant/@run-at/@require/@resource 等）查 `references/header/header-tags.md`、URL 匹配（@match/@include/@exclude）查 `references/header/url-matching.md`、版本号规则查 `references/header/versioning.md`。

**选 API 风格与功能**（`references/api/`，按需精确读取）：
- GM.\* Promise 异步风格 `api/async.md`、GM_* 同步风格 `api/sync.md`、存储 `api/storage.md`、Cookie `api/cookies.md`、标签页 `api/tabs.md`、音频 `api/audio.md`、DOM 与 UI（unsafeWindow/GM_addStyle/GM_addElement/GM_registerMenuCommand/通知）`api/dom-ui.md`、网络请求 GM_xmlhttpRequest `api/http-requests.md`、页面请求拦截 `api/web-requests.md`、ScriptCat 特有 API `api/scriptcat-api.md`。

**运行环境**（`references/runtime/`）：
- 沙箱与安全模型 `runtime/sandbox.md`、跨浏览器（Chrome/Firefox/Edge）兼容 `runtime/compatibility.md`。

**常用模式与进阶**（`references/patterns/`）：
- 可复用代码模式（等待元素、SPA 导航检测等）`patterns/common.md`、高级技巧（XHR/fetch 拦截、拖拽面板、快捷键等）`patterns/advanced.md`。
- TypeScript 开发（@types/tampermonkey 配置）查 `references/typescript.md`。

最小模板：
```javascript
// ==UserScript==
// @name         脚本名
// @namespace    https://example.com/scripts/
// @version      1.0.0
// @description  描述
// @author       作者
// @match        https://example.com/*
// @grant        none
// @run-at       document-idle
// ==/UserScript==

(function () {
    'use strict';
    // 你的代码
})();
```

### 4. 调试与测试

- **校验脚本**：`bash scripts/validate-userscript.sh 你的脚本.user.js`，检查必需元数据、@grant 声明、性能反模式、安全问题。
- **质量与调试**（`references/quality/`）：调试清单 `quality/debugging.md`、常见坑对照 `quality/pitfalls.md`、安全检查清单 `quality/security.md`。

### 5. 部署（MCP 自动安装 / 更新）

用 **Tampermonkey MCP** 直接把脚本写进浏览器 Tampermonkey（免确认页、全自动）：
```bash
# 启动 MCP Server（HTTP 模式，端口 4001）
tampermonkey-mcp --transport=http --port=4001
```
- 先 `tampermonkey_get_connection_code` 获取连接码，在 **Tampermonkey Editors** 扩展输入连接码建立 WebSocket 连接（Server 常驻则只需输一次）。
- **新建**：`tampermonkey_put`（value=脚本源码，需 Tampermonkey 5.6+）→ `Script created successfully`。
- **更新**：`tampermonkey_list` 找 path → `tampermonkey_get` 读当前内容 → `tampermonkey_patch`（path+value+lastModified 乐观锁）。
- **删除**：`tampermonkey_delete`（需 5.6+）。
- 部署后用 `tampermonkey_get` 读回校验，刷新页面验证生效。

> MCP 完整架构、鉴权握手协议、6 个工具入参/出参表、连接码管理、curl/stdio 测试命令、实践案例与常见问题，见 `references/mcp/deployment.md`。

### 6. 优化与发布

- **性能**：防抖/节流、事件委托、缓存 DOM 查询、避免同步 XHR，常用模式见 `references/patterns/common.md`。
- **安全**：避免 eval、innerHTML 注入不可信内容；GM_xmlhttpRequest 配 @connect；不过度 `@match`，安全清单见 `references/quality/security.md`。
- **版本号**：遵循 `@version` 语义化递增（`references/header/versioning.md`），供自动更新比较。
- **兼容性**：多浏览器测试要点见 `references/runtime/compatibility.md`。
- **参考成品**：`examples/网页导出.user.js`（Readability+Turndown 把网页导出为 Markdown/HTML 的实战成品）。

## 编码规范要点

- **@match**：`*://*.example.com/*` 匹配所有子域；`https://example.com/path/*` 精确前缀；避免 `*://*/*`。
- **@grant 最小权限**：每个用到的 GM API 单独声明；`@grant none` 无沙箱直接访问页面变量。
- **@run-at**：`document-start` 最早（拦截/改全局）；`document-end` DOM 就绪；`document-idle` 完全加载——**默认值是 `document-idle`**，TM 与 ScriptCat 一致（判据：TM 的 @types/tampermonkey 注释 "Never null, defaults to document-idle"，ScriptCat 的 `getRunAt()` 对缺省回退 `document_idle`）。
- **跨域请求**：GM_xmlhttpRequest 必须配 `@connect` 允许域名。

## 相关

- 网页自动化 / 浏览器控制：`browser-automation`。
- 发布技能仓库：见 `github` 技能。
