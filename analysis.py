import matplotlib
matplotlib.use('Agg')

import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import numpy as np
from scipy import stats
import csv
import os

if not os.path.exists("output_charts"):
    os.makedirs("output_charts")

HUMAN_CLR = "#6366f1"
LLM_CLR = "#f97316"
GREEN = "#22c55e"
RED = "#ef4444"
BG = "#0f1117"
CARD = "#1a1d27"
TXT = "#e2e4eb"
MUTED = "#8b8fa3"
GRID = "#2d3348"

plt.rcParams.update({
    'figure.facecolor': BG, 'axes.facecolor': CARD,
    'text.color': TXT, 'axes.labelcolor': TXT,
    'xtick.color': MUTED, 'ytick.color': MUTED,
    'axes.edgecolor': GRID, 'grid.color': GRID,
    'font.family': 'sans-serif', 'font.size': 10,
})

BAR_W = 0.35

def cohens_d(grp1, grp2):
    diff = np.array(grp1, dtype=float) - np.array(grp2, dtype=float)
    sd = np.std(diff, ddof=1)
    if sd == 0:
        return 0
    return np.mean(diff) / sd

def efect_size(d):
    d = abs(d)
    if d >= 0.8: return "Large"
    elif d >= 0.5: return "Medium"
    elif d >= 0.2: return "Small"
    return "Negligible"

data = []
with open("metrics_data.csv", "r") as f:
    reader = csv.DictReader(f)
    for row in reader:
        data.append(row)

n = len(data)
print(f"Loaded {n} test comparisons")

ids = [t["bug_id"] for t in data]
h_assert = [int(float(t["h_assertions"])) for t in data]
l_assert = [int(t["l_assertions"]) for t in data]
h_loc = [int(float(t["h_loc"])) for t in data]
l_loc = [int(t["l_loc"]) for t in data]
h_edge = [int(float(t["h_edge_cases"])) for t in data]
l_edge = [int(t["l_edge_cases"]) for t in data]
h_fault = [int(t["h_fault_detect"]) for t in data]
l_fault = [int(t["l_fault_detect"]) for t in data]
h_doc = [int(t["h_docstring"]) for t in data]
l_doc = [int(t["l_docstring"]) for t in data]
datasets = [t["dataset"] for t in data]

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10, 4))
hd = sum(h_fault)
ld = sum(l_fault)
ax1.pie([max(hd, 0.01), n-hd], labels=["Detected", "Missed"], colors=[GREEN, RED], autopct='%1.0f%%', textprops={'color': TXT, 'fontsize': 11}, startangle=90, wedgeprops={'edgecolor': BG, 'linewidth': 2})
ax1.set_title(f"Human: {hd/n*100:.0f}%", fontsize=13, fontweight='bold', color=HUMAN_CLR)
ax2.pie([ld, max(n-ld, 0.01)], labels=["Detected", "Missed"], colors=[GREEN, RED], autopct='%1.0f%%', textprops={'color': TXT, 'fontsize': 11}, startangle=90, wedgeprops={'edgecolor': BG, 'linewidth': 2})
ax2.set_title(f"LLM: {ld/n*100:.0f}%", fontsize=13, fontweight='bold', color=LLM_CLR)
plt.tight_layout()
plt.savefig("output_charts/fault_detection_pie.png", dpi=200)
plt.close()
print("saved fault_detection_pie.png")

fig, ax = plt.subplots(figsize=(10, 5))
lbls = ['Avg\nAssertions', 'Avg\nLOC', 'Avg Edge\nCases', 'Fault\nDetection %', 'Docstring\n%']
h_vals = [np.mean(h_assert), np.mean(h_loc), np.mean(h_edge), sum(h_fault)/n*100, sum(h_doc)/n*100]
l_vals = [np.mean(l_assert), np.mean(l_loc), np.mean(l_edge), sum(l_fault)/n*100, sum(l_doc)/n*100]
x = np.arange(len(lbls))
ax.bar(x-BAR_W/2, h_vals, BAR_W, label='Human', color=HUMAN_CLR, edgecolor='none', zorder=3)
ax.bar(x+BAR_W/2, l_vals, BAR_W, label='LLM', color=LLM_CLR, edgecolor='none', zorder=3)
for i in range(len(lbls)):
    ax.text(i-BAR_W/2, h_vals[i]+0.5, f'{h_vals[i]:.1f}', ha='center', va='bottom', fontsize=9, color=HUMAN_CLR, fontweight='bold')
    ax.text(i+BAR_W/2, l_vals[i]+0.5, f'{l_vals[i]:.1f}', ha='center', va='bottom', fontsize=9, color=LLM_CLR, fontweight='bold')
