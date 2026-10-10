# -*- coding: utf-8 -*-
"""Strata中文版 — 界面汉化安装器

用法（放在哪都行）：
    python apply_zh_ui.py                   自动寻找 Strata 安装目录
    python apply_zh_ui.py "D:\\Strata"       指定目录
    python apply_zh_ui.py --check           只检查状态
    python apply_zh_ui.py --remove          卸载汉化

它只做三件事：
  1) 把 i18n-zh.js 复制到 <Strata>\\serve\\web\\
  2) 在 index.html / monitor.html 里补上对它的 <script> 引用（缺了才补）
  3) 卸载时反向操作，并还原被改过的页面

不改动 Strata 的任何其它文件；改页面之前会存 .zhbak 备份。
"""
from __future__ import annotations

import sys
from pathlib import Path

try:                                    # Windows 控制台按 UTF-8 输出，避免乱码
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass

HERE = Path(__file__).resolve().parent
LANG_SRC = HERE / "i18n-zh.js"
LANG_NAME = "i18n-zh.js"
WEB_SUB = Path("serve") / "web"

# 页面 -> (锚点行, 要插入的引用行)  锚点是官方页面里原有的 script 标签
TARGETS = {
    "index.html": ('<script src="web/app.js"></script>',
                   '<script src="web/i18n-zh.js"></script>'),
    "monitor.html": ('<script defer src="/web/monitor.js"></script>',
                     '<script defer src="/web/i18n-zh.js"></script>'),
}


def say(msg: str = "") -> None:
    print(msg)


def read_raw(p: Path) -> str:
    """原样读：不做换行符转换。"""
    with open(p, "r", encoding="utf-8", newline="") as f:
        return f.read()


def write_raw(p: Path, s: str) -> None:
    """原样写：不做换行符转换。"""
    with open(p, "w", encoding="utf-8", newline="") as f:
        f.write(s)


def is_strata(p: Path) -> bool:
    """判断一个目录是不是 Strata 安装目录（有 serve/web/index.html 就算）。"""
    try:
        return (p / WEB_SUB / "index.html").is_file()
    except OSError:
        return False


def find_root(explicit: str | None = None) -> Path | None:
    if explicit:
        p = Path(explicit).expanduser()
        return p.resolve() if is_strata(p) else None
    cwd = Path.cwd()
    cands: list[Path] = [cwd, *cwd.parents, Path.home() / "Strata"]
    for drive in ("C:", "D:", "E:", "F:", "G:"):
        for name in ("Strata", "strata", "StrataData"):
            cands.append(Path(f"{drive}/{name}"))
    for c in cands:
        if is_strata(c):
            return c.resolve()
    return None


def status(root: Path) -> dict[str, bool]:
    out: dict[str, bool] = {}
    out["file"] = (root / WEB_SUB / LANG_NAME).is_file()
    for name in TARGETS:
        page = root / WEB_SUB / name
        out[name] = page.is_file() and LANG_NAME in page.read_text(encoding="utf-8")
    return out


def install(root: Path) -> int:
    web = root / WEB_SUB
    if not LANG_SRC.is_file():
        say(f"找不到语言文件 {LANG_SRC}，请把本目录下的文件放在一起。")
        return 1

    dst = web / LANG_NAME
    same = dst.is_file() and dst.read_bytes() == LANG_SRC.read_bytes()
    if not same:
        dst.write_bytes(LANG_SRC.read_bytes())
        say(f"已写入语言文件：{dst}")
    else:
        say(f"语言文件已是最新：{dst}")

    changed = 0
    for name, (anchor, tag) in TARGETS.items():
        page = web / name
        if not page.is_file():
            say(f"跳过（文件不存在）：{name}")
            continue
        text = read_raw(page)
        if LANG_NAME in text:
            say(f"已挂载，无需处理：{name}")
            continue
        backup = page.with_suffix(page.suffix + ".zhbak")
        if not backup.exists():
            write_raw(backup, text)
        eol = "\r\n" if "\r\n" in text else "\n"      # 沿用该文件自己的换行符
        if anchor in text:
            text = text.replace(anchor, anchor + eol + tag, 1)
        elif "</body>" in text:
            text = text.replace("</body>", tag + eol + "</body>", 1)
        else:
            say(f"无法处理（找不到插入点）：{name}")
            continue
        write_raw(page, text)
        say(f"已挂载：{name}")
        changed += 1

    say()
    say("完成。请刷新浏览器页面（Ctrl+F5），然后点顶栏左侧的 Language 按钮切换语言。")
    return 0


def remove(root: Path) -> int:
    web = root / WEB_SUB
    n = 0
    for name in TARGETS:
        page = web / name
        if not page.is_file():
            continue
        text = read_raw(page)
        if LANG_NAME not in text:
            say(f"未挂载，跳过：{name}")
            continue
        lines = [ln for ln in text.splitlines(keepends=True) if LANG_NAME not in ln]
        write_raw(page, "".join(lines))
        say(f"已还原页面：{name}")
        n += 1
    dst = web / LANG_NAME
    if dst.is_file():
        dst.unlink()
        say(f"已删除语言文件：{dst}")
        n += 1
    say()
    say("卸载完成，界面已还原为原版英文。" if n else "本来就没有装，无需卸载。")
    return 0


def main(argv: list[str]) -> int:
    args = [a for a in argv[1:] if not a.startswith("--")]
    flags = {a for a in argv[1:] if a.startswith("--")}
    root = find_root(args[0] if args else None)

    if root is None:
        say("没有找到 Strata 安装目录。")
        say("请把 Strata 的路径作为参数传进来，例如：")
        say('    python apply_zh_ui.py "D:\\Strata"')
        return 1

    say(f"Strata 目录：{root}")
    say()

    if "--check" in flags:
        st = status(root)
        say(f"  语言文件：{'已安装' if st['file'] else '未安装'}")
        for name in TARGETS:
            say(f"  {name}：{'已挂载' if st[name] else '未挂载'}")
        return 0

    if "--remove" in flags:
        return remove(root)

    return install(root)


if __name__ == "__main__":
    sys.exit(main(sys.argv))
