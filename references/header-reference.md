# 脚本头部与元数据参考

> ==UserScript== 元数据块、全部 @ 标签、URL 匹配（@match/@include/@exclude）、版本号规则，以及 Tampermonkey 开发总览（@grant 速查、@run-at 时机、@require/@resource、交付检查清单）。

## ==UserScript== 元数据参考

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
// @grant        window.onurlchange     // TM only
```

**重要**：
- `@grant none` 不能和其他 @grant 共存
- 声明任何 @grant 后，脚本运行在沙箱中，需 `unsafeWindow` 访问页面全局变量

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
| `document-end` | DOM 构建完成（≈ DOMContentLoaded）| **默认值**，一般操作 |
| `document-idle` | 页面完全加载（≈ load 事件后） | 非紧急操作 |
| `document-body` | `<body>` 存在时 | 需要早期 body 访问 |
| `context-menu` | 用户右键菜单时执行 | TM 特有 |

#### @noframes
脚本不在 iframe 中运行。等效于脚本开头 `if (window.top !== window.self) return;`

```js
// @noframes
```

#### @run-in（ScriptCat）
指定脚本运行的上下文。

```js
// @run-in       content          // 内容脚本（默认）
// @run-in       page             // 页面上下文（等同 @grant none 但可声明其他 grant）
// @run-in       background       // 后台 Service Worker
```

### 更新机制

#### @updateURL
检查更新的元数据 URL（只包含 ==UserScript== 头部的 .meta.js）。

#### @downloadURL
脚本完整下载 URL。更新时从此处下载新版本。

### ScriptCat 特有元数据

#### @background
声明为后台脚本，在 Service Worker 中运行，无需打开匹配页面。

```js
// @background
```

#### @crontab
定时执行表达式（需配合 @background）。格式同 cron：`秒 分 时 日 月 周`。

```js
// @crontab      0 0 9 * * *      // 每天 9:00:00
// @crontab      0 */30 * * * *   // 每 30 分钟
// @crontab      0 0 9 * * 1-5    // 工作日 9:00
```

ScriptCat 的 crontab 是 6 位（含秒），标准 cron 是 5 位。

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

---

## Tampermonkey Header Tags Reference

Complete documentation for all userscript header tags.

### Metadata Block Format

```javascript
// ==UserScript==
// @tag value
// ==/UserScript==
```

---

### Script Identity

#### @name

The script's display name. Supports internationalisation.

```javascript
// @name         My Awesome Script
// @name:de      Mein tolles Skript
// @name:fr      Mon script génial
// @name:ja      私の素晴らしいスクリプト
```

#### @namespace

Unique identifier namespace, typically a URL you control.

```javascript
// @namespace    https://yoursite.com/userscripts
```

#### @version

Script version for update checking. Must increase with each update.

```javascript
// @version      1.0.0
// @version      2.3.1-beta
// @version      2024-01-15
```

**See:** [version-numbering.md](version-numbering.md) for comparison rules.

#### @description

Brief description of what the script does. Supports i18n.

```javascript
// @description       Enhances the user interface with dark mode
// @description:de    Verbessert die Benutzeroberfläche mit Dunkelmodus
```

#### @author

The script author's name.

```javascript
// @author       John Doe
```

#### @copyright

Copyright statement shown in the script editor.

```javascript
// @copyright    2024, John Doe (https://example.com)
```

#### @homepage, @homepageURL, @website, @source

Link to the script's homepage (all are aliases).

```javascript
// @homepage     https://github.com/user/repo
// @supportURL   https://github.com/user/repo/issues
```

#### @supportURL

URL for users to report issues.

```javascript
// @supportURL   https://github.com/user/repo/issues
```

---

### Icons

#### @icon, @iconURL, @defaulticon

Script icon (low resolution).

```javascript
// @icon         https://example.com/icon.png
// @icon         data:image/png;base64,iVBORw0...
```

#### @icon64, @icon64URL

Script icon at 64x64 pixels. Used at various places in the options page.

```javascript
// @icon64       https://example.com/icon64.png
```

---

### URL Matching

#### @match

Specify pages where the script runs. Uses match patterns.

**Pattern format:** `<scheme>://<host><path>`