ax.set_xticks(x)
ax.set_xticklabels(lbls, fontsize=10)
ax.set_title(f"Overall Summary", fontsize=14, fontweight='bold', pad=12)
ax.legend(fontsize=11)
ax.grid(axis='y', alpha=0.3)
plt.tight_layout()
plt.savefig("output_charts/overall_summary.png", dpi=200)
plt.close()
print("saved overall_summary.png")

fig, ax = plt.subplots(figsize=(7, 7), subplot_kw=dict(polar=True))
cats = ['LOC', 'Assertions', 'Edge Cases', 'Documentation', 'Fault Detection']
nc = len(cats)
h_radar = [np.mean(h_loc)/4, np.mean(h_assert)/2, np.mean(h_edge)/2, sum(h_doc)/n*10, sum(h_fault)/n*10]
l_radar = [np.mean(l_loc)/4, np.mean(l_assert)/2, np.mean(l_edge)/2, sum(l_doc)/n*10, sum(l_fault)/n*10]
angles = [i/float(nc)*2*np.pi for i in range(nc)]
angles += angles[:1]
h_radar += h_radar[:1]
l_radar += l_radar[:1]
ax.plot(angles, h_radar, 'o-', linewidth=2, label='Human', color=HUMAN_CLR)
ax.fill(angles, h_radar, alpha=0.15, color=HUMAN_CLR)
ax.plot(angles, l_radar, 'o-', linewidth=2, label='LLM', color=LLM_CLR)
ax.fill(angles, l_radar, alpha=0.15, color=LLM_CLR)
ax.set_xticks(angles[:-1])
ax.set_xticklabels(cats, fontsize=10)
ax.set_title("Quality Profile", fontsize=14, fontweight='bold', pad=20)
ax.legend(loc='upper right', bbox_to_anchor=(1.3, 1.1), fontsize=11)
ax.grid(color=GRID)
plt.tight_layout()
plt.savefig("output_charts/quality_profile_radar.png", dpi=200)
plt.close()
print("saved quality_profile_radar.png")

h_ptrns = {}
l_ptrns = {}
for t in data:
    h_ptrns[t["h_pattern"]] = h_ptrns.get(t["h_pattern"], 0) + 1
    l_ptrns[t["l_pattern"]] = l_ptrns.get(t["l_pattern"], 0) + 1

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))
hp_lbls = sorted(h_ptrns.keys(), key=lambda k: h_ptrns[k], reverse=True)
hp_tot = sum(h_ptrns.values())
hp_pct = [h_ptrns[k] / hp_tot * 100 for k in hp_lbls]
ax1.barh(hp_lbls, hp_pct, color=HUMAN_CLR, edgecolor='none')
ax1.set_title("Human Patterns", fontsize=13, fontweight='bold', color=HUMAN_CLR)
ax1.set_xlabel("Percentage (%)")
for i, v in enumerate(hp_pct):
    ax1.text(v+0.5, i, f'{v:.0f}%', va='center', fontsize=11, fontweight='bold', color=TXT)

lp_lbls = sorted(l_ptrns.keys(), key=lambda k: l_ptrns[k], reverse=True)
lp_tot = sum(l_ptrns.values())
lp_pct = [l_ptrns[k] / lp_tot * 100 for k in lp_lbls]
ax2.barh(lp_lbls, lp_pct, color=LLM_CLR, edgecolor='none')
ax2.set_title("LLM Patterns", fontsize=13, fontweight='bold', color=LLM_CLR)
ax2.set_xlabel("Percentage (%)")
for i, v in enumerate(lp_pct):
    ax2.text(v+0.5, i, f'{v:.0f}%', va='center', fontsize=11, fontweight='bold', color=TXT)

plt.tight_layout()
plt.savefig("output_charts/testing_patterns.png", dpi=200)
plt.close()
print("saved testing_patterns.png")

