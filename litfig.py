#!/usr/bin/env python3
"""Sec 5 pipeline: SE-venue-filtered lit review of the crossed area.

Fetches wing queries from OpenAlex (cached tmp/litse.json),
keeps only papers in SE venues (VENUES: a reviewable input;
sources: se-deadlines.github.io, Google Scholar's venue index,
plus any venue whose name contains "software"). Snowballing is
deliberately NOT venue-filtered: refs and citers roam anywhere.

Outputs: fig/lit.png (knee + wings venn), fig/lit2.png (coded
venn of the reading set), fig/littab.tex (reading-set table),
fig/litnums.tex (every number quoted in sec0/lit.tex).
"""
import json, os, re, time, urllib.parse, urllib.request
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

YEARS = "2021-01-01"
PAGES = 5  # x200 per query
QS = {
    "cross": "human factors of AI assistants for software engineering",
    "ai4se": "large language models for software engineering",
    "human": "human and social aspects of software developers",
}
# SE venue filter: an input, not an oracle. Edit and rerun.
VENUES = (r"software|ICSE|ESEC|FSE\b|\bASE\b|ISSTA|ICSME|MSR\b"
          r"|SANER|ICPC|ESEM|ISSRE|ICST\b|requirements engineering"
          r"|program|computer languages")
NOTVEN = (r"environmental|statistical|mathematical|optimization"
          r"|elearning|advances in engineering|open source software")
FLAGS = dict(
    TRUST=r"trust|overrelian|reliab|confiden|verif|correct|halluc"
          r"|security|vulnerab",
    PROD=r"productiv|efficien|speed|faster|accelerat|effort"
         r"|performance",
    HUM=r"user stud|interview|survey|usabilit|experience|cognit"
        r"|percept|human.centered|qualitative|developer stud")
CACHE = "tmp/litse2.json"
SRCCACHE = "tmp/sesources2.json"
SEL = ("id,title,publication_year,cited_by_count,primary_location,"
       "authorships,abstract_inverted_index,referenced_works")


def get(url, tries=4):
    for i in range(tries):
        try:
            with urllib.request.urlopen(url) as r:
                return json.load(r)
        except Exception:
            time.sleep(2 + 2 * i)
    return {"results": []}


def se_sources():
    if os.path.exists(SRCCACHE):
        return json.load(open(SRCCACHE))
    d = get("https://api.openalex.org/sources?filter="
            "display_name.search:software&per-page=100"
            "&sort=works_count:desc&select=id,display_name"
            "&mailto=timm@ieee.org")
    keep = [x["id"].rsplit("/", 1)[1] for x in d["results"]
            if re.search(VENUES, x["display_name"], re.I)
            and not re.search(NOTVEN, x["display_name"], re.I)]
    os.makedirs("tmp", exist_ok=True)
    json.dump(keep, open(SRCCACHE, "w"))
    return keep


def fetch(q):
    srcs = "|".join(se_sources())
    out = []
    for p in range(1, PAGES + 1):
        d = get("https://api.openalex.org/works?search=" +
                urllib.parse.quote(q) +
                "&filter=from_publication_date:" + YEARS +
                ",primary_location.source.id:" + srcs +
                "&per-page=200&page=%d" % p +
                "&sort=cited_by_count:desc&select=" + SEL +
                "&mailto=timm@ieee.org")
        out += d["results"]
        time.sleep(1)
    return out


def venue(w):
    loc = w.get("primary_location") or {}
    src = loc.get("source") or {}
    return src.get("display_name") or "arXiv"


def is_se(w):
    return re.search(VENUES, venue(w), re.I) is not None


def abstract(w):
    inv = w.get("abstract_inverted_index")
    if not inv:
        return ""
    pos = {}
    for word, ps in inv.items():
        for p in ps:
            pos[p] = word
    return " ".join(pos[p] for p in sorted(pos))


if os.path.exists(CACHE):
    data = json.load(open(CACHE))
else:
    data = {k: fetch(q) for k, q in QS.items()}
    os.makedirs("tmp", exist_ok=True)
    json.dump(data, open(CACHE, "w"))

fetched = {k: len(v) for k, v in data.items()}
se = data  # venue filter applied server-side
ids = {k: {w["id"] for w in v} for k, v in se.items()}
both = ids["ai4se"] & ids["human"]

