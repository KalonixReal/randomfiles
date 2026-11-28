# -*- coding: utf-8 -*-
"""Report figures: precision-recall operating points and false-alert comparison."""
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import json

plt.rcParams["font.sans-serif"] = ["DejaVu Sans"]
plt.rcParams["axes.unicode_minus"] = False

# ---- Figure 1: precision-recall operating points (test split)
pts = [
    ("No-change baseline", 0.0, 0.0, "#999999", "x"),
    ("Harper (raw)", 0.333, 0.257, "#7f8c8d", "o"),
    ("Harper (filtered)", 0.500, 0.228, "#16a085", "o"),
    ("Existing T5 model", 0.283, 0.584, "#e67e22", "s"),
    ("Original build (Harper+T5)", 0.278, 0.640, "#c0392b", "D"),
    ("Rules only", 0.471, 0.234, "#2980b9", "o"),
    ("Trained tagger@0.98", 0.486, 0.167, "#8e44ad", "o"),
    ("JS engine (rules+tagger@0.995)", 0.475, 0.273, "#2471a3", "o"),
    ("Harper_f + rules (no tagger)", 0.571, 0.343, "#117a65", "o"),
    ("SHIPPED build (Harper_f + engine)", 0.444, 0.338, "#1a5276", "*"),
    ("GLM (standard prompt)", 0.628, 0.800, "#d4ac0d", "^"),
    ("GLM (strict prompt)", 0.664, 0.811, "#b7950b", "^"),
]
fig, ax = plt.subplots(figsize=(7.4, 5.4), constrained_layout=True)
for name, p, r, c, m in pts:
    ms = 230 if m == "*" else 90
    ax.scatter(r, p, c=c, marker=m, s=ms, edgecolors="white", linewidths=0.7, zorder=3)
    dx, dy = 0.012, 0.008
    if "GLM" in name:
        dx, dy = -0.34, 0.012
    if name == "Original build (Harper+T5)":
        dy = -0.03
    ax.annotate(name, (r + dx, p + dy), fontsize=7.6, color="#333333")
ax.set_xlabel("Recall (span-level, equivalent-effect matching)", fontsize=9.5)
ax.set_ylabel("Precision", fontsize=9.5)
ax.set_title("Precision\u2013recall operating points on the held-out test split (202 erroneous,\n281 correct, 89 adversarial sentences)", fontsize=10.5)
ax.grid(True, alpha=0.28, zorder=0)
ax.set_xlim(-0.04, 0.98)
ax.set_ylim(-0.04, 0.88)
fig.savefig("/home/z/my-project/scripts/report_fig_pr.png", dpi=150)
print("PR figure saved")

# ---- Figure 2: false-alert rate on correct sentences
labels = ["Original build\n(Harper+T5)", "Existing T5\nmodel", "GLM\n(both prompts)", "Harper\n(raw)", "SHIPPED\nbuild", "JS engine\n@0.995", "Harper_f+\nrules", "Harper\n(filtered)"]
vals = [48.8, 44.1, 34.0, 17.4, 12.1, 7.8, 5.3, 4.3]
colors = ["#c0392b", "#e67e22", "#b7950b", "#7f8c8d", "#1a5276", "#2471a3", "#117a65", "#16a085"]
fig2, ax2 = plt.subplots(figsize=(7.4, 4.6), constrained_layout=True)
bars = ax2.bar(labels, vals, color=colors, width=0.62, zorder=3)
ax2.axhline(5.0, color="#c0392b", linestyle="--", linewidth=1.1, zorder=2)
ax2.text(6.9, 6.4, "5% target", fontsize=8, color="#c0392b", ha="center")
for b, v in zip(bars, vals):
    ax2.text(b.get_x() + b.get_width() / 2, v + 0.9, f"{v:.1f}%", ha="center", fontsize=8.2)
ax2.set_ylabel("False-alert rate on correct sentences (%)", fontsize=9.5)
ax2.set_title("False-alert rate by system (clean-sentence sets, same evaluation)", fontsize=10.5)
ax2.tick_params(axis="x", labelsize=7.6)
ax2.grid(True, axis="y", alpha=0.25, zorder=0)
ax2.set_ylim(0, 56)
fig2.savefig("/home/z/my-project/scripts/report_fig_fa.png", dpi=150)
print("FA figure saved")
