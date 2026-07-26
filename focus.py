#!/usr/bin/env python3
"""FOCUS-style repertory grid (Shaw/Gaines WebGrid look).

Elements = paper0 authors, constructs = triad-elicited strengths.
Reorders rows/cols by similarity (city-block), reverses construct
poles where that raises match, draws matrix + red element tree on
top + blue construct tree on right, % match scales.
"""
import itertools, matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

ELEMENTS = ["Menzies", "Di Nucci", "Lenarduzzi", "Armenti",
            "Esposito", "Schmid",
            # ICSE'27 research-track areas as reference elements
            "AI-for-SE", "Analytics", "Architecture", "Security",
            "Evolution", "Human/Social", "Requirements",
            "SE-for-AI", "Testing"]
NTOPIC = 9  # trailing elements drawn italic
# (left pole [1], right pole [5], ratings per element above)
CONSTRUCTS = [
    ("one artifact, in depth",  "corpora, at scale",      [5,3,3,1,3,2, 4,5,2,2,3,2,2,3,3]),
    ("quality now (debt)",      "quality future (predict)",[5,2,2,3,3,3, 4,4,2,3,1,2,1,4,4]),
    ("upfront design",          "post-hoc observation",    [5,4,4,4,3,1, 4,5,1,3,5,3,1,4,4]),
    ("AI-centred",              "AI-free SE",              [1,3,3,5,1,4, 1,2,4,3,4,4,4,1,3]),
    ("adversarial (security)",  "benign comprehension",    [4,4,3,5,2,4, 3,4,3,1,4,5,4,3,2]),
    ("builds tools",            "runs studies",            [3,3,5,1,3,2, 2,3,2,2,3,4,3,3,2]),
    ("secondary studies (SLR)", "primary experiments",     [5,2,1,4,3,3, 4,4,3,4,3,3,3,4,5]),
    ("industry-facing",         "open-corpus academic",    [5,3,2,4,2,1, 3,5,2,3,3,3,2,3,4]),
    ("process and people",      "code and models",         [4,4,3,3,4,2, 4,4,3,5,4,1,2,4,5]),
]
NE, NC, SPAN = len(ELEMENTS), len(CONSTRUCTS), 4  # rating span 1..5


def elem_dist(a, b, rows):  # city-block over constructs
    return sum(abs(r[a] - r[b]) for r in rows)


def path_cost(p, dist):
    return sum(dist(p[i], p[i + 1]) for i in range(len(p) - 1))


def order_by_path(n, dist):  # min total adjacent distance
    if n <= 8:  # exact
        best, bestc = None, 1e9
        for p in itertools.permutations(range(1, n)):
            p = (0,) + p
            c = path_cost(p, dist)
            if c < bestc:
                best, bestc = list(p), c
        return best
    bestp, bestc = None, 1e9  # greedy each start + 2-opt
    for s0 in range(n):
        p, left = [s0], set(range(n)) - {s0}
        while left:
            nxt = min(left, key=lambda j: dist(p[-1], j))
            p.append(nxt)
            left.discard(nxt)
        improved = True
        while improved:
            improved = False
            for i in range(1, n - 1):
                for j in range(i + 1, n):
                    q = p[:i] + p[i:j + 1][::-1] + p[j + 1:]
                    if path_cost(q, dist) < path_cost(p, dist):
                        p, improved = q, True
        c = path_cost(p, dist)
        if c < bestc:
            bestp, bestc = p, c
    return bestp


def single_link(order, dist, maxd):
    """Agglomerative single-linkage constrained to the display
    order: only adjacent clusters merge, so the drawn tree is
    planar (no crossings). Returns [(a, b, match%)]."""
    clusters = [frozenset([i]) for i in order]
    merges = []
    while len(clusters) > 1:
        best = None
        for k in range(len(clusters) - 1):
            x, y = clusters[k], clusters[k + 1]
            d = min(dist(i, j) for i in x for j in y)
            if best is None or d < best[3]:
                best = (k, x, y, d)
        k, x, y, d = best
        clusters[k:k + 2] = [x | y]
        merges.append((x, y, 100.0 * (1 - d / maxd)))
    return merges


rows = [list(r) for _, _, r in CONSTRUCTS]
# element ordering
eorder = order_by_path(NE, lambda a, b: elem_dist(a, b, rows))
# construct ordering, allowing pole reversal
def cdist(i, j):
    a, b = rows[i], rows[j]
    d1 = sum(abs(x - y) for x, y in zip(a, b))
    d2 = sum(abs(x - (6 - y)) for x, y in zip(a, b))
    return min(d1, d2)
corder = order_by_path(NC, cdist)
# reverse poles greedily so neighbours align
flipped = [False] * NC
for k in range(1, NC):
    i, j = corder[k - 1], corder[k]
    a = [(6 - v if flipped[i] else v) for v in rows[i]]
    b = rows[j]
    d1 = sum(abs(x - y) for x, y in zip(a, b))
    d2 = sum(abs(x - (6 - y)) for x, y in zip(a, b))
    flipped[j] = d2 < d1

