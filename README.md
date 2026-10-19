# Strata中文版

**非官方** · 基于 [Strata](https://github.com/Niko1221/Strata) · MIT License

一个给 Strata 网页界面用的**中文语言包**。装完点顶栏左上角的 `Language` 按钮，就能在 **英文 / 简体中文 / 中英文** 之间切换。

> 本包**不包含** Strata 源码、**不包含**引擎二进制、**不包含模型权重**。模型请按 Strata 官方流程自行下载。

---

## 效果

- **三档语言**：`English`（原版界面）/ `简体中文` / `中英文`（中文在上、英文小字在下）
- **模型输出永不翻译** —— 聊天正文、思考过程、代码块、工具调用参数与结果，**原样保留**。切到中文只是把界面变中文，模型写什么就显示什么。
- **覆盖完整**：0.2.0-beta 界面里所有用户可见文案，含
  - 聊天、监控、关于三个页面与状态栏
  - **图片生成页**（0.1.44 新增）：标题、提示词输入框、尺寸/种子、生成按钮、提示语与结果区文案（该标签页仅在服务端声明支持图片生成时显示，译文已就位）
  - 采样抽屉（思考档位、temperature、top_p…）
  - **模型设置页**：15 个配置键的说明句 + 下拉项（`默认 (default)`、`开 (on)`…）+ 键名中文注释（`sampling.top_p（核采样范围）`）
  - 只有鼠标悬停或读屏才看到的 `title` / `placeholder` / `aria-label`
- **切回 English 完全还原原版**，包括属性和下拉项。

## 兼容版本

**Strata v0.2.0-beta**（0.1.40.x 起均可）。官方 0.2.0-beta 的 `serve/web/` 与 0.1.45 完全一致，页面结构与文案零变动；变的是模型设置页的说明句来源 `serve/runconfig.py`，其中 `fit_max_tokens` 一条被改写，译文已同步（旧句译文保留，装 0.1.45 及更早版本照旧生效）。这一版还把**模型设置页保存失败的中文报错**补上了：这些提示是服务端原文，以前只显示英文（`lazy_load: lazy loading is text-only…`、`sampling.top_k: expected a whole number…` 等 8 类），现在都有中文。历史沿革：0.1.42 把请求表拆成 `Prefill t/s` 与 `Decode t/s` 两列，0.1.44 新增图片生成页，0.1.45 没有新增界面文案只改了采样默认值逻辑 —— 以上本包均已覆盖。

## 安装

### 一键（Windows）

1. 把本目录解压到任意位置
2. 双击 **`install-zh.bat`**

自动找不到 Strata 时，把路径传给它：

```bat
install-zh.bat "D:\Strata"
```

### 手动（三步）

1. 复制 `i18n-zh.js` 到 `<Strata>\serve\web\`
2. 编辑 `<Strata>\serve\web\index.html`，在 `<script src="web/app.js"></script>` 下面加一行：
   ```html
   <script src="web/i18n-zh.js"></script>
   ```
3. 编辑 `<Strata>\serve\web\monitor.html`，在 `<script defer src="/web/monitor.js"></script>` 下面加一行：
   ```html
   <script defer src="/web/i18n-zh.js"></script>
   ```
4. 刷新页面（**Ctrl+F5**）

## 使用

顶栏左上角 **Language** 按钮 → 选 `英文` / `简体中文` / `中英文`。选择记在浏览器里（`localStorage` 的 `strata.lang`），下次打开还是它。

## 升级 Strata 时（重要）

官方的 “UPDATE.bat” 用 “git pull” 更新，**页面被改过会让它失败**。所以请按这个顺序：

1. **先卸载**：双击 `uninstall-zh.bat`
2. **再更新**：运行官方的 `UPDATE.bat`（或 `START-HERE.bat --update`）
3. **后装回**：双击 `install-zh.bat`

这样永远不会和官方更新打架。

## 检查状态 / 卸载

```bat
python apply_zh_ui.py --check  "D:\Strata"     :: 看装没装
uninstall-zh.bat                                :: 卸载并还原英文界面
```

安装器改页面之前会存一份 `.zhbak` 备份；确认没问题后可以自行删掉。

## 包里有什么

| 文件 | 作用 |
|---|---|
| `i18n-zh.js` | 汉化层本体（约 40 KB，独立文件） |
| `apply_zh_ui.py` | 安装 / 卸载 / 检查 |
| `install-zh.bat` · `uninstall-zh.bat` | Windows 一键入口 |
| `LICENSE` · `NOTICE.md` | 许可与致谢 |

**没有**：Strata 源码、引擎可执行文件、模型权重。

## 许可与致谢

- 本包 **MIT License**，保留了原作者的版权声明 —— 见 [LICENSE](LICENSE)
- **感谢 [Niko1221](https://github.com/Niko1221/Strata) 与 Strata 贡献者**做出这个项目
- 模型权重不在本包内；Qwen3.8-Flash-Next 适用 **Qwen Community License 1.0**（非 MIT），详见 [NOTICE.md](NOTICE.md)
- 本包为**非官方**作品，与 Strata 项目无隶属或背书关系

## 上游 PR

这套汉化已经提给官方：[Niko1221/Strata#1836](https://github.com/Niko1221/Strata/pull/1836)。它是在官方 0.2.0-beta 的 **追踪器重置** 中被统一关闭的，**不是拒绝** —— 维护者说明：超过 1300 个未处理 issue/PR，暂时关闭所有没人正在推进的条目，并给出 4 步重新打开的办法（rebase 到 main、标题加 `[GUI]`/`[Other]` 前缀、填 PR 模板里的问题/结果/验证、评论 `/reopen`）。本包会继续跟官方版本更新，0.2.0-beta 已适配。

---

## English (short)

An **unofficial Chinese localisation pack** for the [Strata](https://github.com/Niko1221/Strata) web interface (MIT). Adds a `Language` button with **English / Simplified Chinese / Chinese + English**. The model's own output — chat text, reasoning, code, tool calls — is never rewritten. Install with `install-zh.bat` (or copy `i18n-zh.js` into `serve/web/` and add one `<script>` tag to each of the two HTML pages). Uninstall before running the official `UPDATE.bat`, then install again.

Contains no Strata source, no engine binaries and **no model weights**. Upstream PR: [#1836](https://github.com/Niko1221/Strata/pull/1836).
