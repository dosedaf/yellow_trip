import pandas as pd

df = pd.read_parquet("data/yellow_tripdata_2025-01.parquet")

df.to_csv(('output.csv'), index=False)
