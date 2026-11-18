# ScriptCat 特有 API 参考

以下 API 和元数据为 ScriptCat 独有，不兼容 Tampermonkey / Violentmonkey。使用时建议在注释中标注 `// ScriptCat only`。

---

### 后台脚本与定时任务

#### @background

声明脚本为后台脚本。运行环境是 ScriptCat 的 Offscreen 沙箱（架构链 SW → Offscreen → Sandbox，
`src/app/service/offscreen/` 与 `sandbox/`），不是 Service Worker；没有目标网页的 DOM，
`GM_getTab` / `GM_saveTab` / `GM_getTabs` 不可用，但 `GM_registerMenuCommand` 可用
（菜单出现在 ScriptCat 的弹窗）。无需匹配页面，脚本启用与浏览器启动时运行。

```js
// ==UserScript==
// @name         后台监控脚本
// @background
// @grant        GM_xmlhttpRequest
// @grant        GM_notification
// @connect      api.example.com
// ==/UserScript==

return new Promise((resolve, reject) => {
  GM.xmlHttpRequest({
    url: 'https://api.example.com/status',
    onload: (res) => resolve(res.status),
    onerror: () => reject(new Error('request failed')),
  });
});
```

**注意**：脚本体被包进 async 函数，同步部分（含顶层 await）跑完即判运行完成，
之后的 GM 调用不保证生效——异步工作必须 `return` 一个 Promise，并在真正完成时
resolve/reject。resolve 记成功、reject 记错误（运行状态在脚本列表，输出走 `GM_log`
或 ScriptCat 日志页；release 版不保存 debug 级）。手动「运行一次」不会调度重试。

#### @crontab

定时执行表达式。**不需要 @background**：`src/pkg/utils/script.ts` 中只要出现 `@crontab`
就把脚本判为定时类型，且该判定优先于 `@background`。格式按 `src/pkg/utils/cron.ts`：
支持 5 位 `分 时 日 月 周`（推荐）与 6 位含秒 `秒 分 时 日 月 周`（不推荐——
后台定时做不到秒级准确，且额外耗性能）。

```js
// @crontab      0 9 * * *           // 每天 9:00（5 位，推荐）
// @crontab      */30 * * * *        // 每 30 分钟（5 位）
// @crontab      0 9 * * 1-5         // 工作日 9:00（5 位）
// @crontab      * * once * *        // 每天至多一次（once 扩展）
// @crontab      * once(9-17) * * *  // 9-17 点每小时至多一次
```

只写一行 `@crontab`：多行时运行期每行都会调度，但安装校验与脚本列表只取第一行，
任何一行解析失败会停掉该脚本的全部定时任务。`once` 表示该字段周期内至多跑一次，
周期按运行**开始**时刻计（失败的运行也算已用，需在周期内重试请 reject 一个 CATRetryError）；
`once(expr)` 只在 expr 的取值里挑第一次命中。用外部 cron 工具验证表达式时，
把 `once` 换成 `*`、`once(expr)` 换成 expr。

每次触发时脚本重新执行，执行完毕后自动回收。

#### CATRetryError

在后台脚本中抛出此错误可让 ScriptCat 稍后重试。

```js
// @background
try {
  const resp = await GM.xmlHttpRequest({ url: "https://api.example.com/data" });
  if (resp.status === 429) {
    throw new CATRetryError("请求限流", 60); // 60 秒后重试
  }
  // 处理数据...
} catch (e) {
  if (e instanceof CATRetryError) throw e;
  throw new CATRetryError("请求失败，稍后重试", 300); // 5 分钟后重试
}
```

构造函数：
- `new CATRetryError(message, seconds)` — N 秒后重试
- `new CATRetryError(message, date)` — 指定时间重试

重试队列每 5 秒检查一次，所以重试可能比请求的时间最晚到 5 秒；运行时长加重试间隔
要短于 cron 周期，否则两次运行会重叠。判据：官方 background.md。

---

### ScriptCat 独有函数

#### CAT_registerMenuInput

注册带输入框的菜单项。用户点击后弹出输入对话框。

`CAT_registerMenuInput` / `CAT_unregisterMenuInput` 需要**单独声明 grant**，
`@grant GM_registerMenuCommand` 不覆盖它们（官方 check.mjs 判据：只给 GM_registerMenuCommand
时报 `error grant-missing: CAT_registerMenuInput is used but not granted`）。

