"""Regenerates the diagrams shown in the README.

    pip install matplotlib
    python docs/figures/make_figures.py

The secret-phase tree is the one stored in the bomb's .data section (symbol n1 at 0x4f91f0,
32-byte nodes {value, left, right}); it was read with `objdump -s` on ej2/bomb55/bomb.
"""
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib import font_manager
from matplotlib.patches import Circle, FancyBboxPatch, Rectangle

HERE = Path(__file__).resolve().parent
for f in Path("/usr/share/fonts/lm").glob("lm*10-*.otf"):  # Latin Modern, if installed
    font_manager.fontManager.addfont(str(f))
plt.style.use(HERE / "paper.mplstyle")
C = plt.rcParams["axes.prop_cycle"].by_key()["color"]
INK, GRAY = "#1a1a1a", "#8c8c8c"
BLUE, ORANGE, LGRAY = "#dce6f2", "#f7e6c8", "#ececec"


def save(fig, name):
    fig.savefig(HERE / name, metadata={"Date": None})
    plt.close(fig)


def canvas(w, h, xmax, ymax):
    fig, ax = plt.subplots(figsize=(w, h))
    ax.set_xlim(0, xmax)
    ax.set_ylim(0, ymax)
    ax.set_aspect("equal")
    ax.axis("off")
    return fig, ax


def box(ax, x, y, w, h, text="", fc="white", ec=INK, fs=8, ls="-", lw=0.7, **kw):
    ax.add_patch(FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0,rounding_size=0.06",
                                fc=fc, ec=ec, lw=lw, ls=ls))
    if text:
        ax.text(x + w / 2, y + h / 2, text, ha="center", va="center", fontsize=fs, **kw)


def arrow(ax, p, q, color=INK, ls="-", rad=0.0, lw=0.7):
    ax.annotate("", xy=q, xytext=p, arrowprops=dict(arrowstyle="-|>", lw=lw, color=color, ls=ls, shrinkA=0,
                                                    shrinkB=0, mutation_scale=7,
                                                    connectionstyle=f"arc3,rad={rad}"))


TT = lambda s: "$\\mathtt{" + s.replace("_", "\\_").replace(" ", "\\ ") + "}$"

# ---- Figure 1: the doubly linked list of exercise 1 and its byte layout
fig, ax = canvas(7.2, 3.0, 14.4, 6.0)
ax.set_ylim(-0.35, 5.8)
ax.text(0.1, 5.55, "(a) string_proc_list with three nodes", fontsize=9, va="center")
box(ax, 0.2, 3.3, 1.7, 1.6, fc=LGRAY)
ax.text(1.05, 4.62, "list", fontsize=8, ha="center", style="italic")
for k, lab in enumerate(("first", "last")):
    box(ax, 0.35, 3.95 - k * 0.55, 1.4, 0.45, TT(lab), fs=7.5)
xs = [3.0, 6.6, 10.2]
for i, x in enumerate(xs):
    box(ax, x, 3.0, 2.8, 2.0, fc=BLUE)
    ax.text(x + 1.4, 4.75, f"node {i + 1}", fontsize=8, ha="center", style="italic")
    for k, lab in enumerate(("next", "previous", "type", "hash")):
        box(ax, x + 0.15, 4.2 - k * 0.38, 2.5, 0.33, TT(lab), fs=7)
    ax.text(x + 1.4, 2.35, f"\"{['sol', 'rigel', 'deneb'][i]}\"", fontsize=7.5, ha="center",
            bbox=dict(fc="white", ec=GRAY, lw=0.5, boxstyle="round,pad=0.25"))
    arrow(ax, (x + 1.4, 3.15), (x + 1.4, 2.6), color=GRAY)
for i in range(2):
    arrow(ax, (xs[i] + 2.65, 4.37), (xs[i + 1], 4.37), color=C[0])            # next
    arrow(ax, (xs[i + 1] + 0.15, 3.99), (xs[i] + 2.8, 3.99), color=C[1])       # previous
