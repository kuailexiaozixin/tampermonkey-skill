# Tampermonkey 与 ScriptCat：差异对照

> 本文件只收**已坐实**的行为差异，每条标注判据来源（scriptcat 源码符号 / 官方技能原文 /
> 类型定义注释）。写跨端兼容脚本前先读这一页；其余 API 手册按引擎归属分别放在
> `../api/`（Tampermonkey 为主）与 `../api/scriptcat-api.md`（ScriptCat 专属）。
>
> 判据仓库与许可见技能根目录 `NOTICE.md`；`@grant none` 在两端都指"关掉沙箱"，
> 未列在本页的能力默认两端行为一致。

## 1. 沙箱判定：`none` 的语义相同，"不写 @grant 行"的语义相反

- **Tampermonkey**：不写 `@grant` 行 = 无沙箱（等同 `none`，脚本直接跑在页面上下文）。
- **ScriptCat**：不写 `@grant` 行 **仍进沙箱**；只有显式 `@grant none` 才免沙箱。
  判据：scriptcat `src/app/service/content/exec_script.ts`——免沙箱分支的条件是
  `grantSet.has("none")`，无 grant 行时 `grantSet` 为空、走 `createContext()` 沙箱路径。
  官方技能 `scriptcat/skills/scriptcat-userscript` 原文同述
  （"also with no `@grant` line at all, unlike Tampermonkey"）。
- 后果：同一份"不声明 grant、直接 `window.X = ...`"的脚本，TM 下能污染页面、
  ScriptCat 下只写到沙箱 `window`，页面读不到。需要两端一致时显式写
  `@grant none`（此时两端都不进沙箱），或改用 `unsafeWindow`（见下条）。

## 2. `unsafeWindow` 的可用性

- 两端在**沙箱内**都提供 `unsafeWindow`（页面真实 window）。
- ScriptCat 在 `@grant none`（无沙箱）下**不提供** `unsafeWindow`，引用即
  `ReferenceError`（判据：官方 api.md "no `unsafeWindow`" + `create_context.ts`
  的 `context.unsafeWindow = window` 只在沙箱上下文执行）。
- TM 的 `@grant none` 下脚本本就在页面上下文，直接用 `window`，无此符号也无需。
- `@grant unsafeWindow` 在 ScriptCat 合法且无害（官方 api.md）。

## 3. `@run-at` 默认值（两端一致，但常见文档写错）

- 两端默认都是 `document-idle`：TM 判据为 `@types/tampermonkey` 的
  `GM_info.script["run-at"]` 注释 "Never null, defaults to document-idle"；
  ScriptCat 判据为 `src/app/service/service_worker/utils.ts` 的 `getRunAt()`
  缺省回退 `document_idle`。
- 取值域（ScriptCat `SUPPORTED_TAG_VALUES["run-at"]`）：
  `document-start` / `document-body` / `document-end` / `document-idle` / `context-menu`；
  未识别的值静默回退默认（官方 background.md "Only the first value counts,
  and an unknown value silently falls back to the default"）。

## 4. ScriptCat 专属（TM 没有，混用即脚本失效）

| 能力 | 判据 |
|---|---|
| `@background` 后台脚本（跑在 Offscreen 环境，非 SW，见 `NOTICE.md` 引文） | scriptcat `AGENTS.md` 架构图 + `src/app/service/sandbox/runtime.ts` |
| `@crontab` 定时脚本；**不依赖** `@background`，crontab 判定优先 | `src/pkg/utils/script.ts`（`SCRIPT_TYPE_CRONTAB` 分支在前） |
| cron `once` / `once(expr)` 扩展；失败也消耗周期 | `src/pkg/utils/cron.ts` `ONCE_MAP`、`src/app/service/sandbox/utils.ts` `isOnceRunDone` |
| `CATRetryError` 重试；`@grant none` 下该全局**不存在** | 官方 background.md "undefined under `@grant none`" |
| `@early-start` + `CAT_scriptLoaded()` | 官方 api.md；`gm_api.ts` `CAT_scriptLoaded` 返回 `loadScriptPromise` |
| `@inject-into content`（注入世界切换；`page` 为默认） | `src/app/service/content/utils.ts` `isInjectIntoContent` |
| `@storageName` 跨脚本共享存储 + `GM_addValueChangeListener` 的 `remote=true` 通道 | 官方 api.md |
| `CAT_setProxy` / `CAT_clearProxy` / `CAT_click(x,y)` / `CAT_fileStorage` / `CAT_fetchDocument` / `CAT_fetchBlob` / `CAT_createBlobUrl` / `CAT_registerMenuInput` / `CAT_userConfig` / `CAT.agent.*` | `src/types/scriptcat.d.ts`（签名以该文件为准） |
| `GM_closeNotification` / `GM_updateNotification`（Firefox 不支持 update） | 官方 api.md |
| `GM_info.scriptHandler === "ScriptCat"`、`userLanguage`、`scriptMetaStr` | 官方 api.md |
| `==UserConfig==` YAML 配置块（表单值走 `GM_getValue("group.key")`） | 官方 userconfig.md |
| `GM_download` 的 `native`/`browser` 模式差异（native 查 `@connect`，未声明的主机**问用户**而非直接拒绝） | 官方 api.md |

两端共有但取值域不同：`@run-in` 在 TM 官方文档 v5.3+ 起收录（`normal-tabs` /
`incognito-tabs`，另记 Firefox 容器写法），ScriptCat 白名单取值为
`all` / `normal-tabs` / `incognito-tabs`（判据：`SUPPORTED_TAG_VALUES["run-in"]`、
`shouldSkipPageLoadScript()`、`backgroundRunInAllowed()`）。

TM 有而 ScriptCat 白名单没有的标签：`@sandbox` 三态（raw/JavaScript/DOM，v4.18+）
与 Firefox 容器类 `@run-in container-id-*` 写法（判据：`SUPPORTED_METADATA_TAGS`
不含 `sandbox`）——见下条缺口。

## 5. 缺口与已查过的层（不得当作"不支持"的证据）

- **`@run-in container-id-N`**：`references/header/header-tags.md` 保留此写法
  （v5.3+ 起，官方文档 TOC 已确认收录该标签）；tampermonkey.net 文档页为需 JS
  渲染的 SPA，正文四层取不到，
  Wayback 存档、changelog.php、faq.php 四层都取不到该标签正文，本地亦无源码可查，
  **未能证实亦未证伪**。引用前按"未证实"处理；如需坐实，用真实 Tampermonkey
  实例装一份带该行的脚本观察（属浏览器实测，本技能未执行）。
- 本页所有引文截至 2026-11-18 的上游快照（commit 见根目录 `manifest.json`），
  上游漂移由 `scripts/sync_upstream.py --check` 发现。