```javascript
// Match all pages on example.com
// @match        https://example.com/*

// Match any subdomain
// @match        https://*.example.com/*

// Match all HTTPS sites
// @match        https://*/*

// Match HTTP and HTTPS
// @match        *://example.com/*

// Match specific paths
// @match        https://example.com/page/*/details

// Multiple matches (use multiple tags)
// @match        https://example.com/*
// @match        https://other.com/*
```

**Special patterns:**
- `*` in scheme matches http or https
- `*` in host matches any subdomain
- `*` in path matches any characters

#### @include

Legacy matching with glob patterns and regex support.

```javascript
// Glob patterns
// @include      https://example.com/*
// @include      *://*.example.com/*

// Regular expression (wrapped in //)
// @include      /^https:\/\/www\.example\.com\/page\/\d+$/
```

**Note:** @include with `://` is interpreted like @match. Use @match for new scripts.

#### @exclude

Exclude URLs even if matched by @match or @include.

```javascript
// @match        https://example.com/*
// @exclude      https://example.com/admin/*
// @exclude      https://example.com/api/*
```

---

### Execution Control

#### @run-at

When to inject the script.

| Value | Description |
|-------|-------------|
| `document-start` | Inject as early as possible, before DOM |
| `document-body` | Inject when body element exists |
| `document-end` | Inject at/after DOMContentLoaded |
| `document-idle` | Inject after DOMContentLoaded (default) |
| `context-menu` | Inject when clicked in browser context menu |

```javascript
// @run-at       document-start
// @run-at       document-idle
// @run-at       context-menu
```

**Note:** With `context-menu`, @include and @exclude are ignored.

#### @run-in (v5.3+)

Control browser context (normal vs incognito tabs).

```javascript
// Only in normal tabs
// @run-in       normal-tabs

// Only in incognito/private mode
// @run-in       incognito-tabs

// Firefox containers
// @run-in       container-id-2
// @run-in       container-id-3
```

Default: Runs in all tabs if not specified.

#### @noframes

Only run on main page, not in iframes.

```javascript
// @noframes
```

---

### Permissions and Security

#### @grant

Whitelist GM_* functions and special window features.

```javascript
// GM functions
// @grant        GM_setValue
// @grant        GM_getValue
// @grant        GM_xmlhttpRequest
// @grant        GM_addStyle
// @grant        GM_notification

// Special window access
// @grant        unsafeWindow
// @grant        window.close
// @grant        window.focus
// @grant        window.onurlchange

// Disable sandbox (no GM_* except GM_info)
// @grant        none
```

#### @sandbox (v4.18+)

Control script injection context.

| Value | Behaviour |
|-------|-----------|
| `raw` | Run in page context (MAIN_WORLD) - default |
| `JavaScript` | Need unsafeWindow access, may use USERSCRIPT_WORLD |
| `DOM` | Only need DOM access, may use ISOLATED_WORLD |

```javascript
// @sandbox      JavaScript
// @sandbox      DOM
// @sandbox      raw
```

**See:** [sandbox-modes.md](sandbox-modes.md) for details.

#### @connect

Whitelist domains for GM_xmlhttpRequest.

```javascript
// @connect      api.example.com
// @connect      *.googleapis.com
// @connect      self
// @connect      localhost
// @connect      127.0.0.1
// @connect      *
```

**Best practice:** Declare known domains explicitly, add `*` to offer "allow all" option.

#### @antifeature

Disclose monetisation (required by GreasyFork).

```javascript
// @antifeature       ads         We show advertisements
// @antifeature       tracking    Analytics included
// @antifeature       miner       Uses crypto mining
// @antifeature:de    ads         Wir zeigen Werbung an
```

---

### External Resources

#### @require

Load external JavaScript before script runs.

```javascript
// External URLs
// @require      https://code.jquery.com/jquery-3.6.0.min.js
// @require      https://cdn.jsdelivr.net/npm/lodash@4.17.21/lodash.min.js

// With integrity hash (SRI)
// @require      https://code.jquery.com/jquery-3.6.0.min.js#sha256-/xUj+3OJU...

// Multiple hashes
// @require      https://example.com/lib.js#md5=abc123,sha256=def456

// Built-in vendor libraries
// @require      tampermonkey://vendor/jquery.js
// @require      tampermonkey://vendor/jszip/jszip.js
```

#### @resource

Preload resources accessible via GM_getResourceText/GM_getResourceURL.

