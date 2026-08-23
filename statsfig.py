"""Regenerate fig/stats_xdf.pdf and fig/stats_ks.pdf: the
appendix stats tutorial samples as pdf and cdf, then the KS
max-gap "pole" view (make statsfig)."""
import matplotlib.pyplot as plt

A = [1,2,2,2,3,3,3,3,3,4,4,4,4,5,5,5,6,6,7,8]
B = [5,6,6,7,7,7,8,8,8,8,8,9,9,9,9,10,10,10,11,11]
C = [5,6,6,7,7,8,8,8,8,9,9,9,9,9,10,10,10,11,11,11]

# Okabe-Ito (validated CVD-safe); linestyle = second encoding
STYLE = {"a": ("#0072B2", "-"),
         "b": ("#D55E00", "--"),
         "c": ("#009E73", ":")}
VALS = range(1, 12)

plt.rcParams.update({
    "font.family": "serif", "mathtext.fontset": "stix",
    "font.size": 7, "axes.linewidth": 0.5})

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(3.4, 1.55))
for name, xs in [("a", A), ("b", B), ("c", C)]:
    col, ls = STYLE[name]
    pdf = [xs.count(v) / len(xs) for v in VALS]
    cdf = [sum(x <= v for x in xs) / len(xs) for v in VALS]
    ax1.step(VALS, pdf, ls, color=col, lw=1.3, where="mid")
    ax2.step(VALS, cdf, ls, color=col, lw=1.3,
             where="post", label=name)
    ax1.annotate(name, (xs[len(xs) // 2], max(pdf)),
                 xytext=(0, 2), textcoords="offset points",
                 ha="center", color=col, fontsize=8,
                 fontstyle="italic")
ax1.set_ylabel("pdf")
ax2.set_ylabel("cdf")
ax2.legend(loc="upper left", frameon=False, fontsize=6.5,
           handlelength=1.6, labelspacing=0.2,
           borderaxespad=0.2)
for ax in (ax1, ax2):
    ax.set_xlabel("days to first MVP")
    ax.set_xticks([1, 5, 11])
    ax.grid(color="0.9", lw=0.4)
    ax.set_axisbelow(True)
    for s in ("top", "right"): ax.spines[s].set_visible(False)
fig.tight_layout(pad=0.4)
fig.savefig("fig/stats_xdf.pdf", bbox_inches="tight")
print("wrote fig/stats_xdf.pdf")

# second figure: KS as the tallest pole between two cdfs
def ecdf(xs, v): return sum(x <= v for x in xs) / len(xs)

fig, axs = plt.subplots(1, 2, figsize=(3.4, 1.55))
for ax, (n1, xs), (n2, ys) in zip(
        axs, [("a", A), ("b", B)], [("b", B), ("c", C)]):
    vstar = max(VALS, key=lambda v: abs(ecdf(xs,v) - ecdf(ys,v)))
    d = abs(ecdf(xs, vstar) - ecdf(ys, vstar))
    for (name, s), off in (((n1, xs), (-11, 3)),
                           ((n2, ys), (7, -9))):
        col, ls = STYLE[name]
        ax.step(VALS, [ecdf(s, v) for v in VALS], ls, color=col,
                lw=1.3, where="post")
        ax.annotate(name, (s[10], ecdf(s, s[10])), xytext=off,
                    textcoords="offset points", color=col,
                    fontsize=8, fontstyle="italic")
    lo, hi = sorted((ecdf(xs, vstar), ecdf(ys, vstar)))
    ax.plot([vstar, vstar], [lo, hi], color="0.15", lw=2,
            solid_capstyle="butt", marker="_", ms=5, mew=1.2)
    ax.annotate(f"D={d:.2f}", (vstar, (lo + hi) / 2),
                xytext=(5, 0), textcoords="offset points",
                fontsize=7, va="center")
    ax.set_xlabel("days to first MVP")
    ax.set_xticks([1, 5, 11])
    ax.grid(color="0.9", lw=0.4)
    ax.set_axisbelow(True)
    for s_ in ("top", "right"): ax.spines[s_].set_visible(False)
axs[0].set_ylabel("cdf")
axs[1].set_yticklabels([])
fig.tight_layout(pad=0.4)
fig.savefig("fig/stats_ks.pdf", bbox_inches="tight")
print("wrote fig/stats_ks.pdf")

# third artifact: fig/stats_grid.tex -- 10 treatments x 10
# datasets, grey = top rank per dataset, wins counted below
import random

TINY = 1e-32
def mean(a): return sum(a) / len(a)
def stdev(a): n = len(a)//10; return (a[9*n]-a[n])/2.56

def cohen(xs, ys):
    n, m = len(xs), len(ys)
    sd = (((n-1)*stdev(xs)**2 +
           (m-1)*stdev(ys)**2) / (n+m-2)) ** 0.5
    return abs(mean(xs) - mean(ys)) / (sd + TINY)

def ks(xs, ys):
    nx, ny = len(xs), len(ys)
    d = p = q = 0
    while p < nx and q < ny:
        v = min(xs[p], ys[q])
        while p < nx and xs[p] == v: p += 1
        while q < ny and ys[q] == v: q += 1
        d = max(d, abs(p/nx - q/ny))
    return d / ((nx + ny) / (nx * ny)) ** 0.5

def cliffs(xs, ys):
    gt = lt = j = k = 0
    for x in xs:
        while j < len(ys) and ys[j] < x: j += 1; k = j
        while k < len(ys) and ys[k] == x: k += 1
        gt += j; lt += len(ys) - k
    return abs(gt - lt) / (len(xs) * len(ys))

def same(xs, ys, c0=.35, d0=.195, k0=1.36, is_sorted=True):
    if not is_sorted:
        xs, ys = sorted(xs), sorted(ys)
    return (cohen(xs, ys)  <= c0 and
            cliffs(xs, ys) <= d0 and
            ks(xs, ys)     <= k0)

def ranks(d, big=False):
    mid  = lambda t: t[len(t) // 2]
    dd   = {k: sorted(v) for k, v in d.items()}
    out, win, rank, best = {}, [], -1, None
    for k in sorted(dd, key=lambda k: mid(dd[k]), reverse=big):
        if best is None or not same(dd[best], dd[k]):
            rank, best = rank + 1, k
        if rank == 0: win.append(k)
        out[k] = rank
    return win, out

random.seed(7)
RXS = [f"rx{j}" for j in range(1, 11)]
DBS = [f"db{i}" for i in range(1, 11)]
base = {rx: 8 + (j % 5) * 1.5 for j, rx in enumerate(RXS)}
base["rx7"] = 5                      # usual winner
mu = {db: dict(base) for db in DBS}
mu["db2"].update(rx7=12, rx2=3)      # counterexample 1
mu["db5"].update(rx7=12, rx5=3)      # counterexample 2

rows, wins = [], {rx: 0 for rx in RXS}
for db in DBS:
    data = {rx: sorted(round(random.gauss(mu[db][rx], 1), 1)
                       for _ in range(20)) for rx in RXS}
    top = set(ranks(data)[0])
    cells = []
    for rx in RXS:
        med = data[rx][10]
        if rx in top:
            wins[rx] += 1
            cells.append(r"\cellcolor{black!15}%.1f" % med)
        else:
            cells.append("%.1f" % med)
    rows.append(db + " & " + " & ".join(cells) + r"\\")

out = [r"\begin{tabular}{@{}l*{10}{r}@{}}", r"\toprule",
       " & " + " & ".join(RXS) + r"\\", r"\midrule",
       *rows, r"\midrule",
       r"wins & " + " & ".join(str(wins[rx]) for rx in RXS)
       + r"\\", r"\bottomrule", r"\end{tabular}"]
open("fig/stats_grid.tex", "w").write("\n".join(out) + "\n")
print("wrote fig/stats_grid.tex; wins:",
      {k: v for k, v in wins.items() if v})
