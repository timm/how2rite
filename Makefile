include .dot/Makefile
# vim: ts=8 noexpandtab :

%.pdf: %.tex sec/*.tex sec0/*.tex refs.bib ## build any paper: pdf in tmp/, temporaries in .aux/
	@mkdir -p tmp .aux
	tectonic --keep-intermediates -o .aux $<
	@mv .aux/$*.pdf tmp/$*.pdf
	@echo $* > .aux/.last

fast: ## recompile last-built paper, one pass, no bib update
	@t=$$(cat .aux/.last 2>/dev/null || echo paper1); \
	  echo "fast: $$t.tex"; \
	  tectonic --keep-intermediates -r 0 -o .aux $$t.tex; \
	  mv .aux/$$t.pdf tmp/$$t.pdf

focus: ## regenerate fig/focus_grid.png (repgrid, sec0/know)
	@python3 focus.py

lit: ## regenerate sec 5 figures/table/numbers (litfig.py)
	@python3 litfig.py

notes: ## list open review comments
	@grep -n '^[^%]*\\note{' paper1.tex sec/*.tex || echo "none"

fmt: ## rewrap sec/*.tex to one sentence per line
	@python3 fmt.py sec/*.tex