```javascript
// @resource     myCSS    https://example.com/style.css
// @resource     myIcon   https://example.com/icon.png
// @resource     myData   https://example.com/data.json

// With integrity hash
// @resource     secure   https://example.com/file.js#sha256=abc123
```

---

### Updates

#### @updateURL

URL to check for updates (requires @version).

```javascript
// @updateURL    https://example.com/script.meta.js
```

#### @downloadURL

URL to download updates from. Use `none` to disable.

```javascript
// @downloadURL  https://example.com/script.user.js
// @downloadURL  none
```

---

### Web Request Interception

#### @webRequest

Define request interception rules (experimental, MV2 only).

```javascript
// @webRequest   {"selector": "*://ads.example.com/*", "action": "cancel"}
// @webRequest   {"selector": {"include": "*tracking*"}, "action": {"redirect": "https://example.com/blocked"}}
```

---

### Miscellaneous

#### @tag (v5.0+)

Add categorisation tags visible in script list.

```javascript
// @tag          productivity
// @tag          social-media
// @tag          utility
```

#### @unwrap

Inject script without wrapper/sandbox (for Scriptlets).

```javascript
// @unwrap
```

---

### Subresource Integrity (SRI)

Ensure external resources haven't been tampered with.

**Supported hash algorithms:**
- SHA-256 (native)
- MD5 (native)
- SHA-1, SHA-384, SHA-512 (require window.crypto)

**Formats:**
- Hex: `#sha256=e3b0c44298fc1c149...`
- Base64: `#sha256-47DEQpj8HBSa+/TImW...`

```javascript
// Single hash
// @require      https://example.com/lib.js#sha256=abc123def456...

// Multiple hashes (last supported one used)
// @require      https://example.com/lib.js#md5=abc,sha256=def
```

---

## URL Matching Patterns

Complete guide to @match, @include, and @exclude patterns.

---

### @match (Recommended)

The modern, safer way to specify where scripts run.

#### Pattern Format

```
<scheme>://<host><path>
```

| Component | Description | Wildcards |
|-----------|-------------|-----------|
| `scheme` | Protocol (http, https, *) | `*` matches http or https |
| `host` | Domain name | `*` matches any subdomain |
| `path` | URL path | `*` matches any characters |

#### Common Patterns

```javascript
// Exact domain
// @match https://example.com/*

// All subdomains
// @match https://*.example.com/*

// Both HTTP and HTTPS
// @match *://example.com/*

// Specific path
// @match https://example.com/app/*

// Any page on any HTTPS site (use sparingly!)
// @match https://*/*

// Specific file
// @match https://example.com/page.html
```

#### Wildcard Rules

| Pattern | Matches | Does NOT Match |
|---------|---------|----------------|
| `https://example.com/*` | example.com/page | sub.example.com |
| `https://*.example.com/*` | sub.example.com | example.com |
| `*://example.com/*` | http://example.com, https://example.com | ftp://example.com |
| `https://example.com/app/*` | example.com/app/page | example.com/other |

#### Special Patterns

```javascript
// Match root domain AND all subdomains
// @match https://example.com/*
// @match https://*.example.com/*

// Match specific subdomains only
// @match https://www.example.com/*
// @match https://api.example.com/*

// Path with wildcard in middle
// @match https://example.com/user/*/profile
```

---

### @include (Legacy)

More flexible but less secure than @match. Supports glob patterns and regex.

#### Glob Patterns

```javascript
// Standard glob
// @include https://example.com/*

// Multiple wildcards
// @include *://*.example.com/*

// Match any TLD
// @include https://example.*/*
```

#### Regular Expressions

Wrap in forward slashes:

```javascript
// Match URLs containing "example"
// @include /example/

// Match specific pattern
// @include /^https:\/\/www\.example\.com\/page\/\d+$/

// Case-insensitive
// @include /example\.com/i
```

#### @include vs @match

| Feature | @match | @include |
|---------|--------|----------|
| Security | Stricter | More permissive |
| Regex support | No | Yes |
| TLD wildcards | No | Yes (`example.*`) |
| Recommended | Yes | Legacy |

---

### @exclude

Exclude URLs even if they match @match or @include.

