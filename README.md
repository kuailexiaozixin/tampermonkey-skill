# tampermonkey（油猴 / ScriptCat 用户脚本开发技能）

一个统一的 **Tampermonkey / ScriptCat 用户脚本开发** Agent 技能，覆盖四个能力模块：

- **scriptcat-dev**（脚本猫/油猴脚本开发助手）
- **tampermonkey**（Tampermonkey 用户脚本编写与调试）
- **tampermonkey-developer**（开发测试调试工具包：模板、校验、拦截）
- **tampermonkey-mcp**（通过 MCP 协议直接读写浏览器 Tampermonkey，自动化部署）

四个模块串成**一条完整工作流**：`需求 → 编写 → 调试 → 部署 → 优化`。

## 目录结构

```
tampermonkey/
├── SKILL.md          # 统一技能入口（name: tampermonkey），含完整工作流
├── examples/
│   ├── 网页导出.user.js                  # 实战成品：网页导出为干净 Markdown/HTML
│   └── youtube-timestamp-bookmarker.user.js  # YouTube 时间戳书签示例
├── references/       # 26 篇参考，按功能分 4 类子目录
│   ├── api/          # GM API 功能参考（10 篇）：GM.* 异步 / GM_* 同步 / 存储 / Cookie / 标签页 / 音频 / DOM-UI / HTTP / Web 请求 / ScriptCat API
│   ├── guide/        # 编写指南（8 篇）：元数据块 / 头部标签 / URL 匹配 / 常用模式 / 沙箱 / TypeScript / 跨浏览器 / 版本号
│   ├── quality/      # 质量与调试（3 篇）：调试清单 / 常见坑 / 安全检查
│   └── deep/         # 深度参考（5 篇）：四个子技能原始完整文档（ScriptCat 助手 / Tampermonkey 指南 / 开发者工具包 / MCP Server 部署）
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
