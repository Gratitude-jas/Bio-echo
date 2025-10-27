import pandas as pd

df = pd.read_csv("data/features/features.csv")

print("📊 Total rows in CSV:", len(df))
print("🧹 Rows after dropping NaNs:", len(df.dropna()))
print("\n🔍 NaNs per column:")
print(df.isna().sum())