```javascript
// Run on example.com except admin pages
// @match https://example.com/*
// @exclude https://example.com/admin/*
// @exclude https://example.com/api/*

// Exclude with regex
// @exclude /example\.com\/private/

// Exclude specific file
// @exclude https://example.com/login.html
```

#### Precedence

1. @exclude is checked first
2. If URL matches @exclude, script doesn't run
3. Otherwise, @match/@include is checked

---

### Common Use Cases

#### Single Website

```javascript
// All pages on example.com
// @match https://example.com/*
// @match https://www.example.com/*
```

#### Multiple Related Sites

```javascript
// Company's multiple domains
// @match https://example.com/*
// @match https://example.co.uk/*
// @match https://example.de/*
```

#### SaaS Application

```javascript
// Customer subdomains
// @match https://*.example.com/*
// @exclude https://api.example.com/*
// @exclude https://static.example.com/*
```

#### Social Media Platform

```javascript
// Multiple sections
// @match https://twitter.com/*
// @match https://x.com/*
// @match https://mobile.twitter.com/*
```

#### Development & Production

```javascript
// Both environments
// @match https://example.com/*
// @match https://staging.example.com/*
// @match http://localhost:3000/*
// @match http://127.0.0.1:3000/*
```

---

### Testing Patterns

#### Verify in Browser

1. Navigate to target page
2. Check if Tampermonkey icon shows script count
3. Click icon → see which scripts matched

#### Debug Patterns

```javascript
// Add to script to verify matching
console.log('Script matched URL:', location.href);
console.log('Host:', location.host);
console.log('Path:', location.pathname);
```

#### Pattern Tester

Test if a URL matches your pattern:

```javascript
// Manual test
const patterns = [
    'https://example.com/*',
    'https://*.example.com/*'
];

const testUrl = 'https://sub.example.com/page';

// Note: This is simplified - actual matching is more complex
patterns.forEach(pattern => {
    const regex = pattern
        .replace(/\*/g, '.*')
        .replace(/\//g, '\\/');
    const matches = new RegExp(`^${regex}$`).test(testUrl);
    console.log(`${pattern}: ${matches}`);
});
```

---

### Common Mistakes

#### Mistake 1: Missing www

```javascript
// WRONG - misses www subdomain
// @match https://example.com/*

// RIGHT - include both
// @match https://example.com/*
// @match https://www.example.com/*

// OR use subdomain wildcard (but matches ALL subdomains)
// @match https://*.example.com/*
```

#### Mistake 2: HTTP vs HTTPS

```javascript
// WRONG - only matches HTTPS
// @match https://example.com/*

// RIGHT - if site uses both
// @match *://example.com/*
```

#### Mistake 3: Trailing Slash

```javascript
// These are different!
// @match https://example.com/    // Only root page
// @match https://example.com/*   // All pages
```

#### Mistake 4: Too Broad

```javascript
// WRONG - runs on every site (security risk, performance hit)
// @match *://*/*

// RIGHT - be specific
// @match https://example.com/*
```

#### Mistake 5: Query Parameters

@match doesn't match query strings or hashes:

```javascript
// This won't match https://example.com/page?id=123
// @match https://example.com/page?*

// Use @include with regex instead
// @include /^https:\/\/example\.com\/page\?/
```

---

### URL Fragment Handling