# knee of the SE-filtered goal query
cross = sorted(se["cross"], key=lambda w: -w["cited_by_count"])
cites = [w["cited_by_count"] for w in cross]
n, c0, cn = len(cites), cites[0], cites[-1]
knee = max(range(n), key=lambda i:
           abs((cn - c0) * i - (n - 1) * (cites[i] - c0)))
top = cross[:knee + 1]

# code the reading set
have = [(w, abstract(w)) for w in top]
n_abs = sum(1 for _, a in have if a)
S = {f: {w["id"] for w, a in have if a and re.search(rx, a, re.I)}
     for f, rx in FLAGS.items()}
T, P, H = S["TRUST"], S["PROD"], S["HUM"]
coded = {w["id"] for w, a in have if a}
R = dict(Tonly=len(T - P - H), Ponly=len(P - T - H),
         Honly=len(H - T - P), TP=len((T & P) - H),
         TH=len((T & H) - P), PH=len((P & H) - T),
         TPH=len(T & P & H), none=len(coded - T - P - H))

# snowball from the reading set: NOT venue-filtered, on purpose
refs = {}
for w in top:
    for r in w.get("referenced_works") or []:
        refs[r] = refs.get(r, 0) + 1
classics = sum(1 for c in refs.values() if c >= 2)
citing = set()
for w in top:
    wid = w["id"].rsplit("/", 1)[1]
    d = get("https://api.openalex.org/works?filter=cites:" + wid +
            "&per-page=200&select=id&mailto=timm@ieee.org")
    citing |= {x["id"] for x in d["results"]}
    time.sleep(0.6)

# team check across the SE-filtered goal set
TEAM = [r"tim(othy)? menzies", r"carmen armenti", r"dario di nucci",
        r"matteo esposito", r"valentina lenarduzzi",
        r"klaus schmid\b"]
own = 0
for w in cross:
    for a in (x["author"]["display_name"].lower()
              for x in w.get("authorships") or []):
        if any(re.search(t, a) for t in TEAM):
            own += 1

# ---------- fig/lit.png: knee + wings ----------
BG, RED, BLUE, INK = "#ffffff", "#cc2222", "#2233bb", "#222222"
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(8, 3.4))
fig.patch.set_facecolor(BG)
ax1.plot(range(1, n + 1), cites, color=INK, lw=1.4)
ax1.plot([1, n], [c0, cn], color=INK, ls=":", lw=1.0)
u, v = knee / (n - 1), (cites[knee] - cn) / (c0 - cn)
t = (u - v + 1) / 2
fx, fy = 1 + t * (n - 1), cn + (1 - t) * (c0 - cn)
ax1.plot([knee + 1, fx], [cites[knee], fy], color=RED, ls="--",
         lw=1.2)
ax1.plot([knee + 1], [cites[knee]], "o", color=RED, ms=5)
ax1.plot([knee + 1, knee + 1], [0, cites[knee]], color=RED,
         ls=":", lw=1.0)
ax1.plot([1, knee + 1], [cites[knee], cites[knee]], color=RED,
         ls="--", lw=0.8)
ax1.annotate(str(knee + 1), xy=(knee + 1, 0),
             xytext=(knee + 1, -c0 * 0.06), fontsize=9,
             color=RED, ha="center", annotation_clip=False)
ax1.annotate(str(cites[knee]), xy=(1, cites[knee]),
             xytext=(-n * 0.02, cites[knee]), fontsize=9,
             color=RED, ha="right", va="center",
             annotation_clip=False)
ax1.annotate("knee: %d papers\n(>= %d cites)" %
             (knee + 1, cites[knee]),
             xy=(knee + 1, cites[knee]),
             xytext=(n * 0.42, c0 * 0.12), fontsize=10, color=RED)
ax1.set_xlabel("SE-venue papers, sorted by citations", fontsize=10)
ax1.set_ylabel("citations", fontsize=10)
ax1.tick_params(labelsize=9)
for sp in ("top", "right"):
    ax1.spines[sp].set_visible(False)
ax1.set_box_aspect(1)
for (cx, col) in ((0.38, RED), (0.62, BLUE)):
    ax2.add_patch(plt.Circle((cx, 0.5), 0.27, fc=col, alpha=0.18,
                             ec=col, lw=1.4))
