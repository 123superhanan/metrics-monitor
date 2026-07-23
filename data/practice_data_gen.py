import pandas as pd
import numpy as np

np.random.seed(42)
n =1000

timestamps = pd.date_range("2016-1-1",periods=n, freq="min")
cpu = np.random.normal(50, 10, n)
memory = np.random.normal(60, 15, n)
latency  = np.random.normal(200,50, n)
error_rate = np.clip(np.random.normal(2, 1, n), 0, None)  

df = pd.DataFrame({
    "timestamp": timestamps,
    "cpu": cpu,
    "memory": memory,
    "latency": latency,
    "error_rate": error_rate
})

missing_idx = np.random.choice(df.index, size=50, replace=False)
df.loc[missing_idx, "cpu"] = np.nan
df.loc[missing_idx,"latency"]= np.nan

# inject outliers (fake spikes)
outlier_idx = np.random.choice(df.index, size=15, replace=False)
df.loc[outlier_idx, "cpu"] = np.random.uniform(150, 200, 15)
df.loc[outlier_idx, "error_rate"] = np.random.uniform(150, 200, 15)



bad_time_idx = np.random.choice(df.index, size=10, replace=False)
df.loc[bad_time_idx, "timestamp"] = "2026/01/01 00:00"


df = df.sample(frac=1).reset_index(drop=True)

df.to_csv("data/raw/metricses.csv", index=False)
print(df.shape)
print(df.isna().sum())