@match ignores URL fragments (#hash):

```javascript
// @match https://example.com/*

// Matches all of these:
// https://example.com/page
// https://example.com/page#section1
// https://example.com/page#section2
```

For SPA fragment detection, use window.onurlchange:

```javascript
// @grant window.onurlchange

if (window.onurlchange === null) {
    window.addEventListener('urlchange', (info) => {
        console.log('URL changed:', info.url);
    });
}
```

---

### Performance Considerations

More @match patterns = more overhead:

```javascript
// SLOW - 100 separate patterns
// @match https://site1.com/*
// @match https://site2.com/*
// ... 98 more ...

// FASTER - use wildcards where possible
// @match https://*.example.com/*

// Or use @include with regex for complex patterns
// @include /^https:\/\/(site1|site2|site3)\.com/
```

---

## Tampermonkey Version Numbering

Rules for script version comparison and update detection.

---

### Overview

The `@version` tag determines:
- Whether updates are available
- Version comparison in the script list
- Update check eligibility (required for auto-updates)

```javascript
// @version 1.0.0
```

---

### Version Comparison Rules

Tampermonkey compares versions segment by segment. Higher = newer.

#### Basic Numeric Versions

```
1.0 < 1.1 < 1.2 < 2.0
1.9 < 1.10 < 1.11
1.0.0 < 1.0.1 < 1.1.0
```

**Note:** `1.9 < 1.10` (numeric comparison, not string)

#### Equivalent Versions

These are considered equal:

```
1 == 1. == 1.0 == 1.0.0
1.1 == 1.1.0 == 1.1.00
16.4 == 16.04
```

#### Pre-release Tags

Pre-release versions are **lower** than their release counterparts:

```
1.0-alpha < 1.0-beta < 1.0
1.0.0-alpha < 1.0.0-alpha.1 < 1.0.0
1.10.0-alpha < 1.10.0
```

#### Alpha vs Release Order

```
Alpha-v1 < Alpha-v2 < Alpha-v10 < Beta < 1.0
0.5pre3 < 0.5preliminary < 0.6pre4
```

---

### Complete Version Hierarchy

From lowest to highest:

```
Alpha-v1
Alpha-v2
Alpha-v10
Beta
0.5pre3
0.5preliminary
0.6pre4
0.6pre5
0.7pre4
0.7pre10
1.-1
1 == 1. == 1.0 == 1.0.0
1.1a
1.1aa
1.1ab
1.1b
1.1c
1.1.-1
1.1 == 1.1.0 == 1.1.00
1.1.1.1.1
1.1.1.1.2
1.1.1.1
1.10.0-alpha
1.10 == 1.10.0
1.11.0-0.3.7
1.11.0-alpha
1.11.0-alpha.1
1.11.0-alpha+1
1.12+1 == 1.12+1.0
1.12+1.1 == 1.12+1.1.0
1.12+2
1.12+2.1
1.12+3
1.12+4
1.12
2.0
16.4 == 16.04
2023-08-17.alpha
2023-08-17
2023-08-17_14-04 == 2023-08-17_14-04.0
2023-08-17+alpha
2023-09-11_14-0
```

---

### Recommended Version Formats

#### Semantic Versioning (Recommended)

```javascript
// Major.Minor.Patch
// @version 1.0.0    // Initial release
// @version 1.0.1    // Bug fix
// @version 1.1.0    // New feature
// @version 2.0.0    // Breaking change
```

#### With Pre-release Tags

```javascript
// @version 1.0.0-alpha
// @version 1.0.0-alpha.1
// @version 1.0.0-beta
// @version 1.0.0-rc.1
// @version 1.0.0
```

#### Date-Based Versions

```javascript
// @version 2024-01-15
// @version 2024-01-15.1    // Second release same day
// @version 2024-01-16
```

#### Date-Time Based

```javascript
// @version 2024-01-15_14-30
// @version 2024-01-15_16-45
```

---

### Best Practices

#### 1. Always Increment

```javascript
// WRONG - same version won't trigger update
// @version 1.0.0  →  @version 1.0.0

// CORRECT
// @version 1.0.0  →  @version 1.0.1
```

#### 2. Use Three Segments

```javascript
// GOOD - clear and standard
// @version 1.0.0

// ACCEPTABLE - but less clear
// @version 1.0
// @version 1
```

#### 3. Pre-release for Testing

```javascript
// Development versions
// @version 1.1.0-dev
// @version 1.1.0-alpha
// @version 1.1.0-beta

// Release
// @version 1.1.0
```

#### 4. Build Metadata

Use `+` for build info (doesn't affect comparison order):

```javascript
// @version 1.0.0+build.123
// @version 1.0.0+20240115
```

---

### Update Checking

#### Requirements for Auto-Update

1. **@version** must be present
2. **@updateURL** should point to a meta file
3. **@downloadURL** should point to the script file

```javascript
// @version      1.0.0
// @updateURL    https://example.com/script.meta.js
// @downloadURL  https://example.com/script.user.js
```

#### Disabling Updates

```javascript
// @downloadURL  none
```

#### Update Check Logic

1. Tampermonkey fetches the @updateURL
2. Parses the @version from the meta file
3. Compares with installed @version
4. If remote > local, downloads from @downloadURL

---

### Common Mistakes

#### 1. String vs Numeric Comparison

```javascript
// WRONG assumption: "1.9" > "1.10" (as strings)
// CORRECT: 1.9 < 1.10 (numeric comparison)
```

#### 2. Forgetting to Increment

```javascript
// Users won't get update if version stays same
// Always increment, even for small fixes
```

#### 3. Invalid Characters

```javascript
// AVOID special characters in version
// @version 1.0.0-final!     // May cause issues
// @version 1.0.0-final      // OK
```

#### 4. Skipping Versions

```javascript
// This is fine - no need for sequential versions
// @version 1.0.0  →  @version 2.0.0
```

---

### Version Display

The version appears in:
- Tampermonkey dashboard
- Script editor header
- Update notifications
- Browser extension popup

Keep it readable and meaningful for users.

---

---
name: tampermonkey
description: "Write and debug Tampermonkey userscripts for browser automation, page modification, and web enhancement. Use whenever the user mentions userscripts, Tampermonkey, Greasemonkey, Violentmonkey, or wants to write a script that runs on a website - even if they don't say 'userscript' explicitly. Also trigger for: injecting JavaScript or CSS into web pages, modifying website behaviour, hiding page elements, form auto-fill, scraping page data, intercepting requests, detecting URL changes in SPAs, adding keyboard shortcuts to websites, tab audio control, or TypeScript userscripts. Covers all header tags (@match, @grant, @require, @run-in), GM_* synchronous APIs, GM.* promise-based APIs (recommended for new scripts), batch storage (GM.getValues/setValues v5.3+), binary data support (v5.4+), TypeScript setup via @types/tampermonkey, security sandboxing, and cross-browser compatibility (Chrome, Firefox, Edge). Do NOT use for Selenium/Puppeteer automation, browser extensions (WebExtensions/MV3), or server-side scripts."
allowed-tools: Read, Glob, Grep, Write, Edit
---

## Tampermonkey Userscript Development

Expert guidance for writing Tampermonkey userscripts - browser scripts that modify web pages, automate tasks, and enhance browsing experience.

### Quick Start Template

**JavaScript (simple scripts with no GM.* APIs)**

```javascript
// ==UserScript==
// @name         My Script Name                    // <- CUSTOMISE: Unique script name
// @namespace    https://example.com/scripts/      // <- CUSTOMISE: Your unique namespace
// @version      1.0.0                             // <- INCREMENT on updates
// @description  Brief description of the script   // <- CUSTOMISE: What it does
// @author       Your Name                         // <- CUSTOMISE: Your name
// @match        https://example.com/*             // <- CUSTOMISE: Target URL pattern
// @grant        none                              // <- ADD permissions as needed
// @run-at       document-idle                     // <- ADJUST timing if needed
// ==/UserScript==

(function() {
    'use strict';
    // Your code here
})();
```

**Modern (async/await - recommended when using GM.* APIs)**

```javascript
// ==UserScript==
// @name         My Script Name
// @namespace    https://example.com/scripts/
// @version      1.0.0
// @description  Brief description of the script
// @author       Your Name
// @match        https://example.com/*
// @grant        GM.getValue
// @grant        GM.setValue
// @run-at       document-idle
// ==/UserScript==

(async () => {
    'use strict';
    // Async entry point — use await with GM.* APIs
    const setting = await GM.getValue('myKey', 'default');
    console.log('Script loaded, setting:', setting);
})();
```

**TypeScript:** Add `@types/tampermonkey` for full type safety. See [typescript.md](../guide/typescript.md).

---

### Essential Header Tags

| Tag | Required | Purpose | Example |
|-----|----------|---------|---------|
| `@name` | Yes | Script name (supports i18n with `:locale`) | `@name My Script` |
| `@namespace` | Recommended | Unique identifier namespace | `@namespace https://yoursite.com/` |
| `@version` | Yes* | Version for updates (*required for auto-update) | `@version 1.2.3` |
| `@description` | Recommended | What the script does | `@description Enhances page layout` |
| `@match` | Yes** | URLs to run on (**or @include) | `@match https://example.com/*` |
| `@grant` | Situational | API permissions (use `none` for no GM_* APIs) | `@grant GM_setValue` |
| `@run-at` | Optional | When to inject (default: `document-idle`) | `@run-at document-start` |
| `@run-in` | Optional | Limit to normal or incognito tabs, or Firefox containers (v5.3+) | `@run-in normal-tabs` |

**For complete header documentation, see:** [header-reference.md](../guide/header-reference.md)

---

### URL Matching Quick Reference

```javascript
// Exact domain                  // @match https://example.com/*
// All subdomains                // @match https://*.example.com/*
// HTTP and HTTPS                // @match *://example.com/*
// Exclude paths (with @match)   // @exclude https://example.com/admin/*
```

**For advanced patterns (regex, @include, specific paths), see:** [url-matching.md](../guide/url-matching.md)

---

### @grant Permissions Quick Reference

| You Need To... | Grant This |
|----------------|------------|
| Store persistent data | `@grant GM_setValue` + `@grant GM_getValue` |
| Make cross-origin requests | `@grant GM_xmlhttpRequest` + `@connect domain` |
| Add custom CSS | `@grant GM_addStyle` |
| Access page's window | `@grant unsafeWindow` |
| Show notifications | `@grant GM_notification` |
| Add menu commands | `@grant GM_registerMenuCommand` |
| Detect URL changes (SPA) | `@grant window.onurlchange` |
| Batch read/write settings (v5.3+) | `@grant GM.getValues` + `@grant GM.setValues` |
| Mute/unmute tab audio | `@grant GM_audio` |

```javascript
// Disable sandbox (no GM_* except GM_info)
// @grant none

// Cross-origin requests require @connect
// @grant GM_xmlhttpRequest
// @connect api.example.com
// @connect *.googleapis.com
```

**For complete permissions guide, see:** [header-reference.md](../guide/header-reference.md)

---

### @run-at Injection Timing

| Value | When Script Runs | Use Case |
|-------|------------------|----------|
| `document-start` | Before DOM exists | Block resources, modify globals early |
| `document-body` | When body exists | Early DOM manipulation |
| `document-end` | At DOMContentLoaded | Most scripts - DOM ready |
| `document-idle` | After DOMContentLoaded (default) | Safe default |
| `context-menu` | On right-click menu | User-triggered actions |

---

### Common Patterns

These patterns are used frequently. Brief summaries are below - load [patterns.md](../guide/patterns.md) for full implementations with code examples.

- **Wait for Element** - Promise-based MutationObserver that resolves when a CSS selector appears in the DOM, with configurable timeout
- **SPA URL Change Detection** - Detect navigation in single-page apps using `window.onurlchange` grant or History API interception
- **Cross-Origin Request** - Fetch data from external APIs using `GM_xmlhttpRequest` with `@connect` domain whitelisting. See also [http-requests.md](../api/http-requests.md)
- **Add Custom Styles** - Inject CSS with `GM_addStyle` to restyle pages or hide elements. See also [api-dom-ui.md](../api/api-dom-ui.md)
- **Persistent Settings** - Store user preferences with `GM_setValue`/`GM_getValue` and expose toggle via `GM_registerMenuCommand`. See also [api-storage.md](../api/api-storage.md)
- **DOM Mutation Observation** - Watch for dynamically added content with MutationObserver (debounced variant included)
- **Element Manipulation** - Inject HTML, remove/hide elements, replace text across the page
- **Keyboard Shortcuts** - Simple handlers and a shortcut manager with modifier key support
- **Data Extraction** - Extract table data to arrays/objects, collect and filter page links
- **Error Handling** - Safe wrapper for try/catch and async retry with exponential backoff
- **TypeScript Userscripts** - Type-safe scripts with `@types/tampermonkey`. See [typescript.md](../guide/typescript.md)

---

### External Resources

```javascript
// @require - Load external scripts
// @require https://code.jquery.com/jquery-3.6.0.min.js#sha256-/xUj+3OJU...
// @require tampermonkey://vendor/jquery.js         // Built-in library

// @resource - Preload and inject external CSS
// @resource myCSS https://example.com/style.css    // Then: GM_addStyle(GM_getResourceText('myCSS'))
// @grant GM_getResourceText
// @grant GM_addStyle
```

---

### TypeScript Support

Install the type definitions for full IDE autocompletion and type safety:

```bash
npm install --save-dev @types/tampermonkey
```

```typescript
// ==UserScript==
// @name         My TypeScript Script
// @match        https://example.com/*
// @grant        GM.getValue
// @grant        GM.xmlHttpRequest
// @connect      api.example.com
// ==/UserScript==

(async () => {
    'use strict';
    const value = await GM.getValue<string>('key', 'default');
    const info: Tampermonkey.ScriptInfo = GM_info;
    console.log(info.script.name, value);
})();
```

Build with a bundler (esbuild, Vite, webpack) to a single `.user.js` output file. For full project setup including tsconfig and bundler config, see [typescript.md](../guide/typescript.md).

---

### What Tampermonkey Cannot Do

Userscripts have limitations:

- **Access local files** - Cannot read/write files on your computer
- **Run before page scripts** - In isolated sandbox mode, page scripts run first
- **Access cross-origin iframes** - Browser security prevents this
- **Persist across machines** - GM storage is local to each browser
- **Bypass all CSP** - Some very strict CSP cannot be bypassed
- **Inject without permission** - Tampermonkey v5.4.1+ requires users to grant injection permission per-site or globally; scripts cannot bypass this requirement

Most limitations have **workarounds** - see [common-pitfalls.md](../quality/common-pitfalls.md).

---

### When Generating Userscripts

Always include in your response:

1. **Explanation** - What the script does (1-2 sentences)
2. **Complete userscript** - Full code with all headers in a code block
3. **Installation** - "Copy/paste into Tampermonkey dashboard" or "Save as .user.js"
4. **Customisation points** - What the user can safely modify (selectors, timeouts, etc.)
5. **Permissions used** - Which @grants and why they're needed
6. **Browser support** - If Chrome-only, Firefox-only, or universal

---

### Pre-Delivery Checklist

Before returning a userscript, verify:

#### Critical (Must Pass)

- [ ] No hardcoded API keys, tokens, or passwords
- [ ] @match is specific (not `*://*/*`)
- [ ] All external URLs use HTTPS
- [ ] User input sanitised before DOM insertion

#### Important (Should Pass)

- [ ] Wrapped in IIFE with 'use strict'
- [ ] All @grant statements are necessary
- [ ] @connect includes all external domains
- [ ] Error handling for async operations
- [ ] Null checks before DOM manipulation

#### Recommended

- [ ] @version follows semantic versioning (X.Y.Z)
- [ ] Works in both Chrome and Firefox
- [ ] Comments explain non-obvious code

**For complete security checklist, see:** [security-checklist.md](../quality/security-checklist.md)

---

### Reference Files Guide

Load these on-demand based on user needs:

| File | When to Load |
|------|--------------|
| **Core** | |
| [header-reference.md](../guide/header-reference.md) | Header syntax - all @tags with examples |
| [url-matching.md](../guide/url-matching.md) | @match, @include, @exclude patterns |
| [patterns.md](../guide/patterns.md) | Common implementation patterns with code |
| [sandbox-modes.md](../guide/sandbox-modes.md) | Security/isolation execution contexts |
| **API** | |
| [api-sync.md](../api/api-sync.md) | GM_* synchronous function reference (callback-based) |
| [api-async.md](../api/api-async.md) | GM.* promise-based API reference - prefer these for new scripts |
| [api-storage.md](../api/api-storage.md) | GM_setValue, GM_getValue, listeners |
| [http-requests.md](../api/http-requests.md) | GM_xmlhttpRequest cross-origin |
| [web-requests.md](../api/web-requests.md) | GM_webRequest interception (Firefox) |
| [api-cookies.md](../api/api-cookies.md) | GM_cookie manipulation |
| [api-dom-ui.md](../api/api-dom-ui.md) | addElement, addStyle, unsafeWindow |
| [api-tabs.md](../api/api-tabs.md) | getTab, saveTab, openInTab |
| [api-audio.md](../api/api-audio.md) | Mute/unmute tabs |
| **Quality** | |
| [common-pitfalls.md](../quality/common-pitfalls.md) | What breaks scripts and workarounds |
| [debugging.md](../quality/debugging.md) | How to debug userscripts |
| [browser-compatibility.md](../guide/browser-compatibility.md) | Chrome vs Firefox differences |
| [security-checklist.md](../quality/security-checklist.md) | Pre-delivery security validation |
| [version-numbering.md](../guide/version-numbering.md) | Version string comparison rules |
| [typescript.md](../guide/typescript.md) | TypeScript project setup with @types/tampermonkey, bundler config |
