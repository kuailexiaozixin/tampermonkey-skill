---
name: tampermonkey
description: "Tampermonkey / ScriptCat 用户脚本开发全流程统一技能，覆盖：用户脚本的编写（GM_* 与 GM.* API、元数据块、TypeScript、跨浏览器兼容）、调试与测试（页面分析、校验脚本、常见坑）、优化（性能、安全）、以及自动化部署（通过 Tampermonkey MCP 直接读写浏览器脚本，免确认页安装/更新/删除）。当用户提到油猴、Tampermonkey、ScriptCat、脚本猫、用户脚本、userscript、GM API、网页自动化脚本、把网页导出为 Markdown 时使用。触发词：油猴、tampermonkey、scriptcat、脚本猫、用户脚本、userscript、GM_registerMenuCommand、GM_xmlhttpRequest、@match、网页导出。"
---

# Tampermonkey（油猴 / ScriptCat 用户脚本）开发

> 覆盖 **脚本猫/油猴脚本开发、Tampermonkey 编写调试、开发测试调试工具、MCP 自动化部署** 四类能力的完整开发流程，统一为**一个入口 + 一条完整工作流**：`需求 → 编写 → 调试 → 部署 → 优化`。所有参考文档整合在 `references/`，模板与脚本在 `templates/`、`scripts/`。

## 资源总览

| 类型 | 内容 | 位置 |
|---|---|---|
| 示例脚本 | 网页导出（Readability+Turndown 实战成品）、YouTube 时间戳书签 | `examples/` |
| 参考 | 元数据、GM API（同步/异步/各功能域）、URL 匹配、跨浏览器、TypeScript、安全、常见坑、调试、ScriptCat 特有 API | `references/` |
| 脚本 | 页面分析（analyze_page）、脚本生成（generate-userscript）、脚本校验（validate-userscript） | `scripts/` |
| 模板 | 基础 / 高级 / SPA 兼容三种用户脚本骨架 | `templates/` |

### references/ 索引

| 参考文件 | 内容 | 何时用 |
|---|---|---|
| `metadata.md` | `==UserScript==` 元数据块字段（@name/@match/@grant/@run-at 等） | 写脚本头时 |
| `header-reference.md` | 全部头部标签的完整参考 | 需精细元数据 |
| `url-matching.md` | @match/@include/@exclude 语法 | 配 URL 时 |
| `api-sync.md` / `api-async.md` | GM_* 同步 / GM.* Promise 异步 API | 选 API 风格 |
| `api-storage.md` / `api-cookies.md` / `api-tabs.md` / `api-audio.md` | 存储 / Cookie / 标签页 / 音频 API | 对应功能 |
| `api-dom-ui.md` | unsafeWindow、GM_addStyle、GM_addElement、GM_registerMenuCommand、通知 | DOM/UI 功能 |
| `http-requests.md` / `web-requests.md` | GM_xmlhttpRequest 跨域请求 / 拦截修改页面请求 | 网络请求 |
| `scriptcat_api.md` | ScriptCat 特有：后台脚本、定时任务、Agent API、文件存储 | ScriptCat 高级功能 |
| `patterns.md` / `common-pitfalls.md` | 常用代码模式 / 易错点排查 | 编写、排错 |
| `debugging.md` / `security-checklist.md` | 调试清单 / 安全最佳实践 | 调试、审查 |
| `typescript.md` | @types/tampermonkey 配置与 TS 脚本开发 | TS 开发 |
| `browser-compatibility.md` / `version-numbering.md` / `sandbox-modes.md` | 跨浏览器 / 版本号 / 沙箱模式 | 兼容、发布 |

## 完整工作流

### 1. 需求澄清
确认目标网站、要做的功能、是否需要 ScriptCat 特有功能（后台脚本/定时任务/Agent API）。

### 2. 页面分析（可选）
用户已打开目标页时，用脚本分析 DOM 结构：
```bash
node scripts/analyze_page.js   # 或按需注入页面，获取框架/选择器/动态元素/全局变量
```

### 3. 编写脚本
- 用 `templates/` 起步（基础 / 高级 / SPA 兼容按需选择），或 `bash scripts/generate-userscript.sh <name> <url>` 生成骨架。
- 先写 `==UserScript==` 元数据块（不确定字段查 `references/metadata.md`）。
- **最小权限 `@grant`**：不需要 GM API 时用 `@grant none`（页面作用域）；声明任一 `@grant` 后运行在沙箱，需 `unsafeWindow` 访问页面变量。
- 推荐新脚本用 **GM.* Promise 异步 API**（`api-async.md`）。

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
- 校验脚本：`bash scripts/validate-userscript.sh 你的脚本.user.js`（检查必需元数据、@grant、性能反模式、安全问题）。
- 安装到 Tampermonkey 后，用控制台 / 断点 / Network 调试（详见 `references/debugging.md`）。
- 常见坑、排查对照见 `references/common-pitfalls.md`。

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

> 连接码格式 `<base32(port-1024)><auth><echo>`；重启 MCP Server 后连接码变化，需在 Editors 重输一次。详见 `references/`（MCP 工作流已并入本技能说明）。

### 6. 优化与发布
- 性能：防抖/节流、事件委托、缓存 DOM 查询、避免同步 XHR（见工作流与 `patterns.md`）。
- 安全：避免 eval、innerHTML 注入不可信内容；GM_xmlhttpRequest 配 @connect；不过度 `@match`（避免 `*://*/*`）。
- 版本号：遵循 `@version` 语义化递增（`version-numbering.md`），供自动更新比较。

## 编码规范要点

- **@match**：`*://*.example.com/*` 匹配所有子域；`https://example.com/path/*` 精确前缀；避免 `*://*/*`。
- **@grant 最小权限**：每个用到的 GM API 单独声明；`@grant none` 无沙箱直接访问页面变量。
- **@run-at**：`document-start` 最早（拦截/改全局）；`document-end` DOM 就绪（默认）；`document-idle` 完全加载。
- **跨域请求**：GM_xmlhttpRequest 必须配 `@connect` 允许域名。
- **TypeScript**：加 `@types/tampermonkey` 获得完整类型（`typescript.md`）。

## ScriptCat 特有功能（Tampermonkey 不兼容，标注 `// ScriptCat only`）

- 后台脚本、定时任务、Agent API、文件存储等，见 `references/scriptcat_api.md`。

## 相关

- 网页自动化 / 浏览器控制：`browser-automation`。
- 发布技能仓库：见 `github` 技能。
