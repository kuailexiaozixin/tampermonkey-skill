# ==UserScript== 元数据参考

元数据块是用户脚本的头部声明，定义脚本信息、匹配规则和权限。

```js
// ==UserScript==
// @key  value
// ==/UserScript==
```

### 基本信息

#### @name
脚本名称。支持国际化：`@name:zh-CN 中文名`。

#### @namespace
命名空间 URL，与 @name 组合唯一标识脚本。推荐用个人主页或项目地址。

#### @version
版本号，遵循语义化版本（如 `1.0.0`）。用于自动更新比较。

#### @description
脚本功能描述。支持国际化：`@description:zh-CN 中文描述`。

#### @author
作者名称。

#### @icon / @icon64
脚本图标 URL。@icon64 用于高分辨率显示。支持 data: URL。

#### @homepage / @homepageURL
脚本主页链接。

#### @supportURL
反馈/支持页面链接。

#### @license
开源协议（如 MIT、GPL-3.0）。

### 匹配规则

#### @match（推荐）
URL 匹配模式，决定脚本在哪些页面运行。语法：`scheme://host/path`

```js
// @match        https://example.com/*           // 精确域名
// @match        *://*.example.com/*             // 所有子域 + http/https
// @match        https://example.com/page/*      // 特定路径前缀
// @match        *://*/*                         // 所有页面（慎用）
```

- `*` 在 scheme 位置匹配 http 和 https
- `*` 在 host 位置只能作为子域通配符出现在开头（`*.example.com`）
- `*` 在 path 位置匹配任意字符
- 可声明多个 @match

#### @include
旧式匹配规则，支持通配符 `*` 和正则（`/regex/`）。建议用 @match 替代。

```js
// @include      https://example.com/*
// @include      /^https?:\/\/www\.example\.com/
```

#### @exclude
排除匹配的 URL，语法与 @include 相同。优先级高于 @match/@include。

```js
// @exclude      https://example.com/login*
```

#### @exclude-match
排除匹配的 URL，语法与 @match 相同。

### 权限声明

#### @grant
声明脚本使用的 GM API 权限。**每个 API 需单独声明。**

```js
// @grant        none                    // 不使用 GM API，在页面作用域运行
// @grant        GM_addStyle
// @grant        GM_xmlhttpRequest
// @grant        GM_setValue
// @grant        GM_getValue
// @grant        GM_notification
// @grant        GM_registerMenuCommand
// @grant        GM_setClipboard
// @grant        GM_openInTab
// @grant        GM_download
// @grant        GM_getResourceText
// @grant        GM_getResourceURL
// @grant        GM_cookie              // ScriptCat/TM 4.18+
// @grant        unsafeWindow
// @grant        window.close
// @grant        window.focus
// @grant        window.onurlchange     // TM 与 ScriptCat 都实现
```

**重要**：
- `@grant none` 不能和其他 @grant 共存
- **Tampermonkey**：写了任何 @grant 就进沙箱，需 `unsafeWindow` 访问页面全局；
  **完全不写 @grant 行时不进沙箱**（等同 none 的页面上下文，无 GM API）
- **ScriptCat**：与 TM 的关键差异——**不写 @grant 行也进沙箱**，只有显式 `@grant none`
  才免沙箱；且 `@grant none` 下 `unsafeWindow` 不可用（引用即 ReferenceError），
  GM API 仅剩 `GM_info` / `GM.info`（判据：scriptcat `src/app/service/content/exec_script.ts`
  的 grantSet 分支——只有 `none` 走免沙箱路径）

#### @connect
声明 `GM_xmlhttpRequest` / `GM.xmlHttpRequest` 允许请求的域名。

```js
// @connect      api.example.com        // 精确域名
// @connect      example.com            // 域名（含子域）
// @connect      *.example.com          // 通配符子域
// @connect      *                      // 任意域名（慎用）
// @connect      localhost
// @connect      self                   // 脚本所在域
```

未声明 @connect 时，首次请求会弹出用户确认对话框。

### 资源与依赖

#### @require
引入外部 JS 文件，在脚本执行前加载。

```js
// @require      https://cdn.jsdelivr.net/npm/jquery@3/dist/jquery.min.js
// @require      https://cdn.jsdelivr.net/npm/axios/dist/axios.min.js
```

多个 @require 按声明顺序加载。建议使用 CDN 的固定版本 URL。

#### @resource
声明外部资源文件（CSS、文本、图片等），通过 `GM_getResourceText` / `GM_getResourceURL` 使用。

```js
// @resource     myCSS https://example.com/style.css
// @resource     data  https://example.com/data.json
```

