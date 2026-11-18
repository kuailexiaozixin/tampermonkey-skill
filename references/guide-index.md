# 油猴教程学习指南（scriptscat/tampermonkey-learn-guide）— 全量收录索引

> `references/guide/` 是 [scriptscat/tampermonkey-learn-guide](https://github.com/scriptscat/tampermonkey-learn-guide) 
> `docs/` 的**完整镜像**（95 篇正文 + 配图），随技能一起分发（本索引自研，放在镜像目录之外以免被同步覆盖）；上游跟踪方式见 
> `../manifest.json` 与 `../scripts/sync_upstream.py`，同步记录见 `../SYNCLOG.md`。
>
> 仓库未提供 LICENSE 文件；此处按原样收录并全程注明来源，只作学习参考，勿复制正文进自研材料。
> 文内图片路径（`./img/...`）在本地同样可解析；站内链接写作 `/油猴教程/...` 形式，对应本目录 `01.油猴教程/...`。

## 怎么用这 95 篇

- **入门篇**（17 篇）：第一个脚本、模拟点击、grant/none/unsafeWindow、沙盒机制、run-at、
  跨域 ajax、加新元素、外部资源、右键菜单与存储、GM_addStyle、hook、XHR/fetch 劫持、
  addEventListener 劫持、基础调试。写脚本前先按这里对齐概念。
- **中级篇**（11 篇）：元素规则校验、WebSocket 劫持、Vue 初探、本地文件权限、iframe、
  前端路由监听、video.js、shadowRoot、Vue3、堆栈异常利用。处理 SPA 与框架页面时查。
- **高级篇**（5 篇）：破解复制限制、Webpack 劫持实例、React 富文本输入框、VSCode 开发体验。
- **工程篇**（14 篇）：Node/npm/webpack、模块化八讲（AMD/CMD/UMD/CJS/ESM 与混用问题）。
- **实战篇**（10 篇）：抖音无水印下载、百度分享码、知乎/快手 Fetch 劫持、鼠标限制破解、
  React 数据提取、秒杀提取、B 站动态加载、videojs 去广告、智慧树 shadowRoot。
- **原理/番外**（8 篇）：油猴本质与 document 处理、脚本与网页作用域、Script 标签初始化劫持、
  isTrusted 验证绕过、Node 轻量模糊搜索。
- **实用知识库**（27 篇）：JavaScript 十五讲（this/箭头函数/原型链/属性劫持/Proxy/选择器）、
  Promise 五讲、MutationObserver 四讲、引用库十一讲（Vue、Element Plus、FileSaver、JSZip、
  toastr、SweetAlert2、jQuery、下载器、NPM 魔改包、Layui）。
- **常见问题**（2 篇）：常见误区两篇。

## 篇目清单（95）

### 油猴教程（63 篇）

| 标题 | 文件 |
|---|---|
| 第一个脚本-HelloWorld | [01.油猴教程/01.入门篇/01.第一个脚本-HelloWorld.md](guide/01.油猴教程/01.入门篇/01.第一个脚本-HelloWorld.md) |
| 脚本自动化之模拟点击和表单填写 | [01.油猴教程/01.入门篇/02.脚本自动化之模拟点击和表单填写.md](guide/01.油猴教程/01.入门篇/02.脚本自动化之模拟点击和表单填写.md) |
| grant介绍,none与unsafeWindow | [01.油猴教程/01.入门篇/03.grant介绍,none与unsafeWindow.md](guide/01.油猴教程/01.入门篇/03.grant介绍,none与unsafeWindow.md) |
| 沙盒机制的前世今生 | [01.油猴教程/01.入门篇/04.沙盒机制的前世今生.md](guide/01.油猴教程/01.入门篇/04.沙盒机制的前世今生.md) |
| H5视频倍速,时间加速和run-at | [01.油猴教程/01.入门篇/05.h5视频倍速,时间加速和run-at.md](guide/01.油猴教程/01.入门篇/05.h5视频倍速,时间加速和run-at.md) |
| 脚本ajax的跨域请求 | [01.油猴教程/01.入门篇/06.脚本ajax的跨域请求.md](guide/01.油猴教程/01.入门篇/06.脚本ajax的跨域请求.md) |
| 使用脚本向页面上添加新元素 | [01.油猴教程/01.入门篇/07.使用脚本向页面上添加新元素.md](guide/01.油猴教程/01.入门篇/07.使用脚本向页面上添加新元素.md) |
| 外部资源引用 | [01.油猴教程/01.入门篇/08.外部资源引用.md](guide/01.油猴教程/01.入门篇/08.外部资源引用.md) |
| 右键菜单与 GM 存储函数介绍 | [01.油猴教程/01.入门篇/09.右键菜单与GM存储函数介绍.md](guide/01.油猴教程/01.入门篇/09.右键菜单与GM存储函数介绍.md) |
| GM_addStyle去除网页广告 | [01.油猴教程/01.入门篇/10.GM_addStyle去除网页广告.md](guide/01.油猴教程/01.入门篇/10.GM_addStyle去除网页广告.md) |
| hook实现b站评论小尾巴 | [01.油猴教程/01.入门篇/11.hook实现b站评论小尾巴.md](guide/01.油猴教程/01.入门篇/11.hook实现b站评论小尾巴.md) |
| 百度去广告及判断去除元素 | [01.油猴教程/01.入门篇/12.百度去广告及判断去除元素.md](guide/01.油猴教程/01.入门篇/12.百度去广告及判断去除元素.md) |
| XHR 提交劫持与内容监听 | [01.油猴教程/01.入门篇/13.XHR提交劫持与内容监听.md](guide/01.油猴教程/01.入门篇/13.XHR提交劫持与内容监听.md) |
| XHR 返回内容劫持 | [01.油猴教程/01.入门篇/14.XHR返回内容劫持.md](guide/01.油猴教程/01.入门篇/14.XHR返回内容劫持.md) |
| Fetch 提交与返回内容 | [01.油猴教程/01.入门篇/15.Fetch提交与返回内容劫持.md](guide/01.油猴教程/01.入门篇/15.Fetch提交与返回内容劫持.md) |
| addEventListener 劫持 | [01.油猴教程/01.入门篇/16.addEventListener劫持.md](guide/01.油猴教程/01.入门篇/16.addEventListener劫持.md) |
| 脚本基础调试与控制台介绍 | [01.油猴教程/01.入门篇/17.脚本基础调试与控制台介绍.md](guide/01.油猴教程/01.入门篇/17.脚本基础调试与控制台介绍.md) |
| 前言 | [01.油猴教程/02.中级篇/01.前言.md](guide/01.油猴教程/02.中级篇/01.前言.md) |
| 元素规则校验和检测的触发 | [01.油猴教程/02.中级篇/02.元素规则校验和检测的触发.md](guide/01.油猴教程/02.中级篇/02.元素规则校验和检测的触发.md) |
| WebSocket 提交返回劫持 | [01.油猴教程/02.中级篇/03.WebSocket提交返回劫持.md](guide/01.油猴教程/02.中级篇/03.WebSocket提交返回劫持.md) |
| Vue 初探与代码分析 | [01.油猴教程/02.中级篇/04.Vue初探与代码分析.md](guide/01.油猴教程/02.中级篇/04.Vue初探与代码分析.md) |
| 本地文件访问权限与外部开发 | [01.油猴教程/02.中级篇/05.本地文件访问权限与外部开发.md](guide/01.油猴教程/02.中级篇/05.本地文件访问权限与外部开发.md) |
| 处理 iframe 的碎碎念 | [01.油猴教程/02.中级篇/06.处理iframe的碎碎念.md](guide/01.油猴教程/02.中级篇/06.处理iframe的碎碎念.md) |
| 监听前端路由改变 | [01.油猴教程/02.中级篇/07.监听前端路由改变.md](guide/01.油猴教程/02.中级篇/07.监听前端路由改变.md) |
| video.js 劫持方式分析 | [01.油猴教程/02.中级篇/08.video.js劫持方式分析.md](guide/01.油猴教程/02.中级篇/08.video.js劫持方式分析.md) |
| shadowRoot 的基础介绍 | [01.油猴教程/02.中级篇/09.shadowRoot基础介绍.md](guide/01.油猴教程/02.中级篇/09.shadowRoot基础介绍.md) |
| Vue3 的初步处理方案 | [01.油猴教程/02.中级篇/10.Vue3的初步处理方案.md](guide/01.油猴教程/02.中级篇/10.Vue3的初步处理方案.md) |
| 堆栈异常抛出的利用技巧 | [01.油猴教程/02.中级篇/11.堆栈异常抛出的利用技巧.md](guide/01.油猴教程/02.中级篇/11.堆栈异常抛出的利用技巧.md) |
| 前言 | [01.油猴教程/03.高级篇/01.前言.md](guide/01.油猴教程/03.高级篇/01.前言.md) |
| 实战破解 Vue 百度文库复制 | [01.油猴教程/03.高级篇/02.实战破解Vue百度文库复制.md](guide/01.油猴教程/03.高级篇/02.实战破解Vue百度文库复制.md) |
| 实战 Webpack 劫持 Vue 实例 | [01.油猴教程/03.高级篇/03.实战Webpack劫持Vue实例.md](guide/01.油猴教程/03.高级篇/03.实战Webpack劫持Vue实例.md) |
| 实战抖音 React 富文本输入框 | [01.油猴教程/03.高级篇/04.实战抖音React富文本输入框.md](guide/01.油猴教程/03.高级篇/04.实战抖音React富文本输入框.md) |
| 抹平 Tampermonkey 的 VSCode 开发体验 | [01.油猴教程/03.高级篇/05.抹平Tampermonkey的VSCode开发体验.md](guide/01.油猴教程/03.高级篇/05.抹平Tampermonkey的VSCode开发体验.md) |
| 前言 | [01.油猴教程/04.工程篇/01.前言.md](guide/01.油猴教程/04.工程篇/01.前言.md) |
| Nodejs简介与安装 | [01.油猴教程/04.工程篇/02.Nodejs简介与安装.md](guide/01.油猴教程/04.工程篇/02.Nodejs简介与安装.md) |
| npm简介 | [01.油猴教程/04.工程篇/03.npm简介.md](guide/01.油猴教程/04.工程篇/03.npm简介.md) |
| webpack简介 | [01.油猴教程/04.工程篇/04.webpack简介.md](guide/01.油猴教程/04.工程篇/04.webpack简介.md) |
| webpack 初体验 | [01.油猴教程/04.工程篇/05.webpack初体验.md](guide/01.油猴教程/04.工程篇/05.webpack初体验.md) |
| 模块化介绍 | [01.油猴教程/04.工程篇/06.模块化知识/01.模块化介绍.md](guide/01.油猴教程/04.工程篇/06.模块化知识/01.模块化介绍.md) |
| AMD 模块化介绍 | [01.油猴教程/04.工程篇/06.模块化知识/02.AMD模块化介绍.md](guide/01.油猴教程/04.工程篇/06.模块化知识/02.AMD模块化介绍.md) |
| CMD 模块化介绍 | [01.油猴教程/04.工程篇/06.模块化知识/03.CMD模块化介绍.md](guide/01.油猴教程/04.工程篇/06.模块化知识/03.CMD模块化介绍.md) |
| UMD 模块化介绍 | [01.油猴教程/04.工程篇/06.模块化知识/04.UMD模块化介绍.md](guide/01.油猴教程/04.工程篇/06.模块化知识/04.UMD模块化介绍.md) |
| CommonJS 模块化介绍 | [01.油猴教程/04.工程篇/06.模块化知识/05.CommonJS模块化介绍.md](guide/01.油猴教程/04.工程篇/06.模块化知识/05.CommonJS模块化介绍.md) |
| ES6 模块化介绍 | [01.油猴教程/04.工程篇/06.模块化知识/06.ES6模块化介绍.md](guide/01.油猴教程/04.工程篇/06.模块化知识/06.ES6模块化介绍.md) |
| CommonJS 与 ES6 模块混用问题 | [01.油猴教程/04.工程篇/06.模块化知识/07.CommonJS与ES6模块混用问题.md](guide/01.油猴教程/04.工程篇/06.模块化知识/07.CommonJS与ES6模块混用问题.md) |
| Webpack 中模块混用问题 | [01.油猴教程/04.工程篇/06.模块化知识/08.Webpack中模块混用问题.md](guide/01.油猴教程/04.工程篇/06.模块化知识/08.Webpack中模块混用问题.md) |
| 抖音短视频无水印下载 | [01.油猴教程/05.实战篇/01.抖音短视频无水印下载.md](guide/01.油猴教程/05.实战篇/01.抖音短视频无水印下载.md) |
| 实战百度自定义分享码 | [01.油猴教程/05.实战篇/02.实战百度自定义分享码.md](guide/01.油猴教程/05.实战篇/02.实战百度自定义分享码.md) |
| 实战Fetch劫持知乎返回内容 | [01.油猴教程/05.实战篇/03.实战Fetch劫持知乎返回内容.md](guide/01.油猴教程/05.实战篇/03.实战Fetch劫持知乎返回内容.md) |
| 实战 Fetch 劫持快手批量读取 | [01.油猴教程/05.实战篇/04.实战Fetch劫持快手批量读取.md](guide/01.油猴教程/05.实战篇/04.实战Fetch劫持快手批量读取.md) |
| 实战破解鼠标移出限制 | [01.油猴教程/05.实战篇/05.实战破解鼠标移出限制.md](guide/01.油猴教程/05.实战篇/05.实战破解鼠标移出限制.md) |
| 实战 React 数据提取抖音视频 | [01.油猴教程/05.实战篇/06.实战React数据提取抖音视频.md](guide/01.油猴教程/05.实战篇/06.实战React数据提取抖音视频.md) |
| 实战秒杀快手视频提取 | [01.油猴教程/05.实战篇/07.实战秒杀快手视频提取.md](guide/01.油猴教程/05.实战篇/07.实战秒杀快手视频提取.md) |
| 监听 B 站动态的加载的模块 | [01.油猴教程/05.实战篇/08.监听B站动态的加载的模块.md](guide/01.油猴教程/05.实战篇/08.监听B站动态的加载的模块.md) |
| 实战 91 学习网 videojs 去广告 | [01.油猴教程/05.实战篇/09.实战91学习网videojs去广告.md](guide/01.油猴教程/05.实战篇/09.实战91学习网videojs去广告.md) |
| 实战智慧树 shadowRoot | [01.油猴教程/05.实战篇/10.实战智慧树shadowRoot.md](guide/01.油猴教程/05.实战篇/10.实战智慧树shadowRoot.md) |
| 前言 | [01.油猴教程/06.原理篇/01.前言.md](guide/01.油猴教程/06.原理篇/01.前言.md) |
| 油猴的本质以及 document 的处理 | [01.油猴教程/06.原理篇/02.油猴的本质以及document的处理.md](guide/01.油猴教程/06.原理篇/02.油猴的本质以及document的处理.md) |
| 前言 | [01.油猴教程/07.番外篇/01.前言.md](guide/01.油猴教程/07.番外篇/01.前言.md) |
| 脚本与网页作用域的引申 | [01.油猴教程/07.番外篇/02.脚本与网页作用域的引申.md](guide/01.油猴教程/07.番外篇/02.脚本与网页作用域的引申.md) |
| Script 标签初始化对象劫持 | [01.油猴教程/07.番外篇/03.Script标签初始化对象劫持.md](guide/01.油猴教程/07.番外篇/03.Script标签初始化对象劫持.md) |
| 实战秒杀 isTrust 验证 | [01.油猴教程/07.番外篇/04.实战秒杀isTrust验证.md](guide/01.油猴教程/07.番外篇/04.实战秒杀isTrust验证.md) |
| 实现 Node.js 的轻量级模糊搜索 | [01.油猴教程/07.番外篇/05.实现Node.js的轻量级模糊搜索.md](guide/01.油猴教程/07.番外篇/05.实现Node.js的轻量级模糊搜索.md) |

### 实用知识库（27 篇）

| 标题 | 文件 |
|---|---|
| this 的作用 | [02.实用知识库/01.JavaScript 知识篇/01.this的作用.md](guide/02.实用知识库/01.JavaScript 知识篇/01.this的作用.md) |
| this 的推导 | [02.实用知识库/01.JavaScript 知识篇/02.this的推导.md](guide/02.实用知识库/01.JavaScript 知识篇/02.this的推导.md) |
| 箭头函数 | [02.实用知识库/01.JavaScript 知识篇/03.箭头函数.md](guide/02.实用知识库/01.JavaScript 知识篇/03.箭头函数.md) |
| 原型与原型链 | [02.实用知识库/01.JavaScript 知识篇/04.原型与原型链.md](guide/02.实用知识库/01.JavaScript 知识篇/04.原型与原型链.md) |
| 对象的属性劫持 | [02.实用知识库/01.JavaScript 知识篇/05.对象的属性劫持.md](guide/02.实用知识库/01.JavaScript 知识篇/05.对象的属性劫持.md) |
| Proxy 与 Reflect 的使用 | [02.实用知识库/01.JavaScript 知识篇/06.Proxy的使用.md](guide/02.实用知识库/01.JavaScript 知识篇/06.Proxy的使用.md) |
| querySelector 与 css 选择器入门 | [02.实用知识库/01.JavaScript 知识篇/07.querySelector与css选择器入门.md](guide/02.实用知识库/01.JavaScript 知识篇/07.querySelector与css选择器入门.md) |
| 为什么需要 Promise | [02.实用知识库/01.JavaScript 知识篇/08.Promise 知识/01.为什么需要Promise.md](guide/02.实用知识库/01.JavaScript 知识篇/08.Promise 知识/01.为什么需要Promise.md) |
| Promise 基础 | [02.实用知识库/01.JavaScript 知识篇/08.Promise 知识/02.Promise基础.md](guide/02.实用知识库/01.JavaScript 知识篇/08.Promise 知识/02.Promise基础.md) |
| Promise 常用函数与语法糖 | [02.实用知识库/01.JavaScript 知识篇/08.Promise 知识/03.Promise常用函数与语法糖.md](guide/02.实用知识库/01.JavaScript 知识篇/08.Promise 知识/03.Promise常用函数与语法糖.md) |
| 包装异步代码为同步代码 | [02.实用知识库/01.JavaScript 知识篇/08.Promise 知识/04.包装异步代码为同步代码.md](guide/02.实用知识库/01.JavaScript 知识篇/08.Promise 知识/04.包装异步代码为同步代码.md) |
| Promise 执行顺序问题 | [02.实用知识库/01.JavaScript 知识篇/08.Promise 知识/05.Promise执行顺序问题.md](guide/02.实用知识库/01.JavaScript 知识篇/08.Promise 知识/05.Promise执行顺序问题.md) |
| MutationObserve 的由来 | [02.实用知识库/01.JavaScript 知识篇/09.MutationObserve 知识/01.MutationObserve的由来.md](guide/02.实用知识库/01.JavaScript 知识篇/09.MutationObserve 知识/01.MutationObserve的由来.md) |
| MutationObserve 例子 | [02.实用知识库/01.JavaScript 知识篇/09.MutationObserve 知识/02.MutationObserve例子.md](guide/02.实用知识库/01.JavaScript 知识篇/09.MutationObserve 知识/02.MutationObserve例子.md) |
| MutationObserve 实战 | [02.实用知识库/01.JavaScript 知识篇/09.MutationObserve 知识/03.MutationObserve实战.md](guide/02.实用知识库/01.JavaScript 知识篇/09.MutationObserve 知识/03.MutationObserve实战.md) |
| 延迟查询代码范例解读 | [02.实用知识库/01.JavaScript 知识篇/09.MutationObserve 知识/04.延迟查询元素代码.md](guide/02.实用知识库/01.JavaScript 知识篇/09.MutationObserve 知识/04.延迟查询元素代码.md) |
| 引用方式的梗概 | [02.实用知识库/02.引用库使用/01.引用方式的梗概.md](guide/02.实用知识库/02.引用库使用/01.引用方式的梗概.md) |
| Vue 的引用 | [02.实用知识库/02.引用库使用/02.Vue的引用.md](guide/02.实用知识库/02.引用库使用/02.Vue的引用.md) |
| Element Plus 的引用 | [02.实用知识库/02.引用库使用/03.Element Plus的引用.md](guide/02.实用知识库/02.引用库使用/03.Element Plus的引用.md) |
| FileSaver 解决前端下载 | [02.实用知识库/02.引用库使用/04.FileSaver解决前端下载.md](guide/02.实用知识库/02.引用库使用/04.FileSaver解决前端下载.md) |
| `JSZip` 压缩解压文件 | [02.实用知识库/02.引用库使用/05.JSZip压缩解压文件.md](guide/02.实用知识库/02.引用库使用/05.JSZip压缩解压文件.md) |
| toastr 实现消息提示 | [02.实用知识库/02.引用库使用/06.toastr实现消息提示.md](guide/02.实用知识库/02.引用库使用/06.toastr实现消息提示.md) |
| `SweetAlert2` 实现对话框 | [02.实用知识库/02.引用库使用/07.SweetAlert2实现对话框.md](guide/02.实用知识库/02.引用库使用/07.SweetAlert2实现对话框.md) |
| jQuery 引用 | [02.实用知识库/02.引用库使用/08.Jquery引用.md](guide/02.实用知识库/02.引用库使用/08.Jquery引用.md) |
| 触发下载器实现下载 | [02.实用知识库/02.引用库使用/09.触发下载器实现下载.md](guide/02.实用知识库/02.引用库使用/09.触发下载器实现下载.md) |
| NPM 发布魔改包 | [02.实用知识库/02.引用库使用/10.NPM发布魔改包.md](guide/02.实用知识库/02.引用库使用/10.NPM发布魔改包.md) |
| Layui 库的引用 | [02.实用知识库/02.引用库使用/11.Layui库的引用.md](guide/02.实用知识库/02.引用库使用/11.Layui库的引用.md) |

### 常见问题（2 篇）

| 标题 | 文件 |
|---|---|
| 常见误区 (一) | [03.常见问题/01.常见误区1.md](guide/03.常见问题/01.常见误区1.md) |
| 常见误区 (二) | [03.常见问题/02.常见误区2.md](guide/03.常见问题/02.常见误区2.md) |

### (root)（3 篇）

| 标题 | 文件 |
|---|---|
| 感谢名单 | [感谢名单.md](guide/感谢名单.md) |
| 简介 | [简介.md](guide/简介.md) |
| 赞助名单 | [赞助名单.md](guide/赞助名单.md) |

