import pandas as pd

# 1. Load data
df = pd.read_csv("data/health_data_clean.csv")
df['startDate'] = pd.to_datetime(df['startDate'])
df['date'] = df['startDate'].dt.date

# 2. Filter for Resting Heart Rate
rhr_df = df[df['metric'] == 'RestingHeartRate'].copy()
rhr_daily = rhr_df.groupby('date')['value'].mean().reset_index()
rhr_daily.rename(columns={'value': 'avg_rhr'}, inplace=True)

# 3. Filter for Heart Rate Variability
hrv_df = df[df['metric'] == 'HRV'].copy()
hrv_daily = hrv_df.groupby('date')['value'].mean().reset_index()
hrv_daily.rename(columns={'value': 'avg_hrv'}, inplace=True)

# 4. Filter for Steps
steps_df = df[df['metric'] == 'Steps'].copy()
steps_daily = steps_df.groupby('date')['value'].sum().reset_index()
steps_daily.rename(columns={'value': 'total_steps'}, inplace=True)

# 5. Merge the daily summaries
merged = pd.merge(rhr_daily, hrv_daily, on='date', how='outer')
merged = pd.merge(merged, steps_daily, on='date', how='outer')

# 6. Drop rows from before the Apple Watch existed (where RHR and HRV are both missing)
merged = merged.dropna(subset=['avg_rhr', 'avg_hrv'], how='all').reset_index(drop=True)

# 7. Ensure chronological order & calculate 7-day rolling averages
merged = merged.sort_values(by='date').reset_index(drop=True)
merged['rhr_7day_avg'] = merged['avg_rhr'].rolling(window=7).mean()
merged['hrv_7day_avg'] = merged['avg_hrv'].rolling(window=7).mean()

# 8. Save the merged daily features to CSV
merged.to_csv("data/daily_features.csv", index=False)
print("\n Saved daily summary to 'data/daily_features.csv'!")

# 9. Print the first 15 days of the processed biomarkers
print("--- FIRST 15 DAYS OF APPLE WATCH TELEMETRY ---")
print(merged.head(15))