arrow(ax, (1.75, 4.17), (3.0, 4.5), color=C[0])
ax.plot([1.75, 2.45, 2.45, 12.6], [3.62, 3.62, 1.9, 1.9], color=C[1], lw=0.7)  # last -> node 3
arrow(ax, (12.6, 1.9), (12.6, 3.0), color=C[1])
ax.text(13.1, 4.37, "NULL", fontsize=7, va="center")
arrow(ax, (12.85, 4.37), (13.05, 4.37), color=C[0])

ax.text(0.1, 1.2, "(b) node layout used by ej1.asm", fontsize=9, va="center")
layout = [(0, 8, "next", BLUE), (8, 16, "previous", BLUE), (16, 17, "type", ORANGE), (17, 24, "padding", "white"),
          (24, 32, "hash", BLUE)]
s = 0.36  # width per byte
x0 = 3.6
for lo, hi, lab, fc in layout:
    ax.add_patch(Rectangle((x0 + lo * s, 0.15), (hi - lo) * s, 0.55, fc=fc, ec=INK, lw=0.6,
                           hatch="///" if lab == "padding" else None))
    if lab in ("next", "previous", "hash"):
        ax.text(x0 + (lo + hi) / 2 * s, 0.42, TT(lab), fontsize=7, ha="center", va="center")
    if lo % 8 == 0:
        ax.text(x0 + lo * s, 0.82, f"+{lo}", fontsize=6.5, ha="center", color="#4d4d4d")
ax.text(x0 + 32 * s, 0.82, "+32", fontsize=6.5, ha="center", color="#4d4d4d")
ax.text(x0 + 20.5 * s, 0.42, "7 B padding", fontsize=6.5, ha="center", va="center",
        bbox=dict(fc="white", ec="none", pad=0.6))
ax.annotate(TT("type") + " (uint8_t)", xy=(x0 + 16.5 * s, 0.15), xytext=(x0 + 16.5 * s - 1.6, -0.12), fontsize=7,
            va="center", ha="right", arrowprops=dict(arrowstyle="-", lw=0.5, color=INK))
ax.text(x0 - 0.15, 0.42, "string_proc_node", fontsize=7.5, ha="right", va="center")
fig.tight_layout(pad=0.2)
save(fig, "fig1-list.svg")

# ---- Figure 2: what each bomb phase checks
fig, ax = canvas(7.2, 3.3, 14.4, 6.6)
phases = [
    ("Phase 1", "string", ["strings_not_equal against", "a constant in .rodata"]),
    ("Phase 2", "two integers $a$, $b$", ["misterio$(a+b-32,\\,a,\\,b)$:", "popcount$(a+b-32)=11$", "and $a \\oplus b < 0$"]),
    ("Phase 3", "word + integer $k$", ["binary search of the word in", "palabras.txt (10 784 words);",
                                       "$k$ = sum of first letters", "visited, $401 \\leq k \\leq 799$"]),
    ("Phase 4", "6-char string", ["each char $c \\mapsto$ table[c & 0xF]", "(16-letter table);",
                                  "result must equal a", "6-letter target word"]),
]
W, H, Y = 3.25, 3.3, 2.75
for i, (name, inp, lines) in enumerate(phases):
    x = 0.15 + i * 3.55
    box(ax, x, Y, W, H, fc="white")
    ax.add_patch(Rectangle((x, Y + H - 0.55), W, 0.55, fc=BLUE, ec=INK, lw=0.7))
    ax.text(x + W / 2, Y + H - 0.28, name, ha="center", va="center", fontsize=8.5, weight="bold")
    ax.text(x + W / 2, Y + H - 0.85, "input: " + inp, ha="center", va="center", fontsize=7.3, style="italic")
    for k, ln in enumerate(lines):
        ax.text(x + W / 2, Y + H - 1.35 - k * 0.42, ln, ha="center", va="center", fontsize=7.2)
    if i < 3:
        arrow(ax, (x + W, Y + H / 2), (x + 3.55, Y + H / 2))
    ax.plot([x + W / 2, x + W / 2], [Y, Y - 0.35], color=C[1], lw=0.7, ls=(0, (3, 2)))
