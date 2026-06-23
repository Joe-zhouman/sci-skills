"""Generate synthetic tumor volume data for evaluation."""
import numpy as np
import pandas as pd

np.random.seed(42)

groups = ['Control', 'Drug_A', 'Drug_B', 'Drug_C']
timepoints = [0, 7, 14, 21, 28]  # days
n_per_group = 8

# Growth parameters: mean tumor volume at each timepoint per group
# Control: exponential-ish growth
# Drug_A: moderate suppression
# Drug_B: strong suppression
# Drug_C: partial effect then rebound
growth_curves = {
    'Control': [100, 180, 320, 550, 850],
    'Drug_A':  [100, 150, 220, 320, 430],
    'Drug_B':  [100, 130, 155, 180, 200],
    'Drug_C':  [100, 140, 170, 250, 380],
}

rows = []
for group in groups:
    for subj in range(1, n_per_group + 1):
        base_noise = np.random.normal(0, 1) * 8  # individual baseline offset
        for i, t in enumerate(timepoints):
            mean_val = growth_curves[group][i]
            noise = np.random.normal(0, mean_val * 0.12) + base_noise * (1 + i * 0.3)
            volume = max(20, mean_val + noise)
            rows.append({
                'Subject': f'{group}_S{subj:02d}',
                'Group': group,
                'Time_days': t,
                'TumorVolume_mm3': round(volume, 1)
            })

df = pd.DataFrame(rows)
out_path = '/home/joe/Documents/repo/skill/sci-draw/sci-draw/tests/workspace/iteration-2/eval-2/with_skill/run-1/outputs/tumor_data.csv'
df.to_csv(out_path, index=False)
print(f"Saved {len(df)} rows to {out_path}")
print(f"Groups: {df['Group'].unique().tolist()}")
print(f"Subjects per group: {df.groupby('Group')['Subject'].nunique().to_dict()}")
print(f"Timepoints: {sorted(df['Time_days'].unique().tolist())}")
