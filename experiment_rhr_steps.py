import pandas as pd

# Load daily features table
df = pd.read_csv("data/daily_features.csv")

# Find the exact row for lowest and highest Resting HR
min_rhr_row = df.loc[df['avg_rhr'].idxmin()]
max_rhr_row = df.loc[df['avg_rhr'].idxmax()]

# Overall average step count across all days
overall_avg_steps = df['total_steps'].mean()

print("--- EXPERIMENT: RHR EXTREMES VS. STEPS ---")
print(f"Overall Average Daily Steps: {overall_avg_steps:,.0f} steps/day\n")

print("1. DAY WITH LOWEST RESTING HR:")
print(f"   Date: {min_rhr_row['date']}")
print(f"   Resting HR: {min_rhr_row['avg_rhr']} BPM")
print(f"   Steps on this day: {min_rhr_row['total_steps']:,.0f} steps")
print(f"   HRV on this day: {min_rhr_row['avg_hrv']:.1f} ms\n")

print("2. DAY WITH HIGHEST RESTING HR:")
print(f"   Date: {max_rhr_row['date']}")
print(f"   Resting HR: {max_rhr_row['avg_rhr']} BPM")
print(f"   Steps on this day: {max_rhr_row['total_steps']:,.0f} steps")
print(f"   HRV on this day: {max_rhr_row['avg_hrv']:.1f} ms")