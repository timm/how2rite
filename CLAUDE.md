# CLAUDE.md

Workdir for one paper: a meta-paper that explains the
rite method and applies it to itself. The engine is the
read-only repo github.com/timm/rite, cloned at
~/gits/timm/rite: read its CLAUDE.md and HOWTO.md
first; never edit it from here.

This dir owns: README.md (goal: and years: lines -- the
search SSOT), flags.py (coding vocabulary SSOT),
bench.md (field benchmark norms), TODO.md (the standing
work order for the meta-paper), lit/ (generated + hand
notes; see lit/EXHIBIT.md for what is already there).

Run pipeline scripts from this dir, e.g.:

    python3 ~/gits/timm/rite/etc/fetch.py

Keep intermediaries few: README, paper1, critic
reports, paper2 (see TODO.md).

## Paper layout

paper1.tex is a thin root (preamble + \input); prose
lives in sec/*.tex, one sentence per line. Edit a
sentence, touch one line; never reflow a paragraph.
CI rebuilds on push to main with tectonic and serves
https://timm.github.io/how2rite/paper1.pdf; PRs build
only. paper1.pdf is generated, never committed.

## Collaboration rules

Agents: branch + PR only, never push main. Prose edits
in sec/ only; preamble, root .tex, Makefile, or
workflow changes need a human. refs.bib: one entry per
commit, keep sorted.

Ownership (extend as authors join):

| file        | owner |
|-------------|-------|
| sec/*.tex   | timm  |
| paper1.tex  | timm  |
| refs.bib    | timm  |
