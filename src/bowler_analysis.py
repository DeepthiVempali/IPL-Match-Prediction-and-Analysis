import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

sns.set_style("whitegrid")

print("========== IPL BOWLER ANALYSIS ==========\n")

# Load dataset
deliveries = pd.read_csv("data/processed/deliveries_cleaned.csv")
matches = pd.read_csv("data/processed/matches_cleaned.csv")
print("Dataset Loaded Successfully!")
print("Shape:", deliveries.shape)

print("\nColumns:\n")
print(deliveries.columns)

# ============================================
# TOP 10 WICKET TAKERS
# ============================================

# Count only actual wickets (exclude run outs)
wickets = deliveries[
    (deliveries["is_wicket"] == 1) &
    (deliveries["dismissal_kind"] != "run out")
]

top_wickets = (
    wickets.groupby("bowler")["is_wicket"]
    .sum()
    .sort_values(ascending=False)
    .head(10)
)

print("\n========== TOP 10 WICKET TAKERS ==========\n")
print(top_wickets)

# Plot graph
plt.figure(figsize=(10,6))

top_wickets.plot(
    kind="bar",
    color="purple"
)

plt.title("Top 10 IPL Wicket Takers")
plt.xlabel("Bowler")
plt.ylabel("Wickets")

plt.xticks(rotation=45)

plt.tight_layout()

plt.show()

# ============================================
# BEST ECONOMY RATE
# ============================================

# Total runs conceded by each bowler
runs_given = deliveries.groupby("bowler")["total_runs"].sum()

# Total balls bowled by each bowler
balls_bowled = deliveries.groupby("bowler").size()

# Filter bowlers with at least 300 balls bowled
qualified = balls_bowled[balls_bowled >= 300].index

economy = (
    (runs_given[qualified] / (balls_bowled[qualified] / 6))
    .sort_values()
    .head(10)
)

print("\n========== BEST ECONOMY RATE ==========\n")
print(economy)

# Plot
plt.figure(figsize=(10,6))

economy.plot(
    kind="bar",
    color="orange"
)

plt.title("Top 10 Best Economy Rates")
plt.xlabel("Bowler")
plt.ylabel("Economy Rate")

plt.xticks(rotation=45)

plt.tight_layout()

plt.show()
# ============================================
# BEST BOWLING STRIKE RATE
# ============================================

# Count wickets (excluding run outs)
wickets = deliveries[
    (deliveries["is_wicket"] == 1) &
    (deliveries["dismissal_kind"] != "run out")
]

wicket_count = wickets.groupby("bowler")["is_wicket"].sum()

# Balls bowled
balls_bowled = deliveries.groupby("bowler").size()

# Bowlers with at least 30 wickets
qualified = wicket_count[wicket_count >= 30].index

strike_rate = (
    balls_bowled[qualified] / wicket_count[qualified]
).sort_values().head(10)

print("\n========== BEST BOWLING STRIKE RATE ==========\n")
print(strike_rate)

# Plot
plt.figure(figsize=(10,6))

strike_rate.plot(
    kind="bar",
    color="darkgreen"
)

plt.title("Top 10 Bowling Strike Rates")
plt.xlabel("Bowler")
plt.ylabel("Balls per Wicket")

plt.xticks(rotation=45)

plt.tight_layout()

plt.show()

# ============================================
# MOST DOT BALLS
# ============================================

dot_balls = deliveries[
    (deliveries["batsman_runs"] == 0) &
    (deliveries["extra_runs"] == 0)
]

top_dot_balls = (
    dot_balls.groupby("bowler")
    .size()
    .sort_values(ascending=False)
    .head(10)
)

print("\n========== TOP 10 DOT BALL BOWLERS ==========\n")
print(top_dot_balls)

# Plot
plt.figure(figsize=(10,6))

top_dot_balls.plot(
    kind="bar",
    color="steelblue"
)

plt.title("Top 10 Bowlers by Dot Balls")
plt.xlabel("Bowler")
plt.ylabel("Dot Balls")

plt.xticks(rotation=45)

plt.tight_layout()

plt.show()

# ============================================
# MOST MAIDEN OVERS
# ============================================

# Runs conceded in each over
over_runs = (
    deliveries.groupby(["match_id", "inning", "bowler", "over"])["total_runs"]
    .sum()
    .reset_index()
)

# Overs with 0 runs
maidens = over_runs[over_runs["total_runs"] == 0]

maiden_count = (
    maidens.groupby("bowler")
    .size()
    .sort_values(ascending=False)
    .head(10)
)

print("\n========== TOP 10 MAIDEN OVER BOWLERS ==========\n")
print(maiden_count)

# Plot
plt.figure(figsize=(10,6))

maiden_count.plot(
    kind="bar",
    color="teal"
)

plt.title("Top 10 Maiden Over Bowlers")
plt.xlabel("Bowler")
plt.ylabel("Maiden Overs")

plt.xticks(rotation=45)

plt.tight_layout()

plt.show()

# ============================================
# PURPLE CAP WINNERS
# ============================================

# Merge deliveries with matches to get season
merged = deliveries.merge(
    matches[["id", "season"]],
    left_on="match_id",
    right_on="id"
)

# Count only wickets credited to bowlers
season_wickets = merged[
    (merged["is_wicket"] == 1) &
    (merged["dismissal_kind"] != "run out")
]

season_wickets = (
    season_wickets
    .groupby(["season", "bowler"])["is_wicket"]
    .sum()
    .reset_index()
)