```js
// @grant CAT_registerMenuInput
// @grant CAT_unregisterMenuInput

CAT_registerMenuInput("设置延迟时间", (value) => {
  console.log("用户输入:", value);
}, {
  inputType: "number",       // "text" | "number" | "boolean"
  title: "延迟设置",
  inputLabel: "延迟秒数",
  inputDefaultValue: 5,
  inputPlaceholder: "请输入秒数",
});

// 取消注册
CAT_unregisterMenuInput(menuId);
```

（`CAT_unregisterMenuInput` 在 d.ts 里是 `GM_unregisterMenuCommand` 的别名。）

#### CAT_userConfig

打开脚本的用户配置页面（需在元数据中定义 UserConfig）。

```js
// @grant GM_registerMenuCommand

GM_registerMenuCommand("打开设置", () => {
  CAT_userConfig();
});
```

#### CAT_fetchDocument

获取 URL 内容并解析为 Document 对象。在内容脚本上下文中可用。

```js
const doc = await CAT_fetchDocument("https://example.com/page");
if (doc) {
  const title = doc.querySelector("title")?.textContent;
  const links = doc.querySelectorAll("a");
}
```

#### CAT_createBlobUrl

从 Blob 创建 URL。ScriptCat 管理 URL 生命周期（自动回收）。

```js
const blob = new Blob(["Hello"], { type: "text/plain" });
const url = await CAT_createBlobUrl(blob);
// 可在页面 DOM 中使用此 URL
```

#### CAT_fetchBlob

获取 URL 内容作为 Blob。主要用于 `GM.xmlHttpRequest` 的 stream 响应。

```js
const blob = await CAT_fetchBlob("blob:chrome-extension://xxx/yyy");
```

#### CAT_scriptLoaded

配合 `@early-start` 使用。通知 ScriptCat 脚本已完成初始化。

```js
// @early-start

// 脚本极早执行，可以拦截全局对象
Object.defineProperty(window, 'someGlobal', { value: 'intercepted' });

// 通知初始化完成
await CAT_scriptLoaded();
```

---

### 文件存储

#### CAT_fileStorage

操作 ScriptCat 的云端/本地文件存储系统。每个脚本有独立的 `app/<uuid>` 目录。

```js
// 上传文件
CAT_fileStorage("upload", {
  path: "data/export.json",
  data: new Blob([JSON.stringify(data)], { type: "application/json" }),
  onload: () => console.log("上传成功"),
  onerror: (err) => console.error("上传失败:", err.error),
});

// 列出文件
CAT_fileStorage("list", {
  path: "data/",
  onload: (files) => {
    // files: [{ name, path, absPath, size, digest, createtime, updatetime }]
    files.forEach(f => console.log(f.name, f.size));
  },
});

// 下载文件
CAT_fileStorage("download", {
  file: fileInfo, // 从 list 返回的文件对象
  onload: (blob) => {
    const text = await blob.text();
  },
});

// 删除文件
CAT_fileStorage("delete", {
  path: "data/old.json",
  onload: () => console.log("删除成功"),
});

// 打开存储配置
CAT_fileStorage("config");
```

**错误码**（判据：`scriptcat.d.ts` 的 `CATType.FileStorageError.code`）：
| code | 含义 |
|------|------|
| -1 | 未知错误 |
| 1 | 存储未配置 |
| 2 | 配置错误 |
| 3 | 路径不存在 |
| 4 | 上传失败 |
| 5 | 下载失败 |
| 6 | 删除失败 |
| 7 | 文件路径不允许 |
| 8 | 网络错误 |

---

### GM_registerMenuCommand 扩展选项

ScriptCat 对标准 `GM_registerMenuCommand` 增加了以下选项：

```js
GM_registerMenuCommand("菜单项", callback, {
  accessKey: "m",
  autoClose: true,
  nested: false,      // SC: false 时提升到浏览器右键菜单
  individual: true,   // SC: 不合并同名菜单项
});

// GM.registerMenuCommand 额外支持：
await GM.registerMenuCommand("菜单项", callback, {
  icon: "https://example.com/icon.png", // SC: 菜单图标
  closeOnClick: true,                    // SC: alias for autoClose
});
```

---

