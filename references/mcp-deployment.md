# Tampermonkey MCP 部署

> 通过 MCP 协议读写浏览器 Tampermonkey：架构、鉴权握手、6 个工具、连接码管理、工作流、测试命令与常见问题。

## Tampermonkey MCP（油猴脚本 MCP 管理）

基于官方 [Tampermonkey/tampermonkey-mcp](https://github.com/Tampermonkey/tampermonkey-mcp) 仓库整理，并经本机实践验证。它实现了一个 **MCP（Model Context Protocol）Server**，让 AI 助手通过 **Tampermonkey Editors** 浏览器扩展，直接对 Tampermonkey 用户脚本库做 **创建 / 列出 / 读取 / 补丁 / 删除** 操作。

> **核心价值**：用 `tampermonkey_put` 可以把脚本**直接写进 Tampermonkey 并立即生效**——完全绕开"安装确认页"，实现免人工点击、免复制的**全自动安装**。这是与手动安装（`.user.js` 导航 → 确认页点安装）相比的最大优势。

> 定位：与 `scriptcat-dev`、`tampermonkey`、`tampermonkey-developer` 三个"写脚本"技能互补——那几个负责**编写**脚本内容，本技能负责把脚本**部署/托管到浏览器 Tampermonkey**，形成"写 → 装 → 改 → 删"的闭环。

### 架构与原理

```
AI 助手 ──MCP(stdio/http)──> tampermonkey-mcp(Server)
        ──WebSocket(本地端口,由连接码推导)──> Tampermonkey Editors 扩展
        ──扩展消息──> Tampermonkey 用户脚本库
```

- Server 启动后创建一个本地 WebSocket 服务器并生成**连接码**。
- **连接码格式**：`<base32(port - 1024)><auth_token><echo_token>`——前段推导端口，后两段为鉴权令牌与回显令牌。
- 用户在 **Tampermonkey Editors** 扩展中输入连接码，扩展解析端口与令牌并建立 WebSocket 连接。
- **鉴权握手**（Editors 与 Server 之间）：`auth(token)` → Server 回 `auth(echo_token)` → 客户端回 `auth(echo_token)` → Server 返回 `authOK`；之后每 15 秒一次 ping/pong 保活。
- 连接建立后，MCP 工具 `list / get / patch / put / delete` 才可用。

### 前置条件

1. 浏览器安装 **Tampermonkey** 扩展（建议 ≥ 5.6）。
2. 浏览器安装 **Tampermonkey Editors** 扩展（Firefox / Chrome 各自版本，Chrome 版 ID：`lieodnapokbjkkdkhdljlllmgkmdokcm`）。
3. 安装 MCP Server（Node ≥ 22）：

```bash
npm install -g tampermonkey-mcp@latest
```

4. 在 AI 助手/客户端配置 MCP server（灵犀中可注册为 MCP 连接器，或用 npx 直接启动）：

```json
{
  "mcpServers": {
    "tampermonkey": {
      "command": "npx",
      "args": ["-y", "tampermonkey-mcp@latest"]
    }
  }
}
```

HTTP 传输方式（便于 curl / 脚本调用）：

```bash
tampermonkey-mcp --transport=http --port=4001
```

> 用 HTTP 模式启动后，默认监听 `localhost:4001`（IPv6 `::1`），MCP 端点为 `http://localhost:4001/mcp`。

### MCP 工具详解

> 入参/出参以实际 `inputSchema` 为准（可用 `tools/list` 查询）。

| 工具 | 用途 | 必填入参 | 可选入参 | 版本要求 | 返回 |
|------|------|----------|----------|----------|------|
| `tampermonkey_get_connection_code` | 获取连接码，**必须先调用**以启动 WebSocket | 无 | 无 | — | 连接码 |
| `tampermonkey_list` | 列出所有用户脚本 | 无 | `pattern`（按名过滤）、`includePattern`（按 URL 过滤） | — | 元数据数组（name/namespace/path/requires/storage） |
| `tampermonkey_get` | 读取某个脚本/资源内容 | `path` | `ifNotModifiedSince`（时间戳，仅变更时返回） | — | `value` 脚本内容 + `lastModified` |
| `tampermonkey_patch` | 更新已有脚本内容 | `path`、`value` | `lastModified`（乐观锁） | Editors 1.0.6+ | 成功确认或并发冲突错误 |
| `tampermonkey_put` | **创建新用户脚本** | `value`（含完整 `==UserScript==` 元数据块） | `lastModified` | **Editors 1.0.6+ 且 Tampermonkey 5.6+** | `Script created successfully` 或错误 |
| `tampermonkey_delete` | 删除用户脚本 | `path` | 无 | **Editors 1.0.6+ 且 Tampermonkey 5.6+** | 成功确认或错误 |

> ⚠️ **版本硬性要求**：`put` / `delete` 必须 **Tampermonkey 5.6+**。若 Tampermonkey 为 5.5 及以下，调用 `put` 会返回 `405 Method Not Allowed`，只能 `list / get / patch`（无法新建/删除）。此时需先升级 Tampermonkey。

### 连接码管理（重要）

- **只需输入一次**：只要 MCP Server 进程**保持常驻运行**，连接码不变，Editors 输入一次后连接长期保持，**无需每次开发都重新输入**。
- **何时需重输**：每次**重启 MCP Server** 后，鉴权令牌随机变化 → 连接码改变 → 需在 Editors 重新输入新连接码。
- **建议**：将 `tampermonkey-mcp` 配置为常驻后台服务，即可长期免重输连接码。
- 断开后调用 `tampermonkey_get_connection_code` 可获取新连接码；WebSocket 每 15 秒保活，Server 停止则连接断开。

### 工作流

#### 1. 启动 Server 并建立连接
- 启动 `tampermonkey-mcp`（stdio 或 http）。
- 调用 `tampermonkey_get_connection_code` 拿到连接码。
- 用户在 **Tampermonkey Editors** 扩展中输入连接码（一次性，Server 常驻则此后无需再输）。

#### 2. 自动安装新脚本（tampermonkey_put，免确认页）
```text
1. 准备好脚本源码（含 ==UserScript== 元数据块：@name/@namespace/@version/@match/@grant 等）
2. 调用 tampermonkey_put，入参 value = 脚本完整源码
3. 若返回 "Script created successfully" 即安装成功
4. 刷新目标页面，验证脚本已生效（如右键菜单注入、控制台日志、页面行为）
```
- **优势**：完全绕开 `.user.js` 安装确认页，无需人工点击，适合批量/自动化部署。

#### 3. 更新已有脚本（tampermonkey_patch）
```text
1. tampermonkey_list 找到目标脚本的 path
2. tampermonkey_get 读取当前内容与 lastModified（可选）
3. tampermonkey_patch，入参 path + value（新内容）+ lastModified（乐观锁防并发覆盖）
4. tampermonkey_get 读回确认内容已更新
```

#### 4. 查询 / 删除
- **查询**：`tampermonkey_list`（可带 `pattern` 过滤）→ 需要时 `tampermonkey_get` 取内容。
- **删除**：`tampermonkey_delete`，入参 `path`（需 Tampermonkey 5.6+）。

#### 5. 校验
- 安装/更新后用 `tampermonkey_get` 读回确认内容正确，再刷新目标页面验证运行效果。

### 实践案例（本机已验证）

自动安装"网页导出"用户脚本（右键将网页导出为 Markdown/HTML）：

1. Tampermonkey 升级到 **5.6.6239**（满足 `put` 版本要求）。
2. 启动 Server（http 模式，端口 4001），Editors 输入连接码建立连接。
3. 调用 `tampermonkey_put`，`value` 传入脚本完整源码 → 返回 **"Script created successfully"**。
4. 刷新测试页 → 右键出现"Tampermonkey 网页导出 / 导出为 Markdown / 导出为 HTML"菜单 → **安装+运行验证通过**。

> 对比：Tampermonkey 5.5 时调用 `put` 返回 `405 Method Not Allowed`（版本不足），只能 `list/get/patch`。

### 注意事项 / 常见问题

- **`put` 返回 405**：Tampermonkey 版本 < 5.6，需先升级。
- **"Not connected to Tampermonkey Editors"**：Editors 未连接或连接断开，需重新调用 `tampermonkey_get_connection_code` 并在 Editors 输入连接码。
- **`list` 返回 `Error: Timeout`**：WebSocket 未建立连接，Editors 尚未连上 Server。
- **Server 监听 IPv6**：http 模式默认绑 `localhost`（`::1`），用 `127.0.0.1` 可能连不上，应连 `http://localhost:4001/mcp`。
- 脚本内容必须是合法 UserScript（含 `@name`、`@namespace`、`@match` 等元数据）。
- 若需更强浏览器控制（执行 JS、操作页面），可配合 `chrome-devtools-mcp`（见仓库 README）。

### 相关

- 本技能源于官方仓库 README（`README.md`），内容经本机实践验证补充。
- 编写脚本内容：见 `scriptcat-dev`、`tampermonkey`、`tampermonkey-developer`。

---

## How to use

First install the following browser extensions:
* [Tampermonkey](https://www.tampermonkey.net/)
* Tampermonkey Editors for [Firefox](https://addons.mozilla.org/de/firefox/addon/tampermonkey-editors/) or [Chrome](https://chrome.google.com/webstore/detail/lieodnapokbjkkdkhdljlllmgkmdokcm)

Then install `tampermonkey-mcp` globally:
```bash
npm install -g tampermonkey-mcp@latest
```

Finally configure your AI assistant to use the `tampermonkey` tool:
```bash
{
  "mcpServers": {
    "tampermonkey": {
      "command": "npx",
      "args": [
        "-y",
        "tampermonkey-mcp@latest"
      ]
    }
  }
}
```
Your assistant will call `tampermonkey_get_connection_code` and return a connection code that you can enter in the Tampermonkey Editors extension.

## Claude Code configuration example
```
npm install -g claude

// either use your local checkout
npm run watch
claude mcp add --transport http --scope project tampermonkey http://localhost:4001/mcp

// or the npm package
npm install -g tampermonkey-mcp@latest
claude mcp add --transport stdio --scope project tampermonkey -- npx -y tampermonkey-mcp

// more browser control needed?
// Open chrome://inspect/#remote-debugging
// [x] Allow remote debugging for this browser instance
// or
chromium --user-data-dir=/tmp/chrome-devtools-mcp-test-profile --remote-debugging-port=9222

npm install -g chrome-devtools-mcp@latest
// install Tampermonkey and Tampermonkey Editors
claude mcp add --transport stdio --scope project chrome-devtools-mcp -- npx -y chrome-devtools-mcp@latest --slim --no-usage-statistics --auto-connect --browser-url http://127.0.0.1:9222
```

## Build

```bash
npm install
npm run all
```

## Tampermonkey MCP Server Architecture

### Overview

This project implements an MCP (Model Context Protocol) server that allows AI assistants to read and modify Tampermonkey userscripts via the Tampermonkey Editors browser extension.

### Architecture Components

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                              AI Assistant                                   │
└─────────────────────────────────────────────────────────────────────────────┘
                                   │
                                   │ MCP Protocol (stdio transport)
                                   ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│                         tampermonkey_mcp (MCP Server)                       │
│                                                                             │
│  ┌───────────────────────────────────────────────────────────────────────┐  │
│  │  server.ts                    │  Main entry point                     │  │
│  │                               │  - HTTP or stdio transport            │  │
│  │                               │  - MCP middleware                     │  │
│  └───────────────────────────────────────────────────────────────────────┘  │
│                                  │                                          │
│                                  ▼                                          │
│  ┌───────────────────────────────────────────────────────────────────────┐  │
│  │  tampermonkey.ts              │  MCP Tool Definitions                 │  │
│  │                               │  - tampermonkey_get_connection_code   │  │
│  │                               │  - tampermonkey_list                  │  │
│  │                               │  - tampermonkey_get                   │  │
│  │                               │  - tampermonkey_patch                 │  │
│  └───────────────────────────────────────────────────────────────────────┘  │
│                                  │                                          │
│                                  ▼                                          │
│  ┌───────────────────────────────────────────────────────────────────────┐  │
│  │  tampermonkey-ws-client.ts    │  WebSocket Server                     │  │
│  │                               │  - Connection code generation         │  │
│  │                               │  - Authentication handshake           │  │
│  │                               │  - Message relay to extension         │  │
│  └───────────────────────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────────────────────┘
                                   │
                                   │ WebSocket (local, port derived from code)
                                   ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│                   Tampermonkey Editors Extension                            │
│                                                                             │
│  ┌───────────────────────────────────────────────────────────────────────┐  │
│  │  Service Worker               │  Receives connection code,            │  │
│  │                               │  establishes WebSocket connection     │  │
│  └───────────────────────────────────────────────────────────────────────┘  │
│                                  │                                          │
│                                  │ Chrome Extension Messaging               │
│                                  ▼                                          │
│  ┌───────────────────────────────────────────────────────────────────────┐  │
│  │  Content Script               │  Bridges extension ↔ Tampermonkey     │  │
│  └───────────────────────────────────────────────────────────────────────┘  │
│                                  │                                          │
│                                  ▼                                          │
│  ┌───────────────────────────────────────────────────────────────────────┐  │
│  │  Tampermonkey                 │  Userscript storage & execution       │  │
│  └───────────────────────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────────────────────┘
```

### Connection Flow

1. **MCP Server starts** - Creates WebSocket server on a random available port
2. **Connection code generated** - Format: `<base32(port - 1024)><auth_token><echo_token>`
3. **User calls `tampermonkey_get_connection_code`** - Gets the connection code
4. **User enters code in Tampermonkey Editors** - Extension parses code to get port and auth
5. **Extension connects to MCP server** - WebSocket handshake with authentication
6. **MCP tools become available** - list, get, patch can now be called

### Authentication Protocol

```
Extension                              MCP Server
    │                                      │
    │───── auth (token) ──────────────────>│
    │                                      │
    │<──── auth (echo_token) ──────────────│
    │                                      │
    │───── auth (echo_token) ─────────────>│
    │                                      │
    │<──── authOK ─────────────────────────│
    │                                      │
    │<───── pings (every 15s) ─────────────│  (keep-alive)
    │───── pongs ─────────────────────────>│
    │                                      │
    │<───── commands (list/get/patch) ─────│
    │───── responses ─────────────────────>│
```

### MCP Tools

#### `tampermonkey_get_connection_code`
* **Purpose**: Initialize connection by getting the WebSocket connection code.
* **Required**: Must be called first to start the WebSocket server.
* **Output**: Connection code to enter in Tampermonkey Editors.

#### `tampermonkey_list`
* **Purpose**: List all available userscripts.
* **Input**: Optional filter by name pattern or include URL pattern.
* **Output**: Array of userscript metadata (name, namespace, path, requires).

#### `tampermonkey_get`
* **Purpose**: Get content of a specific userscript.
* **Input**: `path` (from list), optional `ifNotModifiedSince` timestamp.
* **Output**: Script content, lastModified timestamp, or error.

#### `tampermonkey_patch`
* **Purpose**: Update userscript content.
* **Input**: `path`, `value` (new content), optional `lastModified` for optimistic locking.
* **Output**: Success confirmation or error.

#### `tampermonkey_put`
* **Purpose**: Create a new userscript with the given name and namespace.
* **Input**: `value` (new script), optional `lastModified`.
* **Output**: Success confirmation, path of created script, or error.
* **Requires**: Tampermonkey Editors 1.0.6+ and Tampermonkey 5.6+

#### `tampermonkey_delete`
* **Purpose**: Delete an existing userscript.
* **Input**: `path` (from list).
* **Output**: Success confirmation or error.
* **Requires**: Tampermonkey Editors 1.0.6+ and Tampermonkey 5.6+


## Basic testing
### MCP Server capabilities

```bash
curl -X POST http://localhost:4001/mcp \
  -H "Content-Type: application/json" \
  -H "Accept: application/json, text/event-stream" \
  -d '{
    "jsonrpc": "2.0",
    "id": 1,
    "method": "initialize",
    "params": {
      "protocolVersion": "2024-11-05",
      "clientInfo": {
        "name": "curl-client",
        "version": "1.0.0"
      },
      "capabilities": {}
    }
  }'
```

### test stdio

```bash
echo '{"jsonrpc":"2.0","id":1,"method":"initialize","params":{"protocolVersion":"2024-11-05","clientInfo":{"name":"test-client","version":"1.0.0"},"capabilities":{}}}' | npx -y tampermonkey-mcp
echo '{"jsonrpc":"2.0","id":2,"method":"tools/list","params":{}}' | npx -y tampermonkey-mcp
echo '{"jsonrpc":"2.0","id":3,"method":"tools/call","params":{"name":"tampermonkey_list","arguments":{"pattern":""}}}' | npx -y tampermonkey-mcp
```
