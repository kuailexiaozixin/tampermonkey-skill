---
name: tampermonkey
description: "Tampermonkey / ScriptCat 用户脚本开发全流程统一技能，覆盖：用户脚本的编写（GM_* 与 GM.* API、元数据块、TypeScript、跨浏览器兼容）、调试与测试（页面分析、校验脚本、常见坑）、优化（性能、安全）、以及自动化部署（通过 Tampermonkey MCP 直接读写浏览器脚本，免确认页安装/更新/删除）。当用户提到油猴、Tampermonkey、ScriptCat、脚本猫、用户脚本、userscript、GM API、网页自动化脚本、把网页导出为 Markdown 时使用。触发词：油猴、tampermonkey、scriptcat、脚本猫、用户脚本、userscript、GM_registerMenuCommand、GM_xmlhttpRequest、@match、网页导出。"
---

# Tampermonkey（油猴 / ScriptCat 用户脚本）开发

> 覆盖 **脚本猫/油猴脚本开发、Tampermonkey 编写调试、开发测试调试工具、MCP 自动化部署** 四类能力的完整开发流程，统一为**一个入口 + 一条完整工作流**：`需求 → 页面分析 → 编写 → 调试 → 部署 → 优化`。
>
> 所有资源文件按用途分布在工作流各步骤中，随用随取：
> - 参考文档在 `references/`（26 篇，按功能分 4 类子目录）：`api/` GM API 功能参考、`guide/` 编写指南、`quality/` 质量与调试、`deep/` 深度参考
> - 模板在 `templates/`（3 个）、工具脚本在 `scripts/`（3 个）
> - 完整示例在 `examples/`（2 个）

## 完整工作流

### 1. 需求澄清

确认目标网站、要做的功能，并判断是否需要 **ScriptCat 特有功能**（后台脚本、定时任务、Agent API、文件存储）——这些是 Tampermonkey 不兼容的能力，按需查 `references/api/scriptcat_api.md`（相关代码标注 `// ScriptCat only`）。
- 需要 ScriptCat 开发助手完整工作流（需求→页面分析→生成→调试）时，读深度参考 `references/deep/scriptcat-dev.md`（含 `==UserScript==` 模板与常见问题排查表）。

### 2. 页面分析

若用户已打开目标页，用 `scripts/analyze_page.js` 分析页面 DOM 结构（框架、选择器、动态元素、全局变量），为选择器和注入时机提供依据。

### 3. 编写脚本

**起步（选一种）**：
- 用模板骨架：`templates/basic-template.user.js`（最小骨架）、`templates/advanced-template.user.js`（含完整 GM API 与结构）、`templates/spa-compatible.user.js`（适配单页应用动态渲染）。
- 或用生成器：`bash scripts/generate-userscript.sh <name> <url>` 一键生成结构化脚本。

**写元数据块**（`==UserScript==` 头部）：
- 字段含义查 `references/guide/metadata.md`；需要精细的头部标签时查 `references/guide/header-reference.md`。
- URL 匹配（@match/@include/@exclude）语法查 `references/guide/url-matching.md`。

**选 API 风格与功能**：
- 新脚本推荐 **GM.\* Promise 异步 API**（`references/api/api-async.md`）；也可用 GM_* 同步风格（`references/api/api-sync.md`）。
- 按功能查对应 API：存储 `references/api/api-storage.md`、Cookie `references/api/api-cookies.md`、标签页 `references/api/api-tabs.md`、音频 `references/api/api-audio.md`、DOM 与 UI（unsafeWindow/GM_addStyle/GM_addElement/GM_registerMenuCommand/通知）`references/api/api-dom-ui.md`、网络请求 GM_xmlhttpRequest `references/api/http-requests.md`、拦截/修改页面请求 `references/api/web-requests.md`。
- 理解脚本运行沙箱与安全模型：`references/guide/sandbox-modes.md`。

**常用模式与进阶**：
- 可复用代码模式（等待元素、DOM 监听、页面加载检测等）查 `references/guide/patterns.md`。
- TypeScript 开发（@types/tampermonkey 配置）查 `references/guide/typescript.md`。
- 跨浏览器（Chrome/Firefox/Edge）兼容查 `references/guide/browser-compatibility.md`。
- **深度总览**：想通读完整知识体系时，`references/deep/tampermonkey-guide.md`（@grant 速查、@run-at 时机、外部 @require/@resource、交付检查清单）与 `references/deep/developer-toolkit.md`（DOM 最佳实践、等待元素/跨域/设置持久化/样式注入/SPA 检测五大模式、XHR/fetch 拦截与拖拽面板等高级技巧、调试与 Troubleshooting）。

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
- **调试清单**：安装到 Tampermonkey 后用控制台 / 断点 / Network 逐项排查，详见 `references/quality/debugging.md`。
- **常见坑对照**：易错点与排查方法查 `references/quality/common-pitfalls.md`。

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

> 连接码格式 `<base32(port-1024)><auth><echo>`；重启 MCP Server 后连接码变化，需在 Editors 重输一次。
> 深度参考：MCP 完整架构、鉴权握手协议、6 个工具入参/出参表、实践案例与常见问题（405/未连接/超时/IPv6）见 `references/deep/mcp-server.md`；官方 README（架构图、认证协议时序、curl/stdio 测试命令、Claude Code 配置）见 `references/deep/mcp-server-readme.md`。

### 6. 优化与发布

- **性能**：防抖/节流、事件委托、缓存 DOM 查询、避免同步 XHR，常用模式见 `references/guide/patterns.md`。
- **安全**：避免 eval、innerHTML 注入不可信内容；GM_xmlhttpRequest 配 @connect；不过度 `@match`，安全清单见 `references/quality/security-checklist.md`。
- **版本号**：遵循 `@version` 语义化递增（`references/guide/version-numbering.md`），供自动更新比较。
- **兼容性**：多浏览器测试要点见 `references/guide/browser-compatibility.md`。
- **参考成品**：`examples/网页导出.user.js`（Readability+Turndown 把网页导出为 Markdown/HTML 的实战成品）、`examples/youtube-timestamp-bookmarker.user.js`（YouTube 时间戳书签完整范例）。

## 编码规范要点

- **@match**：`*://*.example.com/*` 匹配所有子域；`https://example.com/path/*` 精确前缀；避免 `*://*/*`。
- **@grant 最小权限**：每个用到的 GM API 单独声明；`@grant none` 无沙箱直接访问页面变量。
- **@run-at**：`document-start` 最早（拦截/改全局）；`document-end` DOM 就绪（默认）；`document-idle` 完全加载。
- **跨域请求**：GM_xmlhttpRequest 必须配 `@connect` 允许域名。

## 相关

- 网页自动化 / 浏览器控制：`browser-automation`。
- 发布技能仓库：见 `github` 技能。
