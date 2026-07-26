# vim: ts=8 noexpandtab :
SHELL := /bin/bash
.DEFAULT_GOAL := help

help: ## show targets
	@grep -hE '^[a-z0-9.-]+:.*## ' Makefile | \
	  awk -F':.*## ' '{printf "  \033[36m%-12s\033[0m %s\n", $$1, $$2}'

paper1.pdf: paper1.tex sec/*.tex refs.bib ## build pdf with tectonic
	tectonic paper1.tex

fmt: ## rewrap sec/*.tex to one sentence per line
	@python3 fmt.py sec/*.tex

push: ## add+commit+push+status (CI rebuilds + serves pdf)
	@git add -A
	@printf "msg (empty=save): "; read m </dev/tty; git commit -m "$${m:-save}" || true
	@git push
	@git status
