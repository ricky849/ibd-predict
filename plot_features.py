import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv("data/daily_features.csv")
df['date'] = pd.to_datetime(df['date'])

fig, (ax1, ax2, ax3) = plt.subplots(3, 1, figsize=(14, 10), sharex=True)

ax1.plot(df['date'], df['avg_rhr'], color='lightcoral', alpha=0.5, label='Daily RHR')
ax1.plot(df['date'], df['rhr_7day_avg'], color='red', linewidth=2, label='7-Day Avg')
ax1.set_ylabel("Resting HR (BPM)")
ax1.set_title("4-Year IBD Telemetry Trends (2020 - 2024)")
ax1.grid(True, linestyle='--')
ax1.legend()

ax2.plot(df['date'], df['avg_hrv'], color='skyblue', alpha=0.5, label='Daily HRV')
ax2.plot(df['date'], df['hrv_7day_avg'], color='blue', linewidth=2, label='7-Day Avg')
ax2.set_ylabel("HRV (ms)")
ax2.grid(True, linestyle='--')
ax2.legend()

ax3.plot(df['date'], df['total_steps'], color='lightgreen', alpha=0.5, label='Daily Steps')
avg_steps = df['total_steps'].mean()
ax3.axhline(y=avg_steps, color='black', linestyle=':', label=f'Average ({avg_steps:,.0f} steps)')

ax3.set_ylabel("Steps / Day")
ax3.grid(True, linestyle='--')
ax3.legend()

plt.tight_layout()
plt.savefig("assets/multi_year_trends.png", dpi=300)
print("Saved plot to assets/multi_year_trends.png")
plt.show()

plt.show()