ax.plot([0.15 + W / 2, 0.15 + 3 * 3.55 + W / 2], [Y - 0.35, Y - 0.35], color=C[1], lw=0.7, ls=(0, (3, 2)))
arrow(ax, (3.0, Y - 0.35), (3.0, 1.75), color=C[1], ls=(0, (3, 2)))
box(ax, 1.4, 0.95, 3.2, 0.8, "explode_bomb()", fs=8, ec=C[1], fc="#f9e3df")
box(ax, 7.9, 0.15, 6.35, 1.95, fc="#f4f0f8", ec=C[3])
ax.text(11.075, 1.82, "Secret phase", ha="center", va="center", fontsize=8.5, weight="bold", color=C[3])
ax.text(11.075, 1.32, "phase_defused, after line 4: line 3 re-read as", ha="center", fontsize=7.2, va="center")
ax.text(11.075, 0.94, "\"%s %d %s\"; the extra token must equal a keyword", ha="center", fontsize=7.2, va="center")
ax.text(11.075, 0.48, "then $n \\in [1, 1001]$ with fun7(tree, $n$) $= 5$ (Figure 3)", ha="center", fontsize=7.2,
        va="center")
arrow(ax, (0.15 + 3 * 3.55 + W / 2 + 0.6, Y), (0.15 + 3 * 3.55 + W / 2 + 0.6, 2.1), color=C[3])
fig.tight_layout(pad=0.2)
save(fig, "fig2-bomb-phases.svg")

# ---- Figure 3: the secret-phase binary search tree and the path that makes fun7 return 5
tree = {36: (8, 50), 8: (6, 22), 50: (45, 107), 6: (1, 7), 22: (20, 35), 45: (40, 47), 107: (99, 1001)}
pos, level = {}, [[36], [8, 50], [6, 22, 45, 107], [1, 7, 20, 35, 40, 47, 99, 1001]]
for d, row in enumerate(level):
    for j, v in enumerate(row):
        pos[v] = ((j + 0.5) * 14.0 / len(row) + 0.2, 4.95 - d * 1.15)
path = [36, 50, 45, 47]
fig, ax = canvas(7.2, 2.75, 14.4, 5.5)
for parent, kids in tree.items():
    for side, child in zip("LR", kids):
        on = parent in path and child in path and path.index(child) == path.index(parent) + 1
        (x1, y1), (x2, y2) = pos[parent], pos[child]
        ax.plot([x1, x2], [y1, y2], color=C[1] if on else GRAY, lw=1.4 if on else 0.6, zorder=1)
        if on:
            bit = "1" if side == "R" else "0"
            ax.text((x1 + x2) / 2 + (0.25 if side == "R" else -0.25), (y1 + y2) / 2 + 0.12,
                    f"{'right' if side == 'R' else 'left'} $\\to$ {bit}", fontsize=7, color=C[1],
                    ha="left" if side == "R" else "right")
for v, (x, y) in pos.items():
    on = v in path
    ax.add_patch(Circle((x, y), 0.36, fc="#f9e3df" if on else "white", ec=C[1] if on else INK,
                        lw=1.0 if on else 0.6, zorder=2))
    ax.text(x, y, str(v), ha="center", va="center", fontsize=7.5, zorder=3)
ax.text(0.2, 0.5, "fun7(node, $n$): 0 if $n$ = value;  $2\\,f(\\mathrm{left})$ if $n$ < value;  "
        "$2\\,f(\\mathrm{right}) + 1$ if $n$ > value", fontsize=7.5, va="center")
ax.text(0.2, 0.08, "unwinding the highlighted path gives $0 \\to 1 \\to 2 \\to 5 = 101_2$", fontsize=7.5,
        va="center", color=C[1])
fig.tight_layout(pad=0.2)
save(fig, "fig3-secret-tree.svg")
