# TODO: the meta-paper work order

Timm's instructions, verbatim (2026-07-25):

> write me a aper about writing a paper. run our 14
> point stuff to paper2 i.e. paper1 is before the
> critics, then we see the critics reports, then we get
> autocorect paoer2 waiting for manual fixes. keep a
> small numer of itnernmediaries aong the way. readme,
> paper1, ciertics reports, paper2.
>
> so this will be a meta paper explaining the rite
> method and appying it to ite reviews.
>
> when you critie, see section3 of fix
> https://arxiv.org/pdf/1612.03224. start there and do
> a forward and backnowball to find what we should be
> citeing since and what we should be citing before.
>
> i want the meta paper to show the method oadn offer
> some critiues of the paper
>
> btw, to answer some of the pre-questions, i am tim
> menzies and i am good at reviewing and wiring se
> research paeprs. recent = last 5 years.

Parsed:

1. Deliverable: meta-paper that explains the rite
   method AND applies it to itself (shows the method,
   then critiques its own draft).
2. Run the 14-step HOWTO loop up to paper2:
   paper1 = draft before critics (HOWTO step 9);
   critic reports (steps 10-11);
   paper2 = auto-fixes applied, manual fixes listed
   and left waiting (step 13, stopped there).
3. Intermediaries, few and named: README, paper1,
   critic reports, paper2. Nothing else persists.
4. Lit anchor: arXiv 1612.03224, section 3. Start
   there; forward snowball (who cites it since) and
   backward snowball (what it cites) to find what we
   should cite after and before it.
5. Pre-answers to HOWTO steps 1-4: author is Tim
   Menzies; good at = reviewing and writing SE
   research papers; recent = last 5 years
   (README years: 2021-2026).
6. lit/ already holds the first exhibit (the
   abstract-vs-fulltext coding study); the meta-paper
   uses it as evidence. See lit/EXHIBIT.md.

7. Rut-rebuttal exhibit: timm's own encode of his last
   five years of work (his flags, his papers, coded at
   thr like everyone else's), as evidence for the
   HOWTO Objections section ("decide for yourself if
   this career was in a rut"). Verbatim source lines
   (2026-07-25):

   > well having follwoing the forumla for decades now,
   > i can assert that ruts were not my problem. the
   > lit review methods put me in contact with material
   > well outside my prior experience; the subsequent
   > experiments we ran, and the problems we
   > encountered, forced a critical eval of the tool
   > base's premises. you can decide for yourself if my
   > career was "in a rut" or not, but i offer here my
   > own encode from the last 5 years, just to suggest
   > that fighting with our sharpest sword might be the
   > fastest way to cut through the nonsense to find
   > exciting new stuff.

8. RESOLVED 2026-07-25: the sqrt(n) law is Price's,
   not Glass's (timm confirmed). Cite: Derek J. de
   Solla Price, Little Science, Big Science, Columbia
   University Press, 1963. HOWTO Objections updated.
9. RESOLVED 2026-07-25 (rite commit 10bb07f): fetch.py
   reads optional README seed: lines (published DOI or
   OpenAlex W-id; arXiv 10.48550 DOIs often absent
   from OpenAlex); snowball.py forward-snowballs the
   seeds (else kept classics) -> lit/forward.tsv.
   Workdir README now seeds the anchor via its EMSE
   DOI 10.1007/s10664-017-9587-0. Original note:
   Engine feature (loop back later): snowballing is
   two-directional. Backward snowball (implemented)
   finds classics; forward snowball (missing) finds
   what cites some core documents. Let README.md offer
   optional seed lines, e.g.

       seed: doi-or-arxiv-id
       seed: ...

   fetch.py/snowball.py then treat seeds as extra
   roots: backward from them for ancestors, forward
   (OpenAlex cited_by) for descendants. This is also
   how the meta-paper's anchor (arXiv 1612.03224)
   should be wired in, per item 4.

10. OPEN 2026-08-02: paper0 needs a subsection on the
    title and the abstract. They deserve their own
    treatment because they select the reviewers: PCs
    bid and are assigned from title+abstract alone, so
    those two artifacts choose who judges the paper.
    Candidate home: section 5, beside the introduction
    grammar; Shaw's abstract shape (state of the art,
    the problem, the contribution, the evidence) and
    the house rule "the abstract carries the paper"
    are the raw material. Also connects to loop step
    13's recode gate (title+abstract must code the
    same as the body, zero flips).

11. OPEN 2026-08-02: paper0 needs a stats discussion.
    The methods grammar names the gates (repeats,
    Cliff's delta, KS, bootstrap) but the paper never
    says how to choose tests, thresholds, or effect
    sizes, or what "indistinguishable from best"
    means. Candidate raw material: SNAP2's top-tier
    procedure (median sort + per-dataset significance
    cluster; Cliff's delta < 0.195, KS at 95%), the
    bench division (workdir bench.md: stats gates are
    per-field norms), and Matteo's note in intro.tex
    about 30 years of EDA errors (TOSEM 3799715).