ax2.text(0.24, 0.83, "AI-for-SE", fontsize=11, color=RED,
         ha="center")
ax2.text(0.76, 0.83, "human/social", fontsize=11, color=BLUE,
         ha="center")
ax2.text(0.28, 0.5, str(len(ids["ai4se"]) - len(both)),
         fontsize=12, ha="center", color=INK)
ax2.text(0.72, 0.5, str(len(ids["human"]) - len(both)),
         fontsize=12, ha="center", color=INK)
ax2.text(0.5, 0.5, str(len(both)), fontsize=13,
         fontweight="bold", ha="center", color=INK)
ax2.text(0.5, 0.13, "wing queries, SE venues only",
         fontsize=9.5, ha="center", color=INK)
ax2.set_xlim(0, 1)
ax2.set_ylim(0, 1)
ax2.set_aspect("equal")
ax2.axis("off")
plt.savefig("fig/lit.png", dpi=300, facecolor=BG,
            bbox_inches="tight", pad_inches=0.02)

# ---------- fig/lit2.png: coded venn of reading set ----------
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
    ax.text(x, y, str(R[k]), fontsize=12, ha="center", color=INK)
ax.text(0.5, 0.06,
        "reading set: %d papers; coded %d; %d matched no flag" %
        (len(top), n_abs, R["none"]),
        fontsize=9.5, ha="center", color=INK)
ax.set_xlim(0, 1)
ax.set_ylim(0, 1)
ax.set_aspect("equal")
ax.axis("off")
fig2.savefig("fig/lit2.png", dpi=300, facecolor=BG,
             bbox_inches="tight", pad_inches=0.02)

# ---------- fig/littab.tex ----------
def esc(x):
    for a, b in (("\\", ""), ("&", "\\&"), ("%", "\\%"),
                 ("#", "\\#"), ("_", "\\_"), ("$", "\\$")):
        x = x.replace(a, b)
    return x


def first_author(w):
    a = w.get("authorships") or []
    return (a[0]["author"]["display_name"].split()[-1]
            if a else "?")


def mark(w, s):
    return "$\\bullet$" if w["id"] in s else ""


with open("fig/littab.tex", "w") as f:
    f.write("% generated by litfig.py; do not hand-edit\n")
    f.write("\\begin{tabular}"
            "{@{}rp{0.5\\linewidth}p{0.16\\linewidth}rrccc@{}}\n"
            "\\toprule\n\\# & paper & venue & year & cites & "
            "trust & productivity & human studies\\\\\n"
            "\\midrule\n")
    for i, w in enumerate(top):
        ttl = esc(w["title"] or "?")
        ttl = ttl[:48] + ("..." if len(ttl) > 48 else "")
        f.write("%d & %s (%s) & %s & %d & %d & %s & %s & %s\\\\\n" %
                (i + 1, ttl, esc(first_author(w)),
                 esc(venue(w))[:22],
                 w.get("publication_year") or 0,
                 w["cited_by_count"],
                 mark(w, T), mark(w, P), mark(w, H)))
    f.write("\\bottomrule\n\\end{tabular}\n")

# ---------- fig/litnums.tex ----------
with open("fig/litnums.tex", "w") as f:
    f.write("% generated by litfig.py; do not hand-edit\n")
    for k, val in (
            ("litFetched", fetched["cross"]),
            ("litSE", n),
            ("litKnee", knee + 1),
            ("litKneeCites", cites[knee]),
            ("litWingA", len(ids["ai4se"])),
            ("litWingB", len(ids["human"])),
            ("litBoth", len(both)),
            ("litAbs", n_abs),
            ("litTPH", R["TPH"]),
            ("litNone", R["none"]),
            ("litRefs", len(refs)),
            ("litClassics", classics),
            ("litCiting", len(citing)),
            ("litOwn", own)):
        f.write("\\newcommand{\\%s}{%s}\n" % (k, "{:,}".format(val)))

print("fetched", fetched, "| SE cross", n, "| knee", knee + 1,
      "at", cites[knee], "| wings", len(ids["ai4se"]),
      len(ids["human"]), "both", len(both), "| coded", n_abs, R,
      "| refs", len(refs), "classics", classics,
      "citing", len(citing), "own", own)
