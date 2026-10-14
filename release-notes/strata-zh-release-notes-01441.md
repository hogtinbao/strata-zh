**非官方**中文语言包，适配 **Strata v0.1.44.1**（0.1.40.x 起均可）。

> **这一版有实质更新**：官方 0.1.44 新增了**图片生成页**（`Images` 标签页），本包补上了它的全文案 —— 标题「生成图片」、提示词输入框、尺寸 / 种子、生成按钮、提示语，以及结果区的三条状态文案。共新增 9 条译文。
>
> 该标签页仅在服务端声明支持图片生成时才会显示（`health.image_generation`）；不支持时标签隐藏，但译文已就位。

## 安装

下载下面的 zip → 解压 → 双击 **`install-zh.bat`** → 浏览器 **Ctrl+F5**。

自动找不到 Strata 时，把路径传给它：

```bat
install-zh.bat "D:\Strata"
```

## 效果

- 顶栏左上角 **Language** 按钮：**英文 / 简体中文 / 中英文**
- **模型输出永不翻译** —— 聊天正文、思考过程、代码块、工具调用参数与结果原样保留
- 覆盖 0.1.44.1 界面全部用户可见文案，含图片生成页、模型设置页 15 个配置键的中文注释（`sampling.top_p（核采样范围）`…）
- 切换回 `English` 完全还原原版界面

## 包含 / 不包含

| 包含 | 不包含 |
|---|---|
| `i18n-zh.js`（汉化层，独立文件） | Strata 源码 |
| `apply_zh_ui.py`（安装/卸载/检查） | 引擎二进制 |
| `install-zh.bat` · `uninstall-zh.bat` | **模型权重** |
| `README.md` · `NOTICE.md` · `LICENSE` | |

安装器改页面之前会存 `.zhbak` 备份，卸载可逐字节还原（LF / CRLF 两种换行符都验证过）。

## 升级 Strata 时（重要）

官方 `UPDATE.bat` 用 `git pull`，页面被改过会让它失败。顺序是：

1. `uninstall-zh.bat` 卸载
2. 运行官方 `UPDATE.bat`
3. `install-zh.bat` 装回

（如果新版本没有改动 `serve/web/`，第 1、3 步可以省略 —— 挂载点会自动保留。0.1.43 与 0.1.43.1 就属于这种情况；**0.1.44 改了网页，必须走完整三步**。）

## 许可与致谢

**MIT License**，保留原作者版权声明。感谢 [Niko1221](https://github.com/Niko1221/Strata) 与 Strata 贡献者。

模型权重不在本包内；Qwen3.8-Flash-Next 适用 **Qwen Community License 1.0**（非 MIT），详见 `NOTICE.md`。

本包为**非官方**作品，与 Strata 项目无隶属或背书关系。

上游 PR：[Niko1221/Strata#1836](https://github.com/Niko1221/Strata/pull/1836)

---

*Unofficial Chinese localisation pack for the [Strata](https://github.com/Niko1221/Strata) web interface (MIT). Adds a `Language` button with English / Simplified Chinese / Chinese + English. The model's output is never rewritten. Contains no Strata source, no engine binaries and no model weights.*
