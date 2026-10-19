**非官方**中文语言包，适配 **Strata v0.2.0-beta**（`e88ee39d`，v0.2.0-beta 之后 12 个提交；0.1.40.x 起均可用）。

> **这一版是跟版更新，改动很小但有一处必须更：** 官方 0.2.0-beta 的 `serve/web/` 与 0.1.45 **完全一致**（`git diff v0.1.45..HEAD -- serve/web` 为空），页面结构与文案零变动；但**模型设置页的说明句来自 `serve/runconfig.py`**，官方改了其中一条，旧译文因此对不上：
>
> | 官方新文案 | 本包新译文 |
> |---|---|
> | `Shorten a max_tokens that does not fit the context (on by default); off: answer 400 like llama.cpp` | 超出上下文窗口的 max_tokens 会被自动缩短（默认开启）；关闭后像 llama.cpp 一样直接返回 400 错误 |
>
> 旧句（`… instead of answering 400`）的译文保留，装 0.1.45 及更早版本时照旧生效。
>
> **另外新增：模型设置页保存失败时的中文报错。** 这些提示是服务端 `ValueError` 原文，直接显示在右上角弹窗里，以前只能看到英文。本版用 8 条正则规则接住：
>
> - `lazy_load: lazy loading is text-only, and this model reads images ("vision")` → **延迟加载（lazy_load）只支持纯文本模型，而当前模型能读图片（vision），无法开启**
> - `sampling.top_k: expected a whole number, at least 1 and at most 64, not 90` → **sampling.top_k：需要一个整数，至少 1、最多 64，当前是 90**
> - `… expected true or false, not 'yes'` / `… expected one of model, on_request, not 'auto'` / `… expected a list of model names, not 42`
> - `'foo' cannot be changed here (only the keys the Settings view lists)` → **“foo”不能在这里修改（只能改设置页列出的键）**
> - `xxx.json is not a JSON object`、`send {"set": …}`
>
> **顺带补齐 4 条漏网文案**：采样抽屉的 `Top-p` →「Top-p（累积概率）」、`Top-k` →「Top-k（候选数）」；保存成功提示 `Saved to the run config; used from the next start of the model.`；值占位 `not set` →「未设置」；监视页截断提示 `Monitor capture truncated at 256K characters…`。
>
> 词典 275 条词条 + 46 条正则规则，共 730 行（上一版 264 条 / 38 条）。

## 安装

下载下面的 zip → 解压 → 双击 **`install-zh.bat`** → 浏览器 **Ctrl+F5**。

自动找不到 Strata 时，把路径传给它：

```bat
install-zh.bat "D:\Strata"
```

## 效果

- 顶栏左上角 **Language** 按钮：**英文 / 简体中文 / 中英文**
- **模型输出永不翻译** —— 聊天正文、思考过程、代码块、工具调用参数与结果原样保留
- 覆盖 0.2.0-beta 界面全部用户可见文案，含图片生成页、模型设置页 15 个配置键的说明句、采样抽屉、会话缓存与 MCP 卡片
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

0.2.0-beta 没有改动 `serve/web/`，若只是更新引擎与 Python 包，第 1、3 步可省略（本包的挂载点会保留）；但只要官方哪天再改页面，就必须走完整三步。

> 小提示：本机实测 `github.com:443` 直连不通时，`git config url."https://ghfast.top/https://github.com/".insteadOf "https://github.com/"` 可让 `git pull` 与 UPDATE.bat 恢复正常。

## 许可与致谢

**MIT License**，保留原作者版权声明。感谢 [Niko1221](https://github.com/Niko1221/Strata) 与 Strata 贡献者。

模型权重不在本包内；Qwen3.8-Flash-Next 适用 **Qwen Community License 1.0**（非 MIT），详见 `NOTICE.md`。

本包为**非官方**作品，与 Strata 项目无隶属或背书关系。

上游 PR：[Niko1221/Strata#1836](https://github.com/Niko1221/Strata/pull/1836)。它是在官方 **0.2.0-beta 追踪器重置** 中被统一关闭的，不是拒绝 —— 维护者给了 4 步 `/reopen` 流程（rebase 到 main、标题加 `[GUI]`/`[Other]` 前缀、填 PR 模板的问题/结果/验证、评论 `/reopen`）。语言包会继续跟随官方版本更新。

---

*Unofficial Chinese localisation pack for the [Strata](https://github.com/Niko1221/Strata) web interface (MIT). Adds a `Language` button with English / Simplified Chinese / Chinese + English. The model's output is never rewritten. Contains no Strata source, no engine binaries and no model weights.*
