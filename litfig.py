#!/usr/bin/env python3
"""Fig for paper0 sec 5: cites knee + subset overlap.

Fetches three OpenAlex queries (cached in tmp/lit0.json),
draws fig/lit.png: (a) sorted-cites curve of the crossed
goal query with the knee marked (same rule as rite
fetch.py: max distance from the first-to-last chord);
(b) the two subset queries and their overlap.
"""
import json, os, time, urllib.parse, urllib.request
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

YEARS = "2021-01-01"
QS = {
    "cross": "human factors of AI assistants for software engineering",
    "ai4se": "large language models for software engineering",
    "human": "human and social aspects of software developers",
}
CACHE = "tmp/lit0.json"


def fetch(q, pages=2):
    out = []
    for p in range(1, pages + 1):
        url = ("https://api.openalex.org/works?search=" +
               urllib.parse.quote(q) +
               "&filter=from_publication_date:" + YEARS +
               ",type:article|preprint" +
               "&per-page=200&page=%d" % p +
               "&sort=cited_by_count:desc" +
               "&select=id,title,publication_year,cited_by_count")
        with urllib.request.urlopen(url) as r:
            out += json.load(r)["results"]
        time.sleep(1)
    return out


if os.path.exists(CACHE):
    data = json.load(open(CACHE))
else:
    data = {k: fetch(q) for k, q in QS.items()}
    os.makedirs("tmp", exist_ok=True)
    json.dump(data, open(CACHE, "w"))

cites = sorted((w["cited_by_count"] for w in data["cross"]),
               reverse=True)
n = len(cites)
c0, cn = cites[0], cites[-1]


def dist(i):  # distance from chord (0,c0)-(n-1,cn), as fetch.py
    return abs((cn - c0) * i - (n - 1) * (cites[i] - c0))


knee = max(range(n), key=dist)
ids = {k: {w["id"] for w in v} for k, v in data.items()}
both = len(ids["ai4se"] & ids["human"])

BG, RED, BLUE, INK = "#ffffff", "#cc2222", "#2233bb", "#222222"
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(8, 3.4))
fig.patch.set_facecolor(BG)

ax1.plot(range(1, n + 1), cites, color=INK, lw=1.4)
ax1.plot([1, n], [c0, cn], color=INK, ls=":", lw=1.0)
# perpendicular from chord to knee, in normalized space
u, v = knee / (n - 1), (cites[knee] - cn) / (c0 - cn)
t = (u - v + 1) / 2  # foot of perpendicular on chord v = 1 - u
fx, fy = 1 + t * (n - 1), cn + (1 - t) * (c0 - cn)
ax1.plot([knee + 1, fx], [cites[knee], fy], color=RED, ls="--",
         lw=1.2)
ax1.plot([knee + 1], [cites[knee]], "o", color=RED, ms=5)
ax1.annotate("knee: %d papers\n(>= %d cites)" % (knee + 1, cites[knee]),
             xy=(knee + 1, cites[knee]),
             xytext=(knee + 120, c0 * 0.12), fontsize=10, color=RED)
ax1.set_xlabel("papers, sorted by citations", fontsize=10)
ax1.set_ylabel("citations", fontsize=10)
ax1.tick_params(labelsize=9)
for sp in ("top", "right"):
    ax1.spines[sp].set_visible(False)
ax1.set_box_aspect(1)

for cx, col, lab, nn in ((0.38, RED, "AI-for-SE", len(ids["ai4se"])),
                         (0.62, BLUE, "human/social", len(ids["human"]))):
    ax2.add_patch(plt.Circle((cx, 0.5), 0.27, fc=col, alpha=0.18,
                             ec=col, lw=1.4))
ax2.text(0.24, 0.83, "AI-for-SE", fontsize=11, color=RED,
         ha="center")
ax2.text(0.76, 0.83, "human/social", fontsize=11, color=BLUE,
         ha="center")
ax2.text(0.28, 0.5, str(len(ids["ai4se"]) - both), fontsize=12,
         ha="center", color=INK)
ax2.text(0.72, 0.5, str(len(ids["human"]) - both), fontsize=12,
         ha="center", color=INK)
ax2.text(0.5, 0.5, str(both), fontsize=13, fontweight="bold",
         ha="center", color=INK)
ax2.text(0.5, 0.13, "overlap = the crossed area's reading set",
         fontsize=9.5, ha="center", color=INK)
ax2.set_xlim(0, 1)
ax2.set_ylim(0, 1)
ax2.set_aspect("equal")
ax2.axis("off")