### 执行控制

#### @run-at
脚本注入时机：

| 值 | 时机 | 用途 |
|----|------|------|
| `document-start` | 页面开始加载（DOM 未构建） | 拦截请求、注入全局变量 |
| `document-end` | DOM 构建完成（≈ DOMContentLoaded） | 一般 DOM 操作 |
| `document-idle` | 页面完全加载（≈ load 事件后） | **默认值**（TM 与 ScriptCat 均如此），非紧急操作 |
| `document-body` | `<body>` 存在时 | 需要早期 body 访问 |
| `context-menu` | 用户右键菜单时执行 | TM 与 ScriptCat 均支持（SC 判据：`src/app/service/content/utils.ts` `isContextMenuScript`，且 exec 时自动补 `GM_registerMenuCommand` grant） |

默认值的两侧依据：Tampermonkey 官方类型 `@types/tampermonkey` 在 `GM_info.script["run-at"]`
注释写明 "Never null, defaults to document-idle"；ScriptCat 源码 `getRunAt()`
（`src/app/service/service_worker/utils.ts`）对未声明 / 未识别的值统一回退 `document_idle`。

#### @noframes
脚本不在 iframe 中运行。等效于脚本开头 `if (window.top !== window.self) return;`

```js
// @noframes
```

#### @run-in（ScriptCat）
限定脚本（页面脚本与后台/定时脚本均生效）运行在哪些浏览器上下文。
取值域见 `SUPPORTED_TAG_VALUES["run-in"]`：`all`（默认，不写即全部）、
`normal-tabs`、`incognito-tabs`——**没有** `content` / `page` / `background` 取值，
也没有 Firefox 容器 `container-id-N` 写法（TM 的 header-tags.md 保留了容器写法但本轮无法证实，
见 runtime/tampermonkey-vs-scriptcat.md 的缺口记录）。
判据：`src/app/service/service_worker/runtime.ts` `shouldSkipPageLoadScript()` 把值与
`incognito-tabs` / `normal-tabs` 逐字比较；`src/app/service/sandbox/utils.ts`
`backgroundRunInAllowed()` 管后台/定时脚本的同名判断。

```js
// @run-in       normal-tabs      // 只在普通窗口
// @run-in       incognito-tabs   // 只在隐身窗口
// @run-in       all              // 全部（缺省同义）
```
### 更新机制

#### @updateURL
检查更新的元数据 URL（只包含 ==UserScript== 头部的 .meta.js）。

#### @downloadURL
脚本完整下载 URL。更新时从此处下载新版本。

### ScriptCat 特有元数据

#### @background（ScriptCat only）
声明为后台脚本：在扩展的 Offscreen 沙箱里持续运行（不是页面、也没有目标页 DOM；
ScriptCat 架构注释写明 background 路径是 SW → Offscreen → Sandbox，Offscreen 是
"DOM-capable background environment"——所以不能绝对地说"没有 document"）。
无需匹配页面，浏览器开启期间常驻。

```js
// @background
```

#### @crontab（ScriptCat only）
定时执行表达式。**不需要** @background：`src/pkg/utils/script.ts` 里 `@crontab` 单独出现
即把脚本判为定时类型（crontab 优先于 background 判定）。
格式支持 5 位（推荐）与 6 位含秒（不推荐，定时不到秒级精度且费性能）：
`分 时 日 月 周` 或 `秒 分 时 日 月 周`。

```js
// @crontab      0 9 * * *        // 每天 9:00（5 位，推荐）
// @crontab      */30 * * * *     // 每 30 分钟（5 位）
// @crontab      0 0 9 * * 1-5    // 工作日 9:00:00（6 位）
```

`once` 扩展（ScriptCat only）：字段写 `once` 表示"该字段周期内至多执行一次"，
如 `* * once * *`（每天一次）、`* once(9-17) * * *`（9–17 点每小时一次）。
周期按运行开始计，失败也算已用；失败重试用 `CATRetryError`。
只写一行 `@crontab`：多行时安装校验与列表都只认第一行，任何一行解析失败会停掉全部任务。
（判据：`src/pkg/utils/cron.ts` 的 `extractCronExpr` / `ONCE_MAP`；`isOnceRunDone` 注释明确
"失败的运行也算"。）

#### @early-start（ScriptCat）
比 `document-start` 更早注入。配合 `CAT_scriptLoaded()` 使用。

```js
// @early-start
```

#### @storageName（ScriptCat）
自定义存储命名空间，允许多个脚本共享 GM_getValue/GM_setValue 的数据。

```js
// @storageName  shared-data
```