M = []  # reordered matrix, poles applied
LPOLE, RPOLE = [], []
for ci in corder:
    l, r, vals = CONSTRUCTS[ci]
    v = [(6 - x) for x in vals] if flipped[ci] else vals
    if flipped[ci]:
        l, r = r, l
    M.append([v[e] for e in eorder])
    LPOLE.append(l)
    RPOLE.append(r)
ELAB = [ELEMENTS[e] for e in eorder]

emerges = single_link(eorder,
                      lambda a, b: elem_dist(a, b,
                          [[(6 - x) if flipped[i] else x for x in rows[i]]
                           for i in range(NC)]),
                      SPAN * NC)
cmerges = single_link(corder, cdist, SPAN * NE)

# ---------- drawing ----------
BG, RED, BLUE = "#ffffff", "#cc2222", "#2233bb"
GREYS = {1: "#ffffff", 2: "#e8e8e8", 3: "#c9c9c9", 4: "#a5a5a5",
         5: "#8a8a8a"}
CW, CH = 0.45, 0.32          # cell size
X0, Y0 = 3.1, 1.2           # matrix lower-left
TREE_H, TREE_W = 1.6, 1.4   # dendrogram depth
fig, ax = plt.subplots(figsize=(9.6, 4.6 + 0.34 * NC))
fig.patch.set_facecolor(BG)
ax.set_facecolor(BG)
ax.set_aspect("auto")
ax.axis("off")

top = Y0 + NC * CH
for r in range(NC):
    y = top - (r + 1) * CH
    for c in range(NE):
        x = X0 + c * CW
        v = M[r][c]
        ax.add_patch(plt.Rectangle((x, y), CW, CH, lw=0.6,
                     ec="#888", fc=GREYS[v]))
        ax.text(x + CW / 2, y + CH / 2, str(v), ha="center",
                va="center", fontsize=11, color="#222")
    ax.text(X0 - 0.12, y + CH / 2, f"{LPOLE[r]} ", ha="right",
            va="center", fontsize=11, color=BLUE)
    ax.text(X0 + NE * CW + 0.12, y + CH / 2, RPOLE[r], ha="left",
            va="center", fontsize=11, color=BLUE)

# red element labels, rotated; topics italic
for c, ei in enumerate(eorder):
    x = X0 + c * CW + CW / 2
    style = "italic" if ei >= NE - NTOPIC else "normal"
    ax.text(x, Y0 - 0.14, ELEMENTS[ei], rotation=55, ha="right",
            va="top", fontsize=10, color=RED, style=style)

# --- dendrogram helpers: draw merges as right-angle trees ---
def draw_tree(merges, leaf_pos, axis, base, depth, color, scale_lo):
    """axis='top' or 'right'; base = matrix edge coordinate."""
    pos = {frozenset([i]): (leaf_pos(i), base) for i in
           [i for m in merges for s in m[:2] for i in s]}
    gap = depth / 14  # min step past children, breaks ties
    for x, y, match in merges:
        span = (100 - match) / (100 - scale_lo) * depth
        px, bx = pos.get(x), pos.get(y)
        h = max(base + span, px[1] + gap, bx[1] + gap)
        if axis == "top":
            for p in (px, bx):
                ax.plot([p[0], p[0]], [p[1], h], color=color, lw=1.1)
            ax.plot([px[0], bx[0]], [h, h], color=color, lw=1.1)
            pos[x | y] = ((px[0] + bx[0]) / 2, h)
        else:
            for p in (px, bx):
                ax.plot([p[1], h], [p[0], p[0]], color=color, lw=1.1)
            ax.plot([h, h], [px[0], bx[0]], color=color, lw=1.1)
            pos[x | y] = ((px[0] + bx[0]) / 2, h)

etop = top + 0.15
draw_tree(emerges,
          lambda i: X0 + eorder.index(i) * CW + CW / 2,
          "top", etop, TREE_H, RED, 60)
cright = X0 + NE * CW + 3.9
draw_tree(cmerges,
          lambda i: top - (corder.index(i) + 1) * CH + CH / 2,
          "right", cright, TREE_W, BLUE, 60)

# scales
for pct in (100, 90, 80, 70, 60):
    y = etop + (100 - pct) / 40 * TREE_H
    ax.text(X0 - 0.25, y, str(pct), ha="right", va="center",
            fontsize=9, color=RED)
    if pct in (100, 80, 60):
        x = cright + (100 - pct) / 40 * TREE_W
        ax.text(x, top + 0.12, str(pct), ha="center", va="bottom",
                fontsize=9, color=BLUE)

ax.set_xlim(0, cright + TREE_W + 0.6)
ax.set_ylim(Y0 - 1.85, etop + TREE_H + 0.3)
plt.savefig("fig/focus_grid.png", dpi=300, facecolor=BG,
            bbox_inches="tight", pad_inches=0.02)
print("wrote fig/focus_grid.png")
