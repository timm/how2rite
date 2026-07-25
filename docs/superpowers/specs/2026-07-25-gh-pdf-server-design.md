# GitHub as PDF server for how2rite

Date: 2026-07-25. Approved by timm.

## Goal

Push to main rebuilds `paper1.pdf` with tectonic and serves it at a
stable URL: `https://timm.github.io/how2rite/paper1.pdf`. PDF leaves
git; CI copy is the served truth.

## Design

- `.github/workflows/pdf.yml`: on push to main (paths: `**.tex`,
  `refs.bib`, the workflow file), on PRs touching same paths, and
  manual dispatch.
- Build: `wtfjoke/setup-tectonic` (binary install, seconds) +
  `actions/cache` on `~/.cache/Tectonic` (tectonic auto-downloads
  only needed packages; cache keyed on tex/bib hash). Then
  `tectonic paper1.tex`. Matches local `make` exactly.
- Serve: on main only, stage `paper1.pdf` + one-line `index.html`
  redirect into `_site/`, `actions/upload-pages-artifact`,
  `actions/deploy-pages`. No gh-pages branch.
- PRs: build only, PDF as plain workflow artifact. Broken TeX fails CI.
- Hygiene: `git rm --cached paper1.pdf`; add to `.gitignore`.
- One-time: enable Pages with source "GitHub Actions" via `gh api`.

## Rejected

- `xu-cheng/latex-action` full TeXLive docker: ~GB image, slow, not
  tectonic.
- `peaceiris/actions-gh-pages` branch push: extra branch, history churn.
- Committing built PDF to main: bot commits, merge pain at N>1.

## Deferred

- latexdiff-vc PDF on PRs (add when co-authors arrive).
- `sec/` multi-file split, one sentence per line, agent file-ownership
  table (same trigger).
