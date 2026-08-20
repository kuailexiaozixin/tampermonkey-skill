# tampermonkey

统一的 **Tampermonkey / ScriptCat 用户脚本（油猴脚本）开发** Agent 技能，覆盖从编写、调试到自动化部署的完整工作流：`需求 → 页面分析 → 编写 → 调试 → 部署 → 优化`。

## 特性

- **编写**：GM_* 同步 API 与 GM.* Promise 异步 API 参考、元数据块、URL 匹配、TypeScript、跨浏览器兼容、安全沙箱、常用代码模式与高级技巧。
- **调试**：页面 DOM 分析、脚本结构校验、常见坑排查、调试清单、安全检查。
- **部署**：通过 **Tampermonkey MCP**（`tampermonkey_put`/`patch`/`delete`）全自动安装/更新/删除浏览器脚本，免确认页。
- **ScriptCat 特有**：后台脚本、定时任务（@crontab）、Agent API、文件存储。

## 目录结构

```
tampermonkey/
├── SKILL.md          # 技能入口（name: tampermonkey），含完整工作流
├── examples/
│   ├── 网页导出.user.js                  # 实战成品：把网页导出为干净 Markdown/HTML
│   └── youtube-timestamp-bookmarker.user.js  # YouTube 时间戳书签示例
├── references/       # 按主题文件夹存放，每篇一个子主题、可精确检索
│   ├── api/          # GM API 参考（10 篇）：async/sync/storage/cookies/tabs/audio/dom-ui/http-requests/web-requests/scriptcat-api
│   ├── header/       # 脚本头部（4 篇）：metadata/header-tags/url-matching/versioning
│   ├── patterns/     # 代码模式（2 篇）：common 常用模式、advanced 高级技巧与最佳实践
│   ├── runtime/      # 运行环境（2 篇）：sandbox 沙箱、compatibility 跨浏览器
│   ├── quality/      # 质量与调试（3 篇）：debugging/pitfalls/security
│   ├── mcp/          # MCP 部署（1 篇）：deployment 架构与工具
│   └── typescript.md # TypeScript 开发
├── scripts/          # analyze_page / generate-userscript / validate-userscript
└── templates/        # basic / advanced / spa-compatible 三种脚本模板
```

## 快速开始

1. 将本技能安装到 Agent（如灵犀、Claude）的技能目录，或按 `SKILL.md` 指引由 AI 驱动开发/部署用户脚本。
2. **编写**：从 `templates/` 模板起步，用 `scripts/generate-userscript.sh` 生成骨架；GM API 参考见 `references/api/`。
3. **调试**：用 `scripts/validate-userscript.sh` 校验元数据、权限声明与安全问题。
4. **部署**：启动 Tampermonkey MCP（`tampermonkey-mcp --transport=http --port=4001`），用 `tampermonkey_put`/`patch` 全自动安装/更新，详见 `references/mcp/deployment.md`。

## 相关

- [webpage-export](https://github.com/kuailexiaozixin/webpage-export)：把网页导出为 Markdown/HTML 的用户脚本仓库（本技能 `examples/网页导出.user.js` 的来源）。

## License

MIT
