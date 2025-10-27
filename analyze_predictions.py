# analyze_predictions.py
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

LOG_FILE = "data/predictions_log.csv"

if not os.path.exists(LOG_FILE):
    print("No predictions_log.csv found. Run some uploads first.")
    exit()

df = pd.read_csv(LOG_FILE)

# Bar chart: Parkinson's vs Non-Parkinson's
plt.figure(figsize=(6, 4))
sns.countplot(x="parkinson_detected", data=df)
plt.title("Prediction Counts")
plt.xlabel("Parkinson Detected")
plt.ylabel("Count")
plt.savefig("data/prediction_counts.png")
plt.close()

# Histogram: Confidence scores
plt.figure(figsize=(6, 4))
sns.histplot(df["confidence"], bins=10, kde=True)
plt.title("Confidence Score Distribution")
plt.xlabel("Confidence")
plt.ylabel("Frequency")
plt.savefig("data/confidence_distribution.png")
plt.close()

# Scatter plot: Jitter vs Shimmer
plt.figure(figsize=(6, 4))
sns.scatterplot(x="jitter", y="shimmer", hue="parkinson_detected", data=df)
plt.title("Jitter vs Shimmer")
plt.xlabel("Jitter")
plt.ylabel("Shimmer")
plt.legend(title="Parkinson Detected")
plt.savefig("data/jitter_vs_shimmer.png")
plt.close()

print("✅ Visualizations saved in data/:")
print("- prediction_counts.png")
print("- confidence_distribution.png")
print("- jitter_vs_shimmer.png")