h_line = []
l_line = []
h_branch = []
l_branch = []
for t in data:
    hlc = t.get("h_line_cov", "")
    llc = t.get("l_line_cov", "")
    if hlc and llc:
        h_line.append(float(hlc))
        l_line.append(float(llc))
    hbc = t.get("h_branch_cov", "")
    lbc = t.get("l_branch_cov", "")
    if hbc and lbc:
        h_branch.append(float(hbc))
        l_branch.append(float(lbc))

if h_line and h_branch:
    fig, ax = plt.subplots(figsize=(8, 5))
    cov_lbls = ['Avg Line\nCoverage %', 'Avg Branch\nCoverage %']
    h_avg = [np.mean(h_line), np.mean(h_branch)]
    l_avg = [np.mean(l_line), np.mean(l_branch)]
    xm = np.arange(len(cov_lbls))
    ax.bar(xm-BAR_W/2, h_avg, BAR_W, label='Human', color=HUMAN_CLR, edgecolor='none', zorder=3)
    ax.bar(xm+BAR_W/2, l_avg, BAR_W, label='LLM', color=LLM_CLR, edgecolor='none', zorder=3)
    for i in range(len(cov_lbls)):
        ax.text(i-BAR_W/2, h_avg[i]+1, f'{h_avg[i]:.1f}%', ha='center', va='bottom', fontsize=11, color=HUMAN_CLR, fontweight='bold')
        ax.text(i+BAR_W/2, l_avg[i]+1, f'{l_avg[i]:.1f}%', ha='center', va='bottom', fontsize=11, color=LLM_CLR, fontweight='bold')
    ax.set_xticks(xm)
    ax.set_xticklabels(cov_lbls, fontsize=11)
    ax.set_ylim(0, 110)
    ax.set_title("Coverage Summary", fontsize=14, fontweight='bold', pad=12)
    ax.legend(fontsize=11)
    ax.grid(axis='y', alpha=0.3)
    plt.tight_layout()
    plt.savefig("output_charts/coverage_summary.png", dpi=200)
    plt.close()
    print("saved coverage_summary.png")

print("\n" + "=" * 50)
print(f"STATS (n={n})")
print("=" * 50)

ta, pa = stats.ttest_rel(l_assert, h_assert)
tl, pl = stats.ttest_rel(l_loc, h_loc)
te, pe = stats.ttest_rel(l_edge, h_edge)
da = cohens_d(l_assert, h_assert)
dl = cohens_d(l_loc, h_loc)
de = cohens_d(l_edge, h_edge)

print(f"Assertions: t={ta:.3f}, p={pa:.4f}, d={da:.2f} ({efect_size(da)})")
print(f"LOC: t={tl:.3f}, p={pl:.4f}, d={dl:.2f} ({efect_size(dl)})")
print(f"Edge Cases: t={te:.3f}, p={pe:.4f}, d={de:.2f} ({efect_size(de)})")
print(f"Fault: Human={sum(h_fault)}/{n} ({sum(h_fault)/n*100:.0f}%), LLM={sum(l_fault)}/{n} ({sum(l_fault)/n*100:.0f}%)")

if len(h_line) > 2:
    tlc, plc = stats.ttest_rel(l_line, h_line)
    dlc = cohens_d(l_line, h_line)
    print(f"Line Cov: t={tlc:.3f}, p={plc:.4f}, d={dlc:.2f} ({efect_size(dlc)})")

if len(h_branch) > 2:
    tbc, pbc = stats.ttest_rel(l_branch, h_branch)
    dbc = cohens_d(l_branch, h_branch)
    print(f"Branch Cov: t={tbc:.3f}, p={pbc:.4f}, d={dbc:.2f} ({efect_size(dbc)})")

bp = sum(1 for d in datasets if d == "bugsinpy")
osc = sum(1 for d in datasets if d == "opensource")
cc = sum(1 for d in datasets if d == "custom")

print(f"\nCoverage: Line H={np.mean(h_line):.1f}% L={np.mean(l_line):.1f}% | Branch H={np.mean(h_branch):.1f}% L={np.mean(l_branch):.1f}%")
print(f"\nDone! Charts saved to output_charts/")
print(f"Datasets: {bp} BugsInPy + {osc} Open Source + {cc} Custom = {n} total")