plt.tight_layout()
plt.savefig("fig/lit.png", dpi=300, facecolor=BG,
            bbox_inches="tight", pad_inches=0.02)
print("wrote fig/lit.png; knee %d at %d cites; overlap %d" %
      (knee + 1, cites[knee], both))

# ---- second figure: inside the 94 (fig/lit2.png) ----
d2 = json.load(open("tmp/lit3_data.json"))
R = d2["regions"]
fig2, ax = plt.subplots(figsize=(4.4, 4.2))
fig2.patch.set_facecolor(BG)
GREEN = "#1a7a3a"
for (cx, cy), col in (((0.50, 0.60), RED), ((0.40, 0.42), BLUE),
                      ((0.60, 0.42), GREEN)):
    ax.add_patch(plt.Circle((cx, cy), 0.23, fc=col, alpha=0.15,
                            ec=col, lw=1.4))
ax.text(0.50, 0.88, "trust/reliability", fontsize=11, color=RED,
        ha="center")
ax.text(0.16, 0.24, "productivity", fontsize=11, color=BLUE,
        ha="center")
ax.text(0.84, 0.24, "human studies", fontsize=11, color=GREEN,
        ha="center")
for (x, y), k in (((0.50, 0.70), "Tonly"), ((0.30, 0.38), "Ponly"),
                  ((0.70, 0.38), "Honly"), ((0.40, 0.55), "TP"),
                  ((0.60, 0.55), "TH"), ((0.50, 0.35), "PH"),
                  ((0.50, 0.47), "TPH")):
    ax.text(x, y, str(R[k]), fontsize=12, ha="center", color=INK,
            fontweight="bold" if k in ("PH", "TPH") else "normal")
ax.text(0.5, 0.06,
        "above-knee reading set: %d papers (>= %d cites);\n"
        "coded %d abstracts; %d matched no flag" %
        (d2["n"], d2["kneecites"], d2["n_abs"], R["none"]),
        fontsize=9.5, ha="center", color=INK)
ax.set_xlim(0, 1)
ax.set_ylim(0, 1)
ax.set_aspect("equal")
ax.axis("off")
fig2.savefig("fig/lit2.png", dpi=300, facecolor=BG,
             bbox_inches="tight", pad_inches=0.02)
print("wrote fig/lit2.png")

# ---- table of the above-knee reading set (fig/littab.tex) ----
CACHE4 = "tmp/lit4.json"
if os.path.exists(CACHE4):
    det4 = json.load(open(CACHE4))
else:
    top = sorted(data["cross"], key=lambda w: -w["cited_by_count"])[:knee + 1]
    det4 = []
    for i in range(0, len(top), 50):
        chunk = "|".join(w["id"].rsplit("/", 1)[1]
                         for w in top[i:i + 50])
        with urllib.request.urlopen(
            "https://api.openalex.org/works?filter=ids.openalex:" +
            chunk + "&per-page=50&select=id,title,publication_year,"
            "cited_by_count,primary_location,authorships") as r:
            det4 += json.load(r)["results"]
        time.sleep(1)
    json.dump(det4, open(CACHE4, "w"))

def esc(x):
    for a, b in (("\\", ""), ("&", "\\&"), ("%", "\\%"),
                 ("#", "\\#"), ("_", "\\_"), ("$", "\\$")):
        x = x.replace(a, b)
    return x

def venue(w):
    loc = w.get("primary_location") or {}
    src = loc.get("source") or {}
    return src.get("display_name") or "arXiv"

def first_author(w):
    a = w.get("authorships") or []
    return (a[0]["author"]["display_name"].split()[-1]
            if a else "?")

det4.sort(key=lambda w: -w["cited_by_count"])
with open("fig/littab.tex", "w") as f:
    f.write("% generated by litfig.py; do not hand-edit\n")
    f.write("\\begin{tabular}"
            "{@{}rp{0.58\\linewidth}p{0.17\\linewidth}rr@{}}\n"
            "\\toprule\n\\# & paper & venue & year & cites"
            "\\\\\n\\midrule\n")
    for i, w in enumerate(det4):
        t = esc(w["title"] or "?")
        t = t[:52] + ("..." if len(t) > 52 else "")
        v = esc(venue(w))[:22]
        f.write("%d & %s (%s) & %s & %d & %d\\\\\n" %
                (i + 1, t, esc(first_author(w)), v,
                 w.get("publication_year") or 0,
                 w["cited_by_count"]))
    f.write("\\bottomrule\n\\end{tabular}\n")
print("wrote fig/littab.tex (%d rows)" % len(det4))
