import pandas as pd

df = pd.read_csv("data/health_data_clean.csv")
rhr_only = df[df['metric'] == 'RestingHeartRate']
minimum_resting_heartbeat = rhr_only['value'].min()
maximum_resting_heartbeat = rhr_only['value'].max()
row_count = len(df)
print(f"Total records in dataset: {row_count:,}")
print(f"Minimum Resting Heart Rate: {minimum_resting_heartbeat} BPM")
print(f"Maximum Resting Heart Rate: {maximum_resting_heartbeat} BPM")