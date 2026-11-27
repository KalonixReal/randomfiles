# -*- coding: utf-8 -*-
"""Report figures for the v9.5.0 report (matplotlib, English labels)."""
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm

fm.fontManager.addfont('/usr/share/fonts/truetype/chinese/NotoSansSC-Regular.ttf')
plt.rcParams['font.sans-serif'] = ['Noto Sans SC', 'DejaVu Sans']
plt.rcParams['axes.unicode_minus'] = False

# ---- Figure 1: precision/recall locations (test + subset)
fig, ax = plt.subplots(figsize=(7.2, 4.4), constrained_layout=True)
points = [
    ("1  Original build (Harper+T5), full test", 0.278, 0.640, "#c0504d", "o"),
    ("2  Shipped v9.5.0, full test", 0.707, 0.507, "#147d64", "s"),
    ("3  Shipped v9.5.0, GLM subset", 0.687, 0.594, "#147d64", "D"),
    ("4  GLM standard prompt, subset", 0.708, 0.562, "#2d5f9a", "^"),
    ("5  GLM careful prompt, subset", 0.698, 0.578, "#2d5f9a", "v"),
]
for label, p, r, c, mk in points:
    n = label.split()[0]
    ax.scatter(r, p, color=c, marker=mk, s=100, zorder=3, edgecolor="white", linewidth=0.8, label=label)
    ax.annotate(n, (r, p), xytext=(r - 0.012, p + 0.012), fontsize=9, fontweight="bold", color=c)
ax.plot([0, 1], [0, 1], ls=":", lw=0.8, color="#bbb")
ax.set_xlabel("Recall (edit-level, equivalent-effect matcher)")
ax.set_ylabel("Precision")
ax.set_xlim(0.22, 0.80)
ax.set_ylim(0.22, 0.80)
ax.set_title("Precision–recall locations (numbered; legend right)")
ax.legend(loc="center left", bbox_to_anchor=(1.01, 0.5), fontsize=8.5, frameon=False)
ax.grid(alpha=0.25, ls="--")
fig.savefig("/home/z/my-project/scripts/report_fig_pr2.png", dpi=170, bbox_inches="tight", bbox_extra_artists=[ax.get_legend()])
plt.close(fig)

# ---- Figure 2: false-alert + meaning violations bar chart
fig, ax = plt.subplots(figsize=(7.2, 4.0), constrained_layout=True)
systems = ["Original\n(Harper+T5)", "GLM standard\n(subset)", "GLM strict\n(subset)", "Shipped\nv9.5.0"]
fa = [48.8, 24.2, 24.2, 7.6]
mv = [35, None, None, 0]
colors = ["#c0504d", "#2d5f9a", "#2d5f9a", "#147d64"]
bars = ax.bar(systems, fa, color=colors, width=0.55)
for b, v in zip(bars, fa):
    ax.text(b.get_x() + b.get_width() / 2, v + 1.0, f"{v:.1f}%", ha="center", fontsize=9)
ax.set_ylabel("Clean-sentence false-alert rate (%)")
ax.set_title("False alerts on correct sentences (lower is better)")
ax.set_ylim(0, 58)
ax.grid(axis="y", alpha=0.25, ls="--")
fig.savefig("/home/z/my-project/scripts/report_fig_fa2.png", dpi=170)
plt.close(fig)

# ---- Figure 3: engine-level progression dev
fig, ax = plt.subplots(figsize=(7.2, 4.0), constrained_layout=True)
stages = ["Rules v1\n(46 rules)", "Rules v2\n(110 rules)", "Rules v2 +\nHarper(f)", "Shipped\n(+tagger 0.995)"]
f05 = [0.580, 0.884, 0.781, 0.878]
bars = ax.bar(stages, f05, color=["#8fb8c9", "#147d64", "#7c9eb8", "#3f9b7f"], width=0.55)
for b, v in zip(bars, f05):
    ax.text(b.get_x() + b.get_width() / 2, v + 0.012, f"{v:.3f}", ha="center", fontsize=9)
ax.set_ylabel("F0.5 (development split)")
ax.set_title("Engine-level F0.5 progression on the development split")
ax.set_ylim(0, 1.02)
ax.grid(axis="y", alpha=0.25, ls="--")
fig.savefig("/home/z/my-project/scripts/report_fig_prog.png", dpi=170)
plt.close(fig)
print("figures written: report_fig_pr2.png, report_fig_fa2.png, report_fig_prog.png")