### CAT.agent.* — Agent API

ScriptCat Agent 扩展 API，用于在用户脚本中调用 AI 能力和浏览器自动化。每个子 API 需单独声明 `@grant`。

#### CAT.agent.conversation — AI 对话

创建 LLM 对话，支持工具调用和流式输出。

```js
// @grant CAT.agent.conversation

const conv = await CAT.agent.conversation.create({
  system: "你是一个翻译助手",
  model: "model-id",       // 可选，默认使用用户配置的模型
  maxIterations: 10,
  tools: [{
    name: "get_page_text",
    description: "获取当前页面文本",
    parameters: { type: "object", properties: {} },
    handler: async () => document.body.innerText.slice(0, 5000),
  }],
});

// 非流式
const reply = await conv.chat("翻译这段话：Hello World");
console.log(reply.content);

// 流式
const stream = await conv.chatStream("翻译页面内容");
for await (const chunk of stream) {
  if (chunk.type === "content_delta") process.stdout.write(chunk.content);
  if (chunk.type === "tool_call") console.log("调用工具:", chunk.toolCall.name);
  if (chunk.type === "error") console.error(chunk.error);
}
```

#### CAT.agent.dom — 浏览器 DOM 操作

```js
// @grant CAT.agent.dom

const tabs = await CAT.agent.dom.listTabs();
await CAT.agent.dom.navigate("https://example.com", { tabId: tabs[0].tabId });
const page = await CAT.agent.dom.readPage({ tabId: tabs[0].tabId, selector: "main" });
const screenshot = await CAT.agent.dom.screenshot({ tabId: tabs[0].tabId });
await CAT.agent.dom.click("#button", { tabId: tabs[0].tabId, trusted: true });
await CAT.agent.dom.fill("input[name=q]", "text", { tabId: tabs[0].tabId });
await CAT.agent.dom.scroll("down", { tabId: tabs[0].tabId });
await CAT.agent.dom.waitFor(".result", { tabId: tabs[0].tabId, timeout: 5000 });
const result = await CAT.agent.dom.executeScript("return document.title", { tabId: tabs[0].tabId });
```

#### CAT.agent.task — 定时任务管理

```js
// @grant CAT.agent.task

// 创建定时任务（Agent 自动执行 prompt）
const task = await CAT.agent.task.create({
  name: "每日检查",
  crontab: "0 9 * * *",
  mode: "internal",
  enabled: true,
  prompt: "检查仪表盘并汇总异常",
  skills: "auto",
});

// 创建事件模式任务（脚本自己处理）
const eventTask = await CAT.agent.task.create({
  name: "数据同步",
  crontab: "0 */30 * * *",
  mode: "event",
  enabled: true,
});
CAT.agent.task.addListener(eventTask.id, (trigger) => {
  console.log("触发:", trigger.name, trigger.triggeredAt);
});
```

#### CAT.agent.skills — Skill 管理

```js
// @grant CAT.agent.skills

const skills = await CAT.agent.skills.list();
const result = await CAT.agent.skills.call("browser-automation", "screenshot", { tabId: 123 });
```

#### CAT.agent.model — 模型查询

```js
// @grant CAT.agent.model

const models = await CAT.agent.model.list();
const defaultId = await CAT.agent.model.getDefault();
```

#### CAT.agent.opfs — 工作区文件系统

```js
// @grant CAT.agent.opfs

await CAT.agent.opfs.write("data/report.txt", "内容...");
const file = await CAT.agent.opfs.read("data/report.txt");
const entries = await CAT.agent.opfs.list("data/");
await CAT.agent.opfs.delete("data/old.txt");
```

---

### 其他 ScriptCat 专属元数据

#### @inject-into

取值域 `page`（默认）/ `content`（判据：`SUPPORTED_TAG_VALUES["inject-into"]`、
`isInjectIntoContent`）。`content` 把脚本放到内容脚本世界：不受页面 CSP 影响，
但 `unsafeWindow` 不再是页面的 `window`。

```js
// @inject-into  content
```

#### UserConfig 配置块

头部之后可放一个 YAML 块，ScriptCat 据此生成设置表单；字段值以
`GM_getValue("<组>.<键>")` 读取（需 `@grant GM_getValue`），`CAT_userConfig()` 打开表单。

