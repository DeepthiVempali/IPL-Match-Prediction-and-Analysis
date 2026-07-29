import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

sns.set_style("whitegrid")

# Load datasets
deliveries = pd.read_csv("data/processed/deliveries_cleaned.csv")
matches = pd.read_csv("data/processed/matches_cleaned.csv")

# DEBUG: Check venue names
print(matches["venue"].value_counts().head(15))


print("========== PLAYER ANALYSIS ==========\n")

player = input("Enter Player Name: ").strip()

# Filter deliveries for the selected player
player_data = deliveries[deliveries["batter"] == player]

if player_data.empty:
    print("Player not found!")
    exit()

print("\nPlayer Found:", player)

# Basic Statistics
total_runs = player_data["batsman_runs"].sum()
balls = len(player_data)
fours = (player_data["batsman_runs"] == 4).sum()
sixes = (player_data["batsman_runs"] == 6).sum()

print("\n========== CAREER STATS ==========")
print("Runs :", total_runs)
print("Balls Faced :", balls)
print("Fours :", fours)
print("Sixes :", sixes)
# Strike Rate
strike_rate = (total_runs / balls) * 100

print("Strike Rate :", round(strike_rate, 2))
# Number of dismissals
dismissals = player_data[
    player_data["player_dismissed"] == player
].shape[0]

# Batting Average
if dismissals > 0:
    average = total_runs / dismissals
else:
    average = total_runs

print("Dismissals :", dismissals)
print("Batting Average :", round(average, 2))
# Runs scored in each match
match_runs = player_data.groupby("match_id")["batsman_runs"].sum()

centuries = (match_runs >= 100).sum()
fifties = ((match_runs >= 50) & (match_runs < 100)).sum()

print("Centuries :", centuries)
print("Half-Centuries :", fifties)
# ============================================
# Season-wise Runs
# ============================================

# Merge deliveries with matches to get season
merged = deliveries.merge(
    matches[["id", "season"]],
    left_on="match_id",
    right_on="id"
)

# Filter selected player
player_season = merged[merged["batter"] == player]

# Runs scored in each season
season_runs = player_season.groupby("season")["batsman_runs"].sum()

print("\n========== SEASON-WISE RUNS ==========\n")
print(season_runs)

# Plot graph
plt.figure(figsize=(12,6))

season_runs.plot(
    kind="line",
    marker="o",
    linewidth=3
)

plt.title(f"{player} - Runs by Season")
plt.xlabel("Season")
plt.ylabel("Runs")

plt.xticks(rotation=45)

plt.grid(True)

plt.tight_layout()

plt.show()
# ============================================
# Best Venues
# ============================================

venue_data = deliveries.merge(
    matches[["id", "venue"]],
    left_on="match_id",
    right_on="id"
)

player_venue = venue_data[venue_data["batter"] == player]

venue_runs = (
    player_venue.groupby("venue")["batsman_runs"]
    .sum()
    .sort_values(ascending=False)
    .head(10)
)

print("\n========== TOP 10 VENUES ==========\n")
print(venue_runs)

# Plot
plt.figure(figsize=(12,6))

venue_runs.plot(
    kind="bar",
    color="green"
)

plt.title(f"{player} - Runs at Different Venues")
plt.xlabel("Venue")
plt.ylabel("Runs")

plt.xticks(rotation=75)

plt.tight_layout()

plt.show()

# ============================================
# Runs Against Each Team
# ============================================

team_runs = (
    player_data.groupby("bowling_team")["batsman_runs"]
    .sum()
    .sort_values(ascending=False)
)

print("\n========== RUNS AGAINST TEAMS ==========\n")
print(team_runs)

plt.figure(figsize=(12,6))

team_runs.plot(kind="bar")

plt.title(f"{player} - Runs Against Each Team")
plt.xlabel("Opponent")
plt.ylabel("Runs")

plt.xticks(rotation=60)

plt.tight_layout()

plt.show()

# ============================================
# Home vs Away Performance
# ============================================

home_venue = "M Chinnaswamy Stadium"

home_runs = player_venue[player_venue["venue"] == home_venue]["batsman_runs"].sum()
away_runs = player_venue[player_venue["venue"] != home_venue]["batsman_runs"].sum()

print("\n========== HOME vs AWAY ==========\n")
print("Home Runs :", home_runs)
print("Away Runs :", away_runs)

plt.figure(figsize=(6,6))

plt.pie(
    [home_runs, away_runs],
    labels=["Home", "Away"],
    autopct="%1.1f%%",
    startangle=90
)

plt.title(f"{player} - Home vs Away Runs")

plt.show()