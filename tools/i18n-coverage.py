#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""i18n-zh.js 覆盖率自查（两种模式）

模式 1 —— 全量：把一份 serve/ 里的界面文案抽出来，对照词典 + 规则。
    python i18n-coverage.py full <serve 目录> [i18n-zh.js]

模式 2 —— 增量（推荐，噪声小）：只看两次适配之间上游“新增/改动”的英文文案。
    python i18n-coverage.py diff <git 仓库> <旧 commit> <新 commit> [i18n-zh.js]

判定：命中 i18n-zh.js 的词典、选项表，或任一条正则规则，即算已覆盖。
"""
import re
import subprocess
import sys
from pathlib import Path

UI_PATHS = ["serve/web", "serve/runconfig.py", "serve/telemetry.py", "serve/frontend.py"]

ENTITY = {"&amp;": "&", "&lt;": "<", "&gt;": ">", "&quot;": '"', "&#39;": "'",
          "&hellip;": "…", "&nbsp;": " ", "&times;": "×", "&middot;": "·",
          "&mdash;": "—", "&ndash;": "–", "&rarr;": "→"}

JUNK = re.compile(
    r"^(?:[a-z0-9_-]+|#[A-Za-z0-9_-]+|\.[A-Za-z0-9_-]+|/[^ ]*|https?://\S*|"
    r"[a-z]+\.[a-z]+|data-[a-z-]+|aria-[a-z-]+|[A-Za-z]+-[a-z-]+|"
    r"Bearer|application/json|text/[a-z]+|[0-9.]+(?:px|s|ms|%|em|rem|fr|k|K|M|G)?|"
    r"[A-Za-z0-9_.\-]*\$\{|TOP|GET|POST|[A-Z_]{3,})$"
)
HAS_WORD = re.compile(r"[A-Za-z]{2,}")


def norm(s: str) -> str:
    s = " ".join(s.split())
    for k, v in ENTITY.items():
        s = s.replace(k, v)
    return s


def load_zh(js_path: Path):
    text = js_path.read_text(encoding="utf-8")
    keys = set()
    for marker in ("const ZH = {", "const KEY_GLOSS = {", "const OPTION_ZH = {",
                   "const GLOSS = {", "const KEY_ZH = {"):
        idx = text.find(marker)
        if idx < 0:
            continue
        body = text[idx: text.find("\n  };", idx)]
        for line in body.splitlines():
            m = re.match(r'\s*"((?:[^"\\]|\\.)*)"\s*:', line)
            if m:
                keys.add(norm(m.group(1)))
    rules = []
    idx = text.find("const RULES = [")
    if idx >= 0:
        body = text[idx: text.find("\n  ];", idx)]
        for m in re.finditer(r"(?<![\w/])/((?:[^/\\\n]|\\.)+)/([gimsuy]*)", body):
            try:
                rules.append(re.compile(m.group(1)))
            except re.error:
                pass
    return keys, rules


QSTR = re.compile(r'"((?:[^"\\\n]|\\.){2,})"|\'((?:[^\'\\\n]|\\.){2,})\'')
TSTR = re.compile(r"`((?:[^`\\\n]|\\.){2,})`")


def looks_human(t: str) -> bool:
    if not HAS_WORD.search(t):
        return False
    if JUNK.match(t):
        return False
    if t.startswith(("http", "//", "/")):
        return False
    if " " not in t and not (t[0].isupper() or t.endswith(("…", ".", "!", "?", ":"))):
        return False
    if t.count("{") and t.count("}") and t.count("${") != t.count("{"):
        return False
    return True


def strings_in_code(line: str):
    out = []
    for m in QSTR.finditer(line):
        s = m.group(1) or m.group(2)
        if "\\" in s:
            continue
        out.append(norm(s))
    for m in TSTR.finditer(line):
        s = m.group(1)
        if "${" in s or "\\" in s:
            continue
        out.append(norm(s))
    return out


def html_candidates(raw: str):
    out = []
    body = re.sub(r"<(script|style)\b.*?</\1>", " ", raw, flags=re.S | re.I)
    for chunk in body.split("<"):
        t = norm(re.sub(r"<[^>]*>", "", "<" + chunk))
        if t and HAS_WORD.search(t):
            out.append(t)
    for m in re.finditer(r'\b(title|placeholder|aria-label)\s*=\s*"([^"]*)"', raw):
        t = norm(m.group(2))
        if t and HAS_WORD.search(t):
            out.append(t)
    return out


def runconfig_help(raw: str):
    idx = raw.find("EDITABLE = [")
    if idx < 0:
        return []
    body = raw[idx: raw.find("\n]", idx)]
    out = []
    for m in re.finditer(r'\("([a-z_0-9]+)",[^,]+,\s*((?:"(?:[^"\\]|\\.)*"\s*)+)\)', body, re.S):
        parts = re.findall(r'"((?:[^"\\]|\\.)*)"', m.group(2))
        out.append((m.group(1), norm("".join(parts))))
    return out


def report(pairs, keys, rules):
    seen, missing = set(), []
    for kind, s in pairs:
        if not s or s in seen:
            continue
        seen.add(s)
        if s in keys or any(r.search(s) for r in rules):
            continue
        missing.append((kind, s))
    return len(seen), missing


def mode_full(serve: Path, zh: Path):
    keys, rules = load_zh(zh)
    web = serve / "web"
    pairs = []
    for f in ("index.html", "monitor.html"):
        p = web / f
        if p.exists():
            pairs += [(f, s) for s in html_candidates(p.read_text(encoding="utf-8"))]
    for f in ("app.js", "monitor.js"):
        p = web / f
        if p.exists():
            raw = re.sub(r"/\*.*?\*/", " ", p.read_text(encoding="utf-8"), flags=re.S)
            for line in raw.splitlines():
                for s in strings_in_code(line):
                    if looks_human(s):
                        pairs.append((f, s))
    rc = serve / "runconfig.py"
    if rc.exists():
        pairs += [("runconfig.py:" + k, s) for k, s in runconfig_help(rc.read_text(encoding="utf-8"))]
    total, missing = report(pairs, keys, rules)
    print("候选 %d，未命中 %d" % (total, len(missing)))
    for kind, s in missing:
        print("  [%s] %s" % (kind, s))


def _added(diff: str):
    fname = "?"
    for line in diff.splitlines():
        if line.startswith("+++ b/"):
            fname = line[6:]
        elif line.startswith("+") and not line.startswith("+++"):
            yield fname, line


def _added_files(diff: str):
    fname, buf = None, []
    for line in diff.splitlines():
        if line.startswith("+++ b/"):
            if fname:
                yield fname, "\n".join(buf)
            fname, buf = line[6:], []
        elif line.startswith("+") and not line.startswith("+++") and fname:
            buf.append(line[1:])
    if fname:
        yield fname, "\n".join(buf)


def mode_diff(repo: str, old: str, new: str, zh: Path):
    keys, rules = load_zh(zh)
    diff = subprocess.run(["git", "-C", repo, "diff", "--no-color", old + ".." + new, "--"] + UI_PATHS,
                          capture_output=True, text=True, encoding="utf-8", errors="replace").stdout
    pairs = []
    for fname, line in _added(diff):
        s = line[1:].strip()
        if fname.endswith(".html"):
            pairs += [(fname, x) for x in html_candidates(s)]
        for x in strings_in_code(s):
            if looks_human(x):
                pairs.append((fname, x))
    for fname, raw in _added_files(diff):
        if fname.endswith("runconfig.py"):
            pairs += [("runconfig.py:" + k, s) for k, s in runconfig_help(raw)]
    total, missing = report(pairs, keys, rules)
    print("增量候选 %d，未命中 %d" % (total, len(missing)))
    for kind, s in missing:
        print("  [%s] %s" % (kind, s))


def main():
    if len(sys.argv) < 3:
        print(__doc__)
        return 1
    mode = sys.argv[1]
    here = Path(__file__).resolve().parent / "i18n-zh.js"
    if mode == "full":
        serve = Path(sys.argv[2]).resolve()
        zh = Path(sys.argv[3]).resolve() if len(sys.argv) > 3 else here
        mode_full(serve, zh)
    elif mode == "diff":
        repo, old, new = sys.argv[2], sys.argv[3], sys.argv[4]
        zh = Path(sys.argv[5]).resolve() if len(sys.argv) > 5 else here
        mode_diff(repo, old, new, zh)
    else:
        print(__doc__)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
