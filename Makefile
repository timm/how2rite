# vim: ts=8 noexpandtab :
SHELL := /bin/bash
.DEFAULT_GOAL := help

help: ## show targets
	@grep -hE '^[a-z0-9.-]+:.*## ' Makefile | \
	  awk -F':.*## ' '{printf "  \033[36m%-12s\033[0m %s\n", $$1, $$2}'

%.pdf: %.tex sec/*.tex sec0/*.tex refs.bib ## build any paper: pdf in build/, temporaries in tmp/
	@mkdir -p build tmp
	tectonic --keep-intermediates -o tmp $<
	@mv tmp/$*.pdf build/$*.pdf
	@echo $* > tmp/.last

fast: ## recompile last-built paper, one pass, no bib update
	@t=$$(cat tmp/.last 2>/dev/null || echo paper1); \
	  echo "fast: $$t.tex"; \
	  tectonic --keep-intermediates -r 0 -o tmp $$t.tex; \
	  mv tmp/$$t.pdf build/$$t.pdf

notes: ## list open review comments
	@grep -n '^[^%]*\\note{' paper1.tex sec/*.tex || echo "none"

fmt: ## rewrap sec/*.tex to one sentence per line
	@python3 fmt.py sec/*.tex

push: ## add+commit+push+status (CI rebuilds + serves pdf)
	@git add -A
	@printf "msg (empty=save): "; read m </dev/tty; git commit -m "$${m:-save}" || true
	@git push
	@git status
