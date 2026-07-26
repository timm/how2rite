#!/usr/bin/env python3
"""One sentence per line for the paper's tex files.

Joins each prose paragraph into one string (collapsing
runs of blanks), breaks it at sentence ends, then wraps
any sentence longer than WIDTH (default 70) at word
boundaries, so hand-wrapped edits renormalize to the
repo's sentence-per-line rule. Verbatim-like
environments, comment lines, and structural lines pass
through untouched. Idempotent. Usage: make fmt, or
python3 fmt.py [-w N] file.tex...
"""

import re
import sys
import textwrap

WIDTH = 70

PROTECT = ("verbatim", "BVerbatim", "lstlisting", "tabular")
PASS = ("\\begin", "\\end", "\\section", "\\subsection",
        "\\label", "\\caption", "\\centering", "\\input",
        "\\maketitle", "\\bibliography", "\\title", "%")
ABBREV = re.compile(
    r"\b(e\.g|i\.e|cf|vs|etc|al|Fig|Sec|Tab|Eq|Dr|Prof|St|No|"
    r"[A-Z])\.$")


def sentences(par):
    "Split a joined paragraph at full stops (also ! ?)."
    words, out, buf = par.split(), [], []
    for i, w in enumerate(words):
        buf.append(w)
        core = w.rstrip(")'\"}]")
        nxt = words[i + 1] if i + 1 < len(words) else ""
        if (re.search(r"[.!?]$", core)
                and not ABBREV.search(core)
                and (not nxt or nxt[0].isupper()
                     or nxt[0] in "\\(`$")):
            out.append(" ".join(buf))
            buf = []
    if buf:
        out.append(" ".join(buf))
    return out


def fmt(text):
    out, par, depth = [], [], 0

    def flush():
        if par:
            for s in sentences(" ".join(par)):
                out.extend(textwrap.wrap(
                    s, WIDTH, break_long_words=False,
                    break_on_hyphens=False) or [s])
            par.clear()

    for line in text.splitlines():
        s = line.strip()
        opened = re.match(r"\\begin\{(\w+)\**\}", s)
        if opened and opened.group(1) in PROTECT:
            flush()
            depth += 1
            out.append(line)
            continue
        closed = re.match(r"\\end\{(\w+)\**\}", s)
        if closed and closed.group(1) in PROTECT:
            depth -= 1
            out.append(line)
            continue
        if depth > 0:
            out.append(line)
        elif not s:
            flush()
            out.append("")
        elif s.startswith(PASS):
            flush()
            out.append(line)
        else:
            par.append(s)
    flush()
    return "\n".join(out) + "\n"


if __name__ == "__main__":
    args = sys.argv[1:]
    if args[:1] == ["-w"]:
        WIDTH = int(args[1])
        args = args[2:]
    for path in args:
        old = open(path).read()
        new = fmt(old)
        if new != old:
            open(path, "w").write(new)
            print(f"fmt: {path}")
