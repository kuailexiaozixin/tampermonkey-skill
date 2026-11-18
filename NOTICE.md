# NOTICE — 上游来源、许可与归属

本技能大量内容取自第三方开源仓库。以下是逐路来源、许可状态与本次核对结果；
上游跟踪台账见 `manifest.json`，同步机制见 `scripts/sync_upstream.py`，同步历史见 `SYNCLOG.md`。

## 来源清单与许可状态（2026-11-18 实测）

| 来源 | 许可 | 本技能的用法 |
|---|---|---|
| [scriptscat/scriptcat](https://github.com/scriptscat/scriptcat) | **GPL-3.0**（仓库有 LICENSE） | 只引用符号名与行为结论（`src/pkg/utils/script_compat.ts`、`src/pkg/utils/cron.ts`、`src/app/service/content/exec_script.ts`、`src/app/service/sandbox/runtime.ts`、`src/types/scriptcat.d.ts`），不复制源码文本 |
| [scriptscat/scriptcat-skills](https://github.com/scriptscat/scriptcat-skills) | **无 LICENSE 文件** | `references/api/scriptcat-api.md`、`references/header/metadata.md` 与 `scripts/analyze_page.js` 源自该仓库的 `scriptcat-dev`；见下方"搬运面" |
| [scriptscat/tampermonkey-learn-guide](https://github.com/scriptscat/tampermonkey-learn-guide) | **无 LICENSE 文件** | `references/guide/` 整目录镜像（95 篇 + 配图），全程带来源说明 |
| [Tampermonkey/tampermonkey-mcp](https://github.com/Tampermonkey/tampermonkey-mcp) | **无 LICENSE 文件**（npm 包 `package.json` 标 MIT，仓库无 LICENSE） | `references/mcp/deployment.md` 描述该 npm 工具；工具名与版本要求按 `tampermonkey-mcp@0.0.5` 实测 |
| [@types/tampermonkey](https://www.npmjs.com/package/@types/tampermonkey) | MIT（DefinitelyTyped） | `GM_info.script["run-at"]` 的默认值注释用于判据 |
| [antfu-collective/vitesse-webext](https://github.com/antfu-collective/vitesse-webext) | MIT | `references/patterns/advanced.md` 第 12 节示例取自其 README（已注明来源） |

## 搬运面与归属方向（已证）

三处高度同源，方向为**本地 ← 上游**：

| 本地文件 | 上游文件 | 相似度 | 说明 |
|---|---|---|---|
| `scripts/analyze_page.js` | `scriptcat-skills/scriptcat-dev/scripts/analyze_page.js` | 逐字节相同 | 上游首次提交 2026-03-20（commit e73b12c9），本地于 2026-08-20 纳入（commit 6bad7dd） |
| `references/header/metadata.md` | `scriptcat-skills/scriptcat-dev/references/metadata.md` | 99.2% | 差异仅为标题层级（`##`→`###`）；上游 2026-03-20 创建，本地 2026-08-20 |
| `references/api/scriptcat-api.md` | `scriptcat-skills/scriptcat-dev/references/scriptcat_api.md` | 96% | 尾部曾残留上游 frontmatter，已于 2026-11-18 清除 |

其余 references（api/ 十篇、header/ 三篇、patterns/、runtime/、quality/、typescript.md）
在本轮全量 blob 比对中与上游**均不逐字节相同**，为独立撰写。

## 许可缺口（需要权利人决定）

1. **`scriptcat-skills` 与 `tampermonkey-learn-guide` 没有 LICENSE 文件。**
   无许可不等于可自由再分发；本技能仓库整体标注 MIT（`LICENSE`，署名 kuailexiaozixin），
   该声明覆盖不到上述搬运内容。建议三选一：向源仓库提请补 LICENSE、取得书面许可并注明、
   或把这批内容改回"索引 + 自撰摘要"形态（不复制正文）。
2. **`tampermonkey-mcp` 仓库无 LICENSE**（npm 元数据写 MIT）——引用其用法说明属描述性使用，
   但若复制其 README 正文需另行确认。
3. **guide 镜像含 402 个文件 / 25 MB**，其中 `docs/img/` 为教程截图；
   若源仓库后续补 LICENSE 或要求撤下，需同步处理。

## 上游原文引证（本次核对时实际读到的关键句）

- scriptcat 官方技能 `skills/scriptcat-userscript/SKILL.md:92`：
  > With any other grant — and also with no `@grant` line at all, unlike Tampermonkey —
  > the script is sandboxed: its `window` is not the page's.
- scriptcat 官方技能 `references/background.md:56`（once 语义）：
  > A run counts when it **starts**, so a failed run also uses up the period.
- scriptcat `src/pkg/utils/cron.ts` 源码注释：
  > 支持标准 5 位格式（分 时 日 月 周）与扩展 6 位格式（秒 分 时 日 月 周）；
  > 6 位扩展格式会使脚本每秒执行……并不推荐。
- `@types/tampermonkey`（DefinitelyTyped，5.5.0）`index.d.ts:387`：
  > Never null, defaults to document-idle

**未取得、因此不引用的说法**：Tampermonkey 官网 `documentation.php` 的正文（该页为需 JS 渲染
的 SPA，直连、Wayback 存档、changelog.php、faq.php 四层本轮都只取到目录级内容，取不到
`@run-at` / `@run-in` 的正文句子）。因此本技能关于 TM 侧默认值的判据只用
`@types/tampermonkey` 注释；"默认 `document-end`"这一说法只见于上游 scriptcat-skills 的
metadata.md（2026-03-20 版，本地已按源码判据改正），官网正文本轮**未能证实**，
未写入正文，只在 `references/runtime/tampermonkey-vs-scriptcat.md` 记为缺口。

`tampermonkey_put`/`delete` 的 `Tampermonkey 5.6+` 要求：出处是 GitHub 仓库
`Tampermonkey/tampermonkey-mcp` 的 README（commit d3e60f1b "Update version requirements
for PUT and DELETE"，2026-07-13 之后）；npm `tampermonkey-mcp@0.0.5` 包内 README **没有**
这一行（仓库已领先于 0.0.5 发布）。本地引用时按仓库 HEAD 为准。

## 引用不等同于背书

上游材料中被本技能判定为过时或不适用于 ScriptCat 的说法，已按源码改写并在此留痕；
逐条见 `SYNCLOG.md` 的"修正"行与 `references/runtime/tampermonkey-vs-scriptcat.md`。
