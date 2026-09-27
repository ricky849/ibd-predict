import pandas as pd

# 1. Load data
df = pd.read_csv("data/health_data_clean.csv")

# 2. Filter for Resting Heart Rate
rhr_df = df[df['metric'] == 'RestingHeartRate'].copy()

# 3. Handle timestamps
rhr_df['startDate'] = pd.to_datetime(rhr_df['startDate'])
rhr_df['date'] = rhr_df['startDate'].dt.date

# 4. Aggregate by day
daily = rhr_df.groupby('date')['value'].mean().reset_index()
daily.rename(columns={'value': 'avg_resting_hr'}, inplace=True)

# 5. Ensure chronological order & calculate 7-day rolling average
daily = daily.sort_values(by='date').reset_index(drop=True)
daily['rhr_7day_avg'] = daily['avg_resting_hr'].rolling(window=7).mean()

# 6. View the results & save to CSV
print("--- FIRST 15 DAYS OF PROCESSED BIOMARKERS ---")
print(daily.head(15))

# Save this processed table for our machine learning model
daily.to_csv("data/daily_summary.csv", index=False)
print("\n Saved daily summary to 'data/daily_summary.csv'!")