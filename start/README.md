# Start here

How to join the writing on this paper. Pick the rung of
the ladder that matches your comfort zone; every rung is a
full member of the team. Whatever rung you pick, the rule
is the same: comments go in the text as `\note{yourname}{...}`
and are resolved by deleting them (`make notes` lists what
is open).

## The ladder

**Rung 0: reader.** Watch the built PDF at
https://timm.github.io/how2rite/paper1.pdf and send
comments by mail or chat. Zero setup.

**Rung 1: Google Docs + claude.ai.** Draft and comment in
the shared Google Doc (link supplied per session). Use
claude.ai in the browser for drafting help. A git-side
person moves accepted text into the repo. Setup: a Google
account.

**Rung 2: Overleaf in the browser.** Edit the LaTeX (and
these markdown files) live at the shared Overleaf project;
see the PDF re-render as you type. No install, real-time
co-editing. Setup: an Overleaf account plus a project
invite (ask timm).

**Rung 3: GitHub.** Clone github.com/timm/how2rite, edit,
push (or edit files directly on github.com in the
browser). Branch + PR if you are unsure; straight to main
if you are not. Setup: a GitHub account with write access
(ask timm).

**Rung 4: Claude Code + the git bridge.** Run Claude Code
on your own machine in your clone. Two remotes: `origin`
(GitHub, source of truth) and `overleaf`
(https://git.overleaf.com/<project-id>, the live view).
Cycle: pull overleaf, edit, push overleaf, push origin.
Setup: rung 3 plus an Overleaf git token (Account
Settings, Git Integration; needs the project invite
first).

## How to edit the LaTeX (all rungs that touch .tex)

Two habits keep n people from treading on each other:

1. **Every "." starts a new line.** One sentence per line,
   wrapped at 70 characters. Git then diffs and merges by
   the sentence, so two people editing the same section
   rarely collide, and review comments land on exactly one
   sentence. Do not hand-reflow paragraphs; rungs 3-4 run
   `make fmt`, which renormalizes everything. Browser
   editors: just start a fresh line after each sentence
   and let fmt tidy the rest later.

2. **Content lives in lots of small files.** The root
   files (`paper1.tex`, `paper0.tex`) are thin: preamble
   plus `\input` lines, nothing else. Prose goes in one
   file per section (`sec/intro.tex`, `sec0/intro.tex`,
   ...). Small files mean two writers rarely open the same
   file at all; claim a section, not the paper.

## Before any writing session

The session owner checks, the day before, that every
participant can already write to something:

1. Each person has named their rung.
2. Rung 1 people have the Doc link and edit rights.
3. Rung 2 people are invited to the Overleaf project and
   have opened it once.
4. Rung 3/4 people have push access and have pushed one
   trivial commit.
5. The Overleaf main document is set and compiles.
6. One person is named sync captain: they run the
   pull/push cycle between Overleaf and GitHub during the
   session, and paste rung-1 text into the repo.

Solving access problems during the session wastes
everyone's hour. Solve them before.

## House rules (all rungs)

- Prose files: one sentence per line, wrapped at 70; run
  `make fmt` after hand edits (rungs 3-4).
- Comments: `\note{who}{what}` in tex; resolve = delete.
- refs.bib: one entry per commit; real bibliographic data
  only.
- Prompts we use live in `start/prompts/`; see its README.
