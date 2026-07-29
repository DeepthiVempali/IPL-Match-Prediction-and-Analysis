import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Improve graph appearance
sns.set_style("whitegrid")

print("========== IPL BATSMAN ANALYSIS ==========")

# Load cleaned deliveries dataset
deliveries = pd.read_csv("data/processed/deliveries_cleaned.csv")
matches = pd.read_csv("data/processed/matches_cleaned.csv")

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

print("\n========== TOP 10 SIX HITTERS ==========\n")

top_sixes = (
    deliveries[deliveries["batsman_runs"] == 6]
    .groupby("batter")
    .size()
    .sort_values(ascending=False)
    .head(10)
)

print(top_sixes)

plt.figure(figsize=(12,6))

top_sixes.plot(kind="bar", color="orange")

plt.title("Top 10 Six Hitters in IPL")
plt.xlabel("Batsman")
plt.ylabel("Number of Sixes")

plt.xticks(rotation=45)
plt.tight_layout()
plt.show()
print("\n========== TOP 10 FOUR HITTERS ==========\n")

top_fours = (
    deliveries[deliveries["batsman_runs"] == 4]
    .groupby("batter")
    .size()
    .sort_values(ascending=False)
    .head(10)
)

print(top_fours)

plt.figure(figsize=(12,6))

top_fours.plot(kind="bar", color="green")

plt.title("Top 10 Four Hitters in IPL")
plt.xlabel("Batsman")
plt.ylabel("Number of Fours")

plt.xticks(rotation=45)
plt.tight_layout()
plt.show()
print("\n========== TOP 10 STRIKE RATES ==========\n")

balls_faced = deliveries.groupby("batter").size()
runs_scored = deliveries.groupby("batter")["batsman_runs"].sum()

strike_rate = (runs_scored / balls_faced) * 100

strike_rate = strike_rate[balls_faced >= 500]
strike_rate = strike_rate.sort_values(ascending=False).head(10)

print(strike_rate)

plt.figure(figsize=(12,6))

strike_rate.plot(kind="bar", color="purple")

plt.title("Top 10 Strike Rates (Minimum 500 Balls)")
plt.xlabel("Batsman")
plt.ylabel("Strike Rate")

plt.xticks(rotation=45)
plt.tight_layout()
plt.show()
print("\n========== TOP 10 BATTING AVERAGES ==========\n")

# Total runs
runs = deliveries.groupby("batter")["batsman_runs"].sum()

# Number of dismissals
dismissals = (
    deliveries[deliveries["player_dismissed"] == deliveries["batter"]]
    .groupby("batter")
    .size()
)

# Batting average
batting_average = runs / dismissals

# Remove NaN values
batting_average = batting_average.dropna()

# Consider only batsmen with at least 1000 runs
batting_average = batting_average[runs >= 1000]

# Top 10
top_average = batting_average.sort_values(ascending=False).head(10)

print(top_average)

# Plot
plt.figure(figsize=(12,6))

top_average.plot(kind="bar", color="crimson")

plt.title("Top 10 Batting Averages in IPL")
plt.xlabel("Batsman")
plt.ylabel("Batting Average")

plt.xticks(rotation=45)
plt.tight_layout()
plt.show()
print("\n========== SEASON-WISE RUNS ==========\n")

# Merge deliveries with matches
merged_data = deliveries.merge(
    matches[["id", "season"]],
    left_on="match_id",
    right_on="id"
)

# Runs scored each season
season_runs = (
    merged_data.groupby("season")["batsman_runs"]
    .sum()
)

print(season_runs)

# Plot
plt.figure(figsize=(12,6))

season_runs.plot(
    kind="line",
    marker="o",
    linewidth=3
)

plt.title("Total Runs Scored in Each IPL Season")
plt.xlabel("Season")
plt.ylabel("Runs")

plt.grid(True)

plt.tight_layout()

plt.show()

print("\n========== TOP 10 CENTURY SCORERS ==========\n")

# Runs scored by each batter in each match
match_runs = deliveries.groupby(
    ["match_id", "batter"]
)["batsman_runs"].sum()

# Filter innings with 100 or more runs
centuries = match_runs[match_runs >= 100]

# Count centuries by player
century_count = centuries.groupby("batter").size().sort_values(ascending=False)

print(century_count.head(10))

plt.figure(figsize=(12,6))

century_count.head(10).plot(kind="bar", color="gold")

plt.title("Top 10 Century Scorers in IPL")
plt.xlabel("Batsman")
plt.ylabel("Centuries")

plt.xticks(rotation=45)

plt.tight_layout()

plt.show()
print("\n========== TOP 10 HALF-CENTURY SCORERS ==========\n")

# Runs between 50 and 99 in a match
fifties = match_runs[(match_runs >= 50) & (match_runs < 100)]

# Count fifties by player
fifty_count = fifties.groupby("batter").size().sort_values(ascending=False)

print(fifty_count.head(10))

plt.figure(figsize=(12,6))

fifty_count.head(10).plot(kind="bar", color="orange")

plt.title("Top 10 Half-Century Scorers in IPL")
plt.xlabel("Batsman")
plt.ylabel("Half-Centuries")

plt.xticks(rotation=45)

plt.tight_layout()

plt.show()
print("\n========== ORANGE CAP WINNERS ==========\n")

# Merge deliveries with matches
merged = deliveries.merge(
    matches[["id", "season"]],
    left_on="match_id",
    right_on="id"
)

# Runs by player in each season
season_player_runs = (
    merged.groupby(["season", "batter"])["batsman_runs"]
    .sum()
    .reset_index()
)

# Highest run scorer of each season
orange_cap = season_player_runs.loc[
    season_player_runs.groupby("season")["batsman_runs"].idxmax()
]

orange_cap = orange_cap.sort_values("season")

print(orange_cap[["season", "batter", "batsman_runs"]].to_string(index=False))
# Plot
plt.figure(figsize=(14,6))

plt.bar(
    orange_cap["season"].astype(str),
    orange_cap["batsman_runs"]
)

plt.title("Orange Cap Winners by Season")
plt.xlabel("Season")
plt.ylabel("Runs")

plt.xticks(rotation=45)

plt.tight_layout()

plt.show()