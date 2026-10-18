**非官方**中文语言包，适配 **Strata v0.1.45**（0.1.40.x 起均可）。

> **这一版是跟版更新**：官方 0.1.45 没有新增界面文案，改的是**网页采样默认值逻辑** —— 页面在用户没动过采样时不再自己发 `temperature: 0.6`，而是交给服务端按模型卡的档位取值（思考 1.0 / top_p 0.95 / top_k 20；不思考 0.7 / 0.8 / 20 并带 presence penalty）。界面文案只有两处变动，本包都已同步：
>
> 1. 模型设置页 `sampling.temperature` 的说明句被改写成模型卡档位，新译文：「请求未指定时的默认温度（0 = 贪心；不设置则用模型卡的值：思考 1.0，不思考 0.7）」（旧句译文保留，兼容 0.1.44.1 及更早）
> 2. 监控页新增一条只在 **Apple Silicon** 上出现的 GPU 读数说明（非 root 读不到温度与功耗、GPU 与 CPU 同芯片所以没有 PCIe 链路可显示），已收进词典
>
> 共新增 2 条译文，词典总量 695 行。

## 安装

下载下面的 zip → 解压 → 双击 **`install-zh.bat`** → 浏览器 **Ctrl+F5**。

自动找不到 Strata 时，把路径传给它：

```bat
install-zh.bat "D:\Strata"
```

## 效果

- 顶栏左上角 **Language** 按钮：**英文 / 简体中文 / 中英文**
- **模型输出永不翻译** —— 聊天正文、思考过程、代码块、工具调用参数与结果原样保留
- 覆盖 0.1.45 界面全部用户可见文案，含图片生成页、模型设置页 15 个配置键的中文注释（`sampling.top_p（核采样范围）`…）
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

（**0.1.45 改了 `serve/web/app.js`，必须走完整三步**；如果只更新引擎不改网页，第 1、3 步可省略 —— 挂载点会自动保留。）

## 许可与致谢

**MIT License**，保留原作者版权声明。感谢 [Niko1221](https://github.com/Niko1221/Strata) 与 Strata 贡献者。

模型权重不在本包内；Qwen3.8-Flash-Next 适用 **Qwen Community License 1.0**（非 MIT），详见 `NOTICE.md`。

本包为**非官方**作品，与 Strata 项目无隶属或背书关系。

上游 PR：[Niko1221/Strata#1836](https://github.com/Niko1221/Strata/pull/1836)

---

*Unofficial Chinese localisation pack for the [Strata](https://github.com/Niko1221/Strata) web interface (MIT). Adds a `Language` button with English / Simplified Chinese / Chinese + English. The model's output is never rewritten. Contains no Strata source, no engine binaries and no model weights.*
