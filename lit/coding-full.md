# Abstract vs full-text coding

A group like SExMOxBM is an AND: that exact set of
flags fired, no others. Each paper appears in exactly
one group row.

Columns: abs = fired in title+abstract; full-bin =
any single match anywhere in the full text; full-thr
= fired at >=0.5 matches per 1000 words of full text.

Length-normalised term frequency is standard IR
practice (Salton & Buckley 1988); the 0.5 cutoff
itself is ours, not from the literature. Before any
of these numbers reach a paper, sensitivity-check the
cutoff (vary it; show the group table is stable).

0 PDFs with usable text.

## Per-flag agreement, abstract vs full text
(binary = any match; thr = >=0.5 per 1k words)

| flag | abs=y | full-bin=y | full-thr=y | flips abs->thr | flips bin->thr | meaning                                                          |
|------|-------|------------|------------|----------------|----------------|------------------------------------------------------------------|
| SE   | 0     | 0          | 0          | 0              | 0              | software engineering task (defects, testing, requirements, code) |
| MO   | 0     | 0          | 0          | 0              | 0              | multi-objective / search-based optimization                      |
| EX   | 0     | 0          | 0          | 0              | 0              | explanation / interpretability / XAI                             |
| BM   | 0     | 0          | 0          | 0              | 0              | benchmarking / empirical comparison                              |

## Group tables (same 0 papers)

| group | abstract | full-bin | full-thr |
|-------|----------|----------|----------|

## Technology facet (same 0 papers; DRAFT, hand-audit while reading)

Topic flags above say which literature a paper is in;
these say how its method works. Full text only
(abstracts under-report methodology).

| tech  | full-bin=y | full-thr=y | meaning                                                            |
|-------|------------|------------|--------------------------------------------------------------------|
| EXACT | 0          | 0          | exact solvers (integer/linear/constraint programming, SAT/SMT)     |
| EVO   | 0          | 0          | evolutionary / genetic / Pareto search (NSGA, SPEA, MOEA/D)        |
| SMBO  | 0          | 0          | sequential model-based optimization (Bayesian, surrogates, SMAC)   |
| SYM   | 0          | 0          | symbolic / rule-based reasoning (trees, rule lists, logic, fuzzy)  |
| AGG   | 0          | 0          | aggregation / scalarization (weighted sums, utility, desirability) |
| NN    | 0          | 0          | neural methods (deep learning, transformers, LLMs)                 |

## Top tf-idf terms per paper (stemmed)

