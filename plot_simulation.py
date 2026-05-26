import matplotlib.pyplot as plt
import numpy as np

plt.rcParams['font.family'] = 'AR PL UKai CN'
plt.rcParams['font.size'] = 11

types = ['FICTION\n(清醒创作)', 'BLIND\n(盲信转发)', 'CORRECTION\n(辟谣)']
counts = [204, 206, 112]
colors = ['#4C72B0', '#DD8452', '#55A868']

remix_labels = ['FICTION\n(有虚构标记)', 'BLIND\n(无标记)']
remix_rates = [47.5, 40.3]

corr_labels = ['针对 BLIND\n(无标记内容)', '针对 FICTION\n(有标记内容)']
corr_counts = [72, 0]

fig, axes = plt.subplots(1, 3, figsize=(12, 4.2), gridspec_kw={'width_ratios': [1.3, 1, 1]})

ax1 = axes[0]
bars = ax1.bar(types, counts, color=colors, width=0.55, edgecolor='white', linewidth=0.5)
for bar, count in zip(bars, counts):
    ax1.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 6,
             f'{count}条\n({count/522*100:.1f}%)', ha='center', va='bottom', fontsize=9, linespacing=1.4)
ax1.set_title('三类内容产出量', fontweight='bold', fontsize=12)
ax1.set_ylabel('内容数量（条）')
ax1.set_ylim(0, 260)
ax1.spines['top'].set_visible(False)
ax1.spines['right'].set_visible(False)

ax2 = axes[1]
bars2 = ax2.bar(remix_labels, remix_rates, color=['#4C72B0', '#DD8452'], width=0.45, edgecolor='white', linewidth=0.5)
for bar, rate in zip(bars2, remix_rates):
    ax2.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.8,
             f'{rate:.1f}%', ha='center', va='bottom', fontsize=11, fontweight='bold')
ax2.set_title('二次创作率对比', fontweight='bold', fontsize=12)
ax2.set_ylabel('被继续加工的比例')
ax2.set_ylim(0, 60)
ax2.spines['top'].set_visible(False)
ax2.spines['right'].set_visible(False)

ax3 = axes[2]
bars3 = ax3.bar(corr_labels, corr_counts, color=['#55A868', '#c0392b'], width=0.45, edgecolor='white', linewidth=0.5)
ax3.text(0, 74, '72条', ha='center', va='bottom', fontsize=11, fontweight='bold', color='#55A868')
ax3.text(1, 1.5, '0条', ha='center', va='bottom', fontsize=11, fontweight='bold', color='#c0392b')
ax3.set_title('辟谣信息的目标分布', fontweight='bold', fontsize=12)
ax3.set_ylabel('辟谣内容数量（条）')
ax3.set_ylim(0, 90)
ax3.spines['top'].set_visible(False)
ax3.spines['right'].set_visible(False)

plt.tight_layout(pad=1.5)
plt.savefig('simulation_results.pdf', bbox_inches='tight', dpi=200)
plt.savefig('simulation_results.png', bbox_inches='tight', dpi=200)
print("Figures saved.")