# Find highest wicket-taker each season
purple_cap = season_wickets.loc[
    season_wickets.groupby("season")["is_wicket"].idxmax()
]

print("\n========== PURPLE CAP WINNERS ==========\n")
print(purple_cap.to_string(index=False))
# ============================================
# INDIVIDUAL BOWLER ANALYSIS
# ============================================

bowler = input("\nEnter Bowler Name: ").strip()

bowler_data = deliveries[deliveries["bowler"] == bowler]

if bowler_data.empty:
    print("\nBowler not found!")
    exit()

print("\nBowler Found:", bowler)

# Total wickets (excluding run outs)
wickets = bowler_data[
    (bowler_data["is_wicket"] == 1) &
    (bowler_data["dismissal_kind"] != "run out")
].shape[0]

# Balls bowled
balls = len(bowler_data)

# Runs conceded
runs = bowler_data["total_runs"].sum()

# Economy
economy = (runs / balls) * 6

# Strike Rate
if wickets > 0:
    strike_rate = balls / wickets
    average = runs / wickets
else:
    strike_rate = 0
    average = 0

# Dot Balls
dot_balls = bowler_data[
    (bowler_data["batsman_runs"] == 0) &
    (bowler_data["extra_runs"] == 0)
].shape[0]

print("\n========== CAREER STATS ==========")
print("Balls Bowled :", balls)
print("Runs Conceded :", runs)
print("Wickets :", wickets)
print("Dot Balls :", dot_balls)
print("Economy :", round(economy, 2))
print("Strike Rate :", round(strike_rate, 2))
print("Bowling Average :", round(average, 2))
# ============================================
# SEASON-WISE WICKETS
# ============================================

# Merge deliveries with matches to get season
merged = deliveries.merge(
    matches[["id", "season"]],
    left_on="match_id",
    right_on="id"
)

bowler_season = merged[
    (merged["bowler"] == bowler) &
    (merged["is_wicket"] == 1) &
    (merged["dismissal_kind"] != "run out")
]

season_wickets = (
    bowler_season
    .groupby("season")["is_wicket"]
    .sum()
)

print("\n========== SEASON-WISE WICKETS ==========\n")
print(season_wickets)

# Plot
plt.figure(figsize=(12,6))

season_wickets.plot(
    kind="line",
    marker="o",
    linewidth=3
)

plt.title(f"{bowler} - Season-wise Wickets")
plt.xlabel("Season")
plt.ylabel("Wickets")

plt.xticks(rotation=45)

plt.grid(True)

plt.tight_layout()

plt.show()
# ============================================
# BEST BOWLING VENUES
# ============================================

venue_data = deliveries.merge(
    matches[["id", "venue"]],
    left_on="match_id",
    right_on="id"
)

bowler_venue = venue_data[
    (venue_data["bowler"] == bowler) &
    (venue_data["is_wicket"] == 1) &
    (venue_data["dismissal_kind"] != "run out")
]

venue_wickets = (
    bowler_venue.groupby("venue")["is_wicket"]
    .sum()
    .sort_values(ascending=False)
    .head(10)
)

print("\n========== TOP 10 BOWLING VENUES ==========\n")
print(venue_wickets)

# Plot
plt.figure(figsize=(12,6))

venue_wickets.plot(
    kind="bar",
    color="darkorange"
)

plt.title(f"{bowler} - Wickets by Venue")
plt.xlabel("Venue")
plt.ylabel("Wickets")

plt.xticks(rotation=75)

plt.tight_layout()

plt.show()
# ============================================
# WICKETS AGAINST TEAMS
# ============================================

team_wickets = deliveries[
    (deliveries["bowler"] == bowler) &
    (deliveries["is_wicket"] == 1) &
    (deliveries["dismissal_kind"] != "run out")
]

team_wickets = (
    team_wickets.groupby("batting_team")["is_wicket"]
    .sum()
    .sort_values(ascending=False)
)

print("\n========== WICKETS AGAINST TEAMS ==========\n")
print(team_wickets)

# Plot
plt.figure(figsize=(12,6))

team_wickets.plot(
    kind="bar",
    color="crimson"
)

plt.title(f"{bowler} - Wickets Against Teams")
plt.xlabel("Batting Team")
plt.ylabel("Wickets")

plt.xticks(rotation=45)

plt.tight_layout()

plt.show()
# ============================================
# HOME vs AWAY BOWLING PERFORMANCE
# ============================================

# Merge with match details
bowler_matches = deliveries.merge(
    matches[["id", "team1", "team2"]],
    left_on="match_id",
    right_on="id"
)

# Selected bowler
bowler_data = bowler_matches[
    bowler_matches["bowler"] == bowler
]

# Home wickets
home_wickets = bowler_data[
    (bowler_data["bowling_team"] == bowler_data["team1"]) &
    (bowler_data["is_wicket"] == 1) &
    (bowler_data["dismissal_kind"] != "run out")
].shape[0]

# Away wickets
away_wickets = bowler_data[
    (bowler_data["bowling_team"] == bowler_data["team2"]) &
    (bowler_data["is_wicket"] == 1) &
    (bowler_data["dismissal_kind"] != "run out")
].shape[0]

print("\n========== HOME vs AWAY WICKETS ==========\n")
print("Home Wickets :", home_wickets)
print("Away Wickets :", away_wickets)

# Plot
plt.figure(figsize=(6,6))

plt.bar(
    ["Home", "Away"],
    [home_wickets, away_wickets]
)

plt.title(f"{bowler} - Home vs Away Wickets")
plt.ylabel("Wickets")

plt.tight_layout()

plt.show()