include .dot/Makefile
# vim: ts=8 noexpandtab :

%.pdf: %.tex sec/*.tex sec0/*.tex refs.bib ## build any paper: pdf in tmp/, temporaries in .aux/
	@mkdir -p tmp .aux
	tectonic --keep-intermediates -o .aux $<
	@mv .aux/$*.pdf tmp/$*.pdf
	@echo $* > .aux/.last

fast: ## recompile last-built paper, one pass, no bib update
	@t=$$(cat .aux/.last 2>/dev/null || echo paper3); \
	  echo "fast: $$t.tex"; \
	  tectonic --keep-intermediates -r 0 -o .aux $$t.tex; \
	  mv .aux/$$t.pdf tmp/$$t.pdf

focus: ## regenerate fig/focus_grid.png (repgrid, sec0/know)
	@python3 focus.py

lit: ## regenerate sec 5 figures/table/numbers (litfig.py)
	@python3 litfig.py

statsfig: ## regenerate fig/stats_*.pdf + stats_grid.tex (appendix)
	@python3 statsfig.py

notes: ## list open review comments
	@grep -n '^[^%]*\\note{' paper1.tex sec/*.tex || echo "none"

fmt: ## rewrap sec/*.tex to one sentence per line
	@python3 fmt.py sec/*.tex

# overrides .dot push (the "overriding recipe" warning is expected):
# tex + figures land in overleaf; overleaf compiles the pdf itself
push: ## commit all (MSG=...), push github (CI pdf) + overleaf
	@$(MK) dot
	@git add -A
	@git diff-index --quiet HEAD -- || git commit -qm "$(MSG)"
	@git pull -q --no-edit overleaf main
	@git push -q -u origin HEAD
	@git push -q overleaf main
