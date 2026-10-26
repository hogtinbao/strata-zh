**非官方**中文语言包，适配 **Strata v0.2.6**（`4b9e05a2`，tag `v0.2.6`；0.1.40.x 起均可用）。

> **这一版是跟版更新，改动很小，共 6 条：**

> | 官方文案（v0.2.6 新增） | 本包新译文 |
> |---|---|
> | `API key used for this page only`（`app.js`，#3435：浏览器不让存 localStorage 时的警告） | API 密钥仅在本页生效 |
> | `Browser storage is unavailable. Enter it again after reloading.` | 浏览器存储不可用，重新加载页面后需要重新输入。 |
> | `Draft layer (MTP): off starts the engine without it (about 1 GB less graphics memory, slower words per second); empty or on: as installed`（`runconfig.py` 新配置键 `mtp` 的说明句） | 草稿层（MTP）：关闭后启动引擎时不加载它（省约 1 GB 显存，但每秒出词更慢）；留空或开启 = 按安装时的设置 |
> | `unknown reasoning effort …: use none, low, medium, high, max or 1..100`（`frontend.py`，思考档位越界） | 思考档位 … 无法识别：可用 none / low / medium / high / max，或 1～100 的整数 |
> | `messages must be a non-empty list: send at least one message` | 消息列表不能为空：至少要发一条消息 |
> | `whitespace tool name is not declared` | 工具名里含空格，且请求中没有声明这个工具 |
>
> **另补回一条旧版漏掉的：** `0 · greedy` →「0 · 贪心」（温度为 0 时采样抽屉里的读数，0.2.0-beta 重建本文件时丢了）。

> 官方从 0.2.0-beta 到 0.2.6 的 `serve/web/` 只有 `app.js` 增了上面两条提示，其余四个提交（#3594、#3601、#2971、#3435 的 CSS 部分）只动样式与 DOM 结构，页面文案零变动。

> **历史沿革：** 0.1.42 把请求表拆成 `Prefill t/s` 与 `Decode t/s` 两列；0.1.44 新增图片生成页；0.1.45 改了采样默认温度的说明句；0.2.0-beta 改了 `fit_max_tokens` 的说明句并加入模型设置页保存失败的中文报错（8 类）。以上本包均已覆盖。

词典 311 条词条 + 4 条下拉项 + 16 条键名注释 + 50 条正则规则，共 745 行（上一版 306 / 4 / 15 / 46 / 729 行）。

## 安装

下载下面的 zip → 解压 → 双击 **`install-zh.bat`** → 浏览器 **Ctrl+F5**。

自动找不到 Strata 时，把路径传给它：

```bat
install-zh.bat "D:\Strata"
```

## 效果

- 顶栏左上角 **Language** 按钮：**英文 / 简体中文 / 中英文**
- **模型输出永不翻译** —— 聊天正文、思考过程、代码块、工具调用参数与结果原样保留
- 覆盖 0.2.6 界面全部用户可见文案，含图片生成页、模型设置页 16 个配置键的说明句、采样抽屉、会话缓存与 MCP 卡片
- 切换回 `English` 完全还原原版界面（含 `title` / `placeholder` / `aria-label` 与下拉项）

## 包含 / 不包含

| 包含 | 不包含 |
|---|---|
| `i18n-zh.js`（汉化层，独立文件） | Strata 源码 |
| `apply_zh_ui.py`（安装/卸载/检查） | 引擎二进制 |
| `install-zh.bat` · `uninstall-zh.bat` | **模型权重** |
| `README.md` · `NOTICE.md` · `LICENSE` | |

安装器改页面之前会存 `.zhbak` 备份，卸载可逐字节还原。

## 升级 Strata 时（重要）

官方 `UPDATE.bat` 用 `git pull`，页面被改过会让它失败。顺序是：

1. `uninstall-zh.bat` 卸载
2. 运行官方 `UPDATE.bat`
3. `install-zh.bat` 装回

0.2.0-beta → 0.2.6 没有改动 `serve/web/` 的页面结构（`index.html` / `monitor.html` 除新增脚本行外一致），若只是更新引擎与 Python 包，第 1、3 步可省略（本包的挂载点会保留）；但只要官方哪天再改页面，就必须走完整三步。

> 小提示：本机实测 `github.com:443` 直连不通时，`git config url."https://ghfast.top/https://github.com/".insteadOf "https://github.com/"` 可让 `git pull` 与 UPDATE.bat 恢复正常。

## 许可与致谢

**MIT License**，保留原作者版权声明。感谢 [Niko1221](https://github.com/Niko1221/Strata) 与 Strata 贡献者。

模型权重不在本包内；Qwen3.8-Flash-Next 适用 **Qwen Community License 1.0**（非 MIT），详见 `NOTICE.md`。

本包为**非官方**作品，与 Strata 项目无隶属或背书关系。

上游 PR：[Niko1221/Strata#3293](https://github.com/Niko1221/Strata/pull/3293)（取代被官方 0.2.0-beta 追踪器重置关闭的 #1836，不是拒绝）。语言包会继续跟随官方版本更新。

---

*Unofficial Chinese localisation pack for the [Strata](https://github.com/Niko1221/Strata) web interface (MIT). Adds a `Language` button with English / Simplified Chinese / Chinese + English. The model's output is never rewritten. Contains no Strata source, no engine binaries and no model weights.*
