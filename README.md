# tampermonkey（油猴 / ScriptCat 用户脚本开发技能）

一个统一的 **Tampermonkey / ScriptCat 用户脚本开发** Agent 技能，由原「油猴」技能的 4 个子技能合并而成：

- **scriptcat-dev**（脚本猫/油猴脚本开发助手）
- **tampermonkey**（Tampermonkey 用户脚本编写与调试）
- **tampermonkey-developer**（开发测试调试工具包：模板、校验、拦截）
- **tampermonkey-mcp**（通过 MCP 协议直接读写浏览器 Tampermonkey，自动化部署）

合并后形成**一条完整工作流**：`需求 → 编写 → 调试 → 部署 → 优化`。

## 目录结构

```
tampermonkey/
├── SKILL.md          # 统一技能入口（name: tampermonkey），含完整工作流
├── examples/
│   ├── 网页导出.user.js                  # 实战成品：网页导出为干净 Markdown/HTML
│   └── youtube-timestamp-bookmarker.user.js  # YouTube 时间戳书签示例
├── references/       # 整合的 API 与主题参考（GM API、元数据、ScriptCat、调试、安全等 22 篇）
├── scripts/          # analyze_page / generate-userscript / validate-userscript
└── templates/        # basic / advanced / spa-compatible 三种脚本模板
```

## 核心能力

- **编写**：GM_* 同步 API、GM.* Promise 异步 API、元数据块、TypeScript、跨浏览器兼容、安全沙箱。
- **调试**：页面分析、脚本校验、常见坑排查、调试清单。
- **部署**：通过 Tampermonkey MCP（`tampermonkey_put`/`patch`/`delete`）全自动安装/更新/删除浏览器脚本，免确认页。
- **ScriptCat 特有**：后台脚本、定时任务、Agent API、文件存储。

## 使用

将本技能安装到 Agent（如灵犀、Claude）的技能目录，或按 `SKILL.md` 指引由 AI 驱动开发/部署用户脚本。

## License

MIT
