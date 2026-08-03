# CLAUDE.md

Workdir for one paper: a meta-paper that explains the
rite method and applies it to itself. The engine is the
read-only repo github.com/timm/rite, cloned at
~/gits/timm/rite: read its CLAUDE.md and HOWTO.md
first; never edit it from here.

This dir owns: README.md (goal:, years:, and optional
seed: lines -- the search SSOT), flags.py (coding
vocabulary SSOT),
bench.md (field benchmark norms), TODO.md (the standing
work order for the meta-paper), lit/ (generated + hand
notes; see lit/EXHIBIT.md for what is already there).

Run pipeline scripts from this dir, e.g.:

    python3 ~/gits/timm/rite/etc/fetch.py

Keep intermediaries few: README, paper1, critic
reports, paper2 (see TODO.md).

## Paper layout

paper3.tex is the working meta-paper (formerly
paper0); it is a thin root (preamble + \input) reading
sec0/. Retired roots live in old/ (paper0, paper1, the
ASD-STE100 paper2). Prose is one sentence per line,
wrapped at 70 (run `make fmt` after hand edits; it
renormalizes). CI builds paper3 and serves it at
timm.github.io/how2rite/paper3.pdf.

## Prose style

Professional register. Never open a sentence with a
coordinating conjunction (And, But, So, Or) or a
relative fragment (Which is...). No sentence
fragments in paper prose. Prefer: therefore, however,
hence, yet-with-comma.
CI rebuilds on push to main with tectonic and serves
https://timm.github.io/how2rite/paperN.pdf; PRs build
only. Paper PDFs are generated, never committed.

## Collaboration rules

Agents: branch + PR only, never push main. Prose edits
in sec/ only; preamble, root .tex, Makefile, or
workflow changes need a human. refs.bib: one entry per
commit, keep sorted.

Ownership (extend as authors join):

| file        | owner |
|-------------|-------|
| sec0/*.tex  | timm  |
| paper3.tex  | timm  |
| refs.bib    | timm  |
