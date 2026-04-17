#!/usr/bin/env python3
"""Generate all website visuals for WindstormInstitute.org"""
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

matplotlib.rcParams.update({
    'font.size': 13, 'axes.labelsize': 14, 'axes.titlesize': 16,
    'figure.dpi': 200, 'savefig.dpi': 300, 'savefig.bbox': 'tight',
    'font.family': 'sans-serif',
    'axes.facecolor': '#0a0a1a', 'figure.facecolor': '#0a0a1a',
    'text.color': '#e0e0e0', 'axes.labelcolor': '#e0e0e0',
    'xtick.color': '#999999', 'ytick.color': '#999999',
})

import os, sys
OUT = sys.argv[1] if len(sys.argv) > 1 else '.'
os.makedirs(OUT, exist_ok=True)

# === VISUAL 1: Hero Convergence ===
fig, ax = plt.subplots(figsize=(14, 7))
ax.axhspan(3, 6, alpha=0.12, color='#00d4ff', zorder=0)
ax.axhline(4.16, color='#00d4ff', alpha=0.4, linestyle='--', linewidth=1)
systems = [
    ('Ribosome\n(tRNA)', 4.39, '#ff4444', 'o', 200),
    ('English\nConsonants', 4.20, '#44aaff', 's', 180),
    ('Chromatic\nScale', 3.58, '#ffaa44', 'D', 160),
    ('Neural\nWorking Memory', 3.12, '#aa44ff', '^', 180),
    ('AI Transformers\n(matched)', 4.19, '#44ff88', 'p', 200),
    ('Morse Code', 4.75, '#ff88cc', 'v', 140),
    ('TCP/IP\nPackets', 3.80, '#88ccff', 'h', 140),
]
xs = np.linspace(0.5, 6.5, len(systems))
for (n,v,c,m,s), x in zip(systems, xs):
    ax.scatter(x, v, c=c, marker=m, s=s, edgecolors='white', linewidths=1.5, zorder=5)
    ax.annotate(n, (x,v), fontsize=10, color=c, ha='center', va='bottom', xytext=(0,12), textcoords='offset points')
ax.text(6.8, 4.5, 'The Throughput\nBasin', fontsize=14, color='#00d4ff', alpha=0.6, fontstyle='italic', ha='right')
ax.text(6.8, 4.16, 'τ = 4.16 ± 0.19', fontsize=11, color='#00d4ff', alpha=0.5, ha='right', va='center')
ax.set_xlim(0, 7.2); ax.set_ylim(1.5, 6.5)
ax.set_ylabel('Effective Throughput (bits per event)'); ax.set_xticks([])
ax.set_title('Seven Systems. Six Domains. One Basin.', fontsize=18, fontweight='bold', color='white', pad=15)
for s in ['top','right','bottom']: ax.spines[s].set_visible(False)
ax.spines['left'].set_color('#333333'); ax.grid(True, axis='y', alpha=0.15, color='#444444')
plt.savefig(f'{OUT}/web_hero_convergence.png', facecolor='#0a0a1a'); plt.close()
print("1/4 Hero convergence")

# === VISUAL 2: Research Arc — REMOVED 2026-04-16 ===
# The previous generator showed only 5 papers (Paper 0-4 in legacy numbering)
# and was never referenced from any HTML. The output PNG was an orphan.
# If a research-arc visual is wanted again, regenerate with all 9 current
# papers (Fons → Receiver-Limited Floor → Throughput Basin → Serial Decoding
# Basin τ → Dissipative Decoder → Inherited Constraint → Throughput Basin
# Origin → Vision Basin → Hardware Basin) and the refined data-driven law.

# === VISUAL 3: Carnot Analogy ===
fig, (a1,a2) = plt.subplots(1, 2, figsize=(14, 6))
temps = np.linspace(300, 800, 100); eta = 1 - 300/temps
a1.plot(temps, eta*100, color='#ff6644', linewidth=3); a1.fill_between(temps, eta*100, alpha=0.15, color='#ff6644')
a1.set_xlabel('Hot Reservoir Temperature (K)'); a1.set_ylabel('Maximum Efficiency (%)')
a1.set_title('Carnot Limit\nNo heat engine can exceed this', color='#ff6644', fontsize=13)
a1.set_ylim(0, 105); a1.grid(True, alpha=0.15, color='#444444')
a1.text(600, 30, 'FORBIDDEN\nZONE', fontsize=16, color='#ff6644', alpha=0.3, ha='center', fontweight='bold')
for s in ['top','right']: a1.spines[s].set_visible(False)
for s in ['left','bottom']: a1.spines[s].set_color('#333333')
Mv = np.linspace(4, 80, 200); U = np.log2(Mv) - 0.01 * Mv**1.5
a2.plot(Mv, U, color='#44aaff', linewidth=3); a2.fill_between(Mv, U, where=(U>3)&(U<6), alpha=0.15, color='#44aaff')
a2.axhline(3, color='#44aaff', ls='--', alpha=0.3); a2.axhline(6, color='#44aaff', ls='--', alpha=0.3)
a2.axvline(21, color='#ff4444', ls=':', alpha=0.6, lw=2); a2.text(21, -3, 'Ribosome\nM = 21', ha='center', color='#ff4444', fontsize=10)
a2.scatter([Mv[np.argmax(U)]], [max(U)], color='#44aaff', s=100, zorder=5, edgecolors='white')
a2.set_xlabel('Alphabet Size M'); a2.set_ylabel('Net Throughput (bits)')
a2.set_title('Throughput Basin\nNo serial decoder escapes this', color='#44aaff', fontsize=13)
a2.grid(True, alpha=0.15, color='#444444'); a2.text(55, 1, '3–6 bit\nbasin', fontsize=14, color='#44aaff', alpha=0.4, ha='center', fontweight='bold')
for s in ['top','right']: a2.spines[s].set_visible(False)
for s in ['left','bottom']: a2.spines[s].set_color('#333333')
fig.suptitle('Two Universal Limits on Physical Systems', fontsize=17, color='white', fontweight='bold', y=1.02)
plt.tight_layout(); plt.savefig(f'{OUT}/web_carnot_analogy.png', facecolor='#0a0a1a'); plt.close()
print("3/4 Carnot analogy")

# === VISUAL 4: Ribosome Prediction ===
fig, ax = plt.subplots(figsize=(8, 5))
bars = ax.bar(['Predicted\n(from physics)', 'Observed\n(measured)'], [4.387, 4.390], color=['#44aaff','#ff4444'], width=0.5, edgecolor='white', linewidth=1.5)
ax.set_ylim(4.0, 4.5); ax.set_ylabel('Effective Throughput (bits per codon)')
ax.set_title('The Ribosome Prediction\nΔ = 0.003 bits — no fitting, no tuning', color='white', fontsize=14, fontweight='bold')
for b,v in zip(bars,[4.387,4.390]): ax.text(b.get_x()+b.get_width()/2, v+0.005, f'{v:.3f}', ha='center', va='bottom', fontsize=16, fontweight='bold', color='white')
for s in ['top','right']: ax.spines[s].set_visible(False)
for s in ['left','bottom']: ax.spines[s].set_color('#333333')
ax.grid(True, axis='y', alpha=0.15, color='#444444')
plt.savefig(f'{OUT}/web_ribosome_prediction.png', facecolor='#0a0a1a'); plt.close()
print("4/4 Ribosome prediction")
print("ALL IMAGES GENERATED")
