import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Improve graph appearance
sns.set_style("whitegrid")

print("========== IPL BATSMAN ANALYSIS ==========")

# Load cleaned deliveries dataset
deliveries = pd.read_csv("data/processed/deliveries_cleaned.csv")

print("\nDataset Loaded Successfully!")
print("Shape:", deliveries.shape)
print("\nColumns in Dataset:")
print(deliveries.columns)
# ===============================
# Top 10 IPL Run Scorers
# ===============================

top_run_scorers = deliveries.groupby("batter")["batsman_runs"].sum()

top_run_scorers = top_run_scorers.sort_values(ascending=False).head(10)

print("\nTop 10 IPL Run Scorers:")
print(top_run_scorers)
plt.figure(figsize=(12,6))

top_run_scorers.plot(
    kind="bar",
    color="royalblue"
)

plt.title("Top 10 IPL Run Scorers")
plt.xlabel("Batsman")
plt.ylabel("Runs")

plt.xticks(rotation=45)

plt.tight_layout()

plt.show()