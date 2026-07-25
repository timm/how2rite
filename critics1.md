# critics1: critic reports for paper1

Target: paper1 at commit 0d5ffba ("Follow Your
Strengths" reorg). Critics applied per HOWTO step 11:
the paper's own step-13 gate, Shaw's reader questions,
Widom's intro questions, Laurie's laws, a reviewer-2
pass. Step 10 (critic 1 = timm, offline, 30-60 min)
still pending; step 12 (other humans) pending.

## Measured: paper1 FAILS its own abstract gate

Ran flags.py over own title+abstract vs pdftotext of
own body (2,916 words), threshold 0.5 per 1k words:

| flag | abs hits | body/1k | at thr | gate |
|------|----------|---------|--------|------|
| SE   | 4        | 11.66   | yes    | ok   |
| MO   | 1        | 2.40    | yes    | ok   |
| EX   | 1        | 1.37    | yes    | ok   |
| BM   | 0        | 2.40    | yes    | FAIL |

The body's benchmarking/comparison content (the whole
exhibit compares abstract vs full-text coding) never
reaches the abstract: no compare/empirical/benchmark
word appears there. The paper's one aggressive rule
catches the paper. Fix is auto-applicable in paper2:
e.g. "coding 54 papers" -> "comparing the coding of 54
papers' abstracts against their full texts".

## Reviewer-2: promise/evidence gaps

1. Title promise unearned. "Follow Your Strengths" and
   intro beat 3 promise reverse-engineering an author's
   strengths and mapping them to pressing problems
   (loop steps 3-7). No exhibit demonstrates this; the
   five-year self-coding is future work. Either add
   that exhibit (TODO item 7 already plans it) or the
   title outruns the evidence. MANUAL.
2. "consumes months": no citation, no number. Laurie:
   data talk, statistics shout. Candidate datum: this
   paper's own git log (first draft to now, wall-clock
   and human-minutes). MANUAL.
3. "none of it saves any time": blatant assertion,
   Shaw's worst validation category. Cut the absolute
   or evidence it. AUTO (soften) or MANUAL (evidence).
4. Speed is now the motivating problem but no RQ
   measures time. RQ3 candidate: does the pipeline
   save time, with this workdir's own timeline as the
   first datum. MANUAL (scope decision).
5. Conclusion restates only the old claims
   (encodability, cheap reads). The new intro also
   promises strengths and speed; conclusion must
   restate those with receipts or the paper opens
   promises it never closes. MANUAL until RQ3 decided.

## Shaw: three reader questions

- Contribution stated: yes, four items, quotable.
- New result: yes, the abstract-vs-fulltext asymmetry
  (and now: the tool failing its own gate).
- Why believe: partial. Table 2 flips are concrete, but
  the 0.5 cutoff is unvalidated and the promised
  sensitivity analysis has not run (paper admits this;
  reviewers will still ding it).

## Widom: five intro questions

Problem (slow writing): yes. Why interesting (unit of
work): yes. Why unsolved (advice not executable): yes.
Why now (LLMs): yes. What we did + found: mostly; the
found-preview leans entirely on RQ2's numbers.

## Citation hygiene

- newell91 is a videotaped talk; "know your strengths
  and follow them" is a paraphrase. Verify wording
  against the Desires and Diversions transcript before
  any submission; a title-bearing misquote of Newell is
  a desk-reject-grade embarrassment. MANUAL.
- brereton07 "on record since at least 2007": ok.

## Split (feeds step 13)

AUTO for paper2: abstract BM wording; soften "saves any
time".
MANUAL, waiting: title-evidence gap (add TODO-7
exhibit); months datum; RQ3 scope; Newell transcript
check; threshold sensitivity run; conclusion receipts.