```js
/* ==UserConfig==
general:
  token:
    title: API token
    type: text
    password: true
  interval:
    title: 刷新间隔
    type: number
    default: 10
    min: 5
    max: 60
    unit: min
  mode:
    title: 模式
    type: select
    default: fast
    values: [fast, safe]
 ==/UserConfig== */
```

- 组是顶层键，每组一个标签页；`---` 可分成多段 YAML。
- `type` 取值：`text` / `textarea` / `number` / `checkbox` / `switch` / `select` / `mult-select`；
  省略时按 default 与 values 推断，单选请显式写 `type: select`。
- `number` 用 `min`/`max` 约束，`text` 只用 `max` 作最大长度；`mult-select` 的 default 是数组。
- 读值时把默认值一并传给 `GM_getValue`，不要假定表单 default 已落盘。
（判据：官方技能 `scriptcat/skills/scriptcat-userscript/references/userconfig.md`。）

---

### 通知与页面信息补充

- `GM_closeNotification(id)` / `GM_updateNotification(id, details)`：ScriptCat 独有
  （`updateNotification` 在 Firefox 不支持）。`NotificationDetails` 还定义了
  `progress`（进度）、`buttons`（最多 2 个按钮，`NotificationButton`）、
  `image`、`silent`、`highlight`、`oncreate` / `ondone` 等字段。
- `GM_openInTab(url, options)` 的 `OpenTabOptions` 比 Tampermonkey 多 `useOpen`
  （用 `window.open` 打开 `vscode://`、`m3u8dl://` 之类自定义协议，此模式下其余选项被忽略）
  与 `pinned`（固定新标签页）；`insert` 取值为 `true`/`1`/`false`/`0`，
  `incognito` 在 ScriptCat 用 `"split"` 语义。以上均见 `scriptcat.d.ts`。
- **默认值两端相反**（跨端脚本最容易踩的一处）：ScriptCat 的 `active` 与 `insert`
  默认都是 `true`（前台打开、插在当前标签后），Tampermonkey 的两者默认都是 `false`
  （判据：`scriptcat.d.ts` 的 `@default true` 对照 `@types/tampermonkey` 的
  "default is `false`" 注释）。不显式传值时，同一行调用在两端的落点不同。
- `GM_info.scriptMetaStr`：头部原文；`GM_info.userLanguage`：ScriptCat 界面语言
  （如 `zh-CN`），用于本地化脚本自身文案。
- `CAT_setProxy(rules | string)` / `CAT_clearProxy()`：设置/清除浏览器代理规则；
  `CAT_click(x, y)`：坐标级真实点击。三者判据均在 `scriptcat.d.ts`，
  官方技能标注为 **deprecated（正式版已移除，beta 可能回归）**——新脚本不要依赖。


### 完整后台脚本示例

```js
// ==UserScript==
// @name         价格监控
// @namespace    https://scriptcat.org/
// @version      0.1.0
// @description  每小时检查商品价格，降价时通知 // ScriptCat only
// @background
// @crontab      0 0 * * * *
// @grant        GM_xmlhttpRequest
// @grant        GM_getValue
// @grant        GM_setValue
// @grant        GM_notification
// @connect      api.example.com
// ==/UserScript==

"use strict";

const TARGET_URL = "https://api.example.com/product/123";
const PRICE_KEY = "last_price";

try {
  const resp = await GM.xmlHttpRequest({ url: TARGET_URL, responseType: "json" });
  const currentPrice = resp.response.price;
  const lastPrice = await GM.getValue(PRICE_KEY, Infinity);

  if (currentPrice < lastPrice) {
    GM.notification({
      title: "降价提醒！",
      text: `价格从 ¥${lastPrice} 降到 ¥${currentPrice}`,
      timeout: 0, // 不自动消失
    });
  }

  await GM.setValue(PRICE_KEY, currentPrice);
} catch (e) {
  throw new CATRetryError("检查失败，5 分钟后重试", 300);
}
```

> 后台/定时脚本建议在结尾 `return` 一个 Promise 并在真正完成时 resolve：
> 同步部分跑完 ScriptCat 就标记运行结束，之后的 GM 调用不保证生效；
> 手动"运行一次"不会调度 `CATRetryError` 的重试。详见官方技能
> `scriptcat/skills/scriptcat-userscript`（跟踪源，见 SYNCLOG.md）。
