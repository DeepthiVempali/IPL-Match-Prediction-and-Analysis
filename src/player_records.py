import pandas as pd
import matplotlib.pyplot as plt

# Load datasets
matches = pd.read_csv("data/processed/matches_cleaned.csv")
deliveries = pd.read_csv("data/processed/deliveries_cleaned.csv")

print("Dataset Loaded Successfully!")
# ============================================
# MODULE 9
# PLAYER PERFORMANCE & RECORDS
# ============================================

# ============================================
# TOP 10 RUN SCORERS
# ============================================

top_run_scorers = (
    deliveries
    .groupby("batter")["batsman_runs"]
    .sum()
    .sort_values(ascending=False)
    .head(10)
)

print("\n========== TOP 10 RUN SCORERS ==========\n")
print(top_run_scorers)

# Plot
plt.figure(figsize=(10, 6))

top_run_scorers.sort_values().plot(
    kind="barh"
)

plt.title("Top 10 IPL Run Scorers")

plt.xlabel("Runs")

plt.ylabel("Player")

plt.tight_layout()

plt.show()
# ============================================
# MOST CENTURIES
# ============================================

# Calculate runs scored by each batter in every match
player_match_runs = (
    deliveries
    .groupby(["match_id", "batter"])["batsman_runs"]
    .sum()
    .reset_index()
)

# Count centuries
centuries = (
    player_match_runs[
        player_match_runs["batsman_runs"] >= 100
    ]
    .groupby("batter")
    .size()
    .sort_values(ascending=False)
    .head(10)
)

print("\n========== MOST CENTURIES ==========\n")
print(centuries)

# Plot
plt.figure(figsize=(10, 6))

centuries.sort_values().plot(
    kind="barh"
)

plt.title("Top 10 IPL Players by Centuries")

plt.xlabel("Centuries")
plt.ylabel("Player")

plt.tight_layout()

plt.show()
# ============================================
# MOST HALF-CENTURIES
# ============================================

half_centuries = (
    player_match_runs[
        (player_match_runs["batsman_runs"] >= 50) &
        (player_match_runs["batsman_runs"] < 100)
    ]
    .groupby("batter")
    .size()
    .sort_values(ascending=False)
    .head(10)
)

print("\n========== MOST HALF-CENTURIES ==========\n")
print(half_centuries)

# Plot
plt.figure(figsize=(10, 6))

half_centuries.sort_values().plot(
    kind="barh"
)

plt.title("Top 10 IPL Players by Half-Centuries")

plt.xlabel("Half-Centuries")
plt.ylabel("Player")

plt.tight_layout()

plt.show()
# ============================================
# MOST SIXES
# ============================================

sixes = (
    deliveries[
        deliveries["batsman_runs"] == 6
    ]
    .groupby("batter")
    .size()
    .sort_values(ascending=False)
    .head(10)
)

print("\n========== MOST SIXES ==========\n")
print(sixes)

# Plot
plt.figure(figsize=(10, 6))

sixes.sort_values().plot(
    kind="barh"
)

plt.title("Top 10 IPL Players by Sixes")

plt.xlabel("Sixes")
plt.ylabel("Player")

plt.tight_layout()

plt.show()
# ============================================
# MOST FOURS
# ============================================

fours = (
    deliveries[
        deliveries["batsman_runs"] == 4
    ]
    .groupby("batter")
    .size()
    .sort_values(ascending=False)
    .head(10)
)

print("\n========== MOST FOURS ==========\n")
print(fours)

# Plot
plt.figure(figsize=(10, 6))

fours.sort_values().plot(
    kind="barh"
)

plt.title("Top 10 IPL Players by Fours")

plt.xlabel("Fours")
plt.ylabel("Player")

plt.tight_layout()

plt.show()
# ============================================
# BEST STRIKE RATES
# ============================================

player_batting = (
    deliveries
    .groupby("batter")
    .agg(
        Runs=("batsman_runs", "sum"),
        Balls=("batsman_runs", "count")
    )
)

# Minimum 500 balls faced
player_batting = player_batting[
    player_batting["Balls"] >= 500
]

# Strike Rate
player_batting["Strike_Rate"] = (
    player_batting["Runs"] /
    player_batting["Balls"]
) * 100

best_strike_rates = (
    player_batting
    .sort_values(
        "Strike_Rate",
        ascending=False
    )
    .head(10)
)

print("\n========== BEST STRIKE RATES ==========\n")
print(
    best_strike_rates[
        ["Runs", "Balls", "Strike_Rate"]
    ].round(2)
)

# Plot
plt.figure(figsize=(10, 6))

best_strike_rates["Strike_Rate"].sort_values().plot(
    kind="barh"
)

plt.title("Top 10 IPL Players by Strike Rate")
plt.xlabel("Strike Rate")
plt.ylabel("Player")

plt.tight_layout()
plt.show()
# ============================================
# BEST BATTING AVERAGES
# ============================================

# Total runs and balls
batting_stats = (
    deliveries
    .groupby("batter")
    .agg(
        Runs=("batsman_runs", "sum"),
        Balls=("batsman_runs", "count")
    )
)

# Count dismissals
dismissals = (
    deliveries[
        deliveries["player_dismissed"].notna()
    ]
    .groupby("player_dismissed")
    .size()
)

# Add dismissals to batting stats
batting_stats["Dismissals"] = (
    dismissals
    .reindex(batting_stats.index)
    .fillna(0)
)

# Minimum 500 balls faced
batting_stats = batting_stats[
    batting_stats["Balls"] >= 500
]

# Avoid division by zero
batting_stats = batting_stats[
    batting_stats["Dismissals"] > 0
]

# Batting Average
batting_stats["Batting_Average"] = (
    batting_stats["Runs"] /
    batting_stats["Dismissals"]
)

best_batting_average = (
    batting_stats
    .sort_values(
        "Batting_Average",
        ascending=False
    )
    .head(10)
)

print("\n========== BEST BATTING AVERAGES ==========\n")

print(
    best_batting_average[
        [
            "Runs",
            "Balls",
            "Dismissals",
            "Batting_Average"
        ]
    ].round(2)
)

# Plot
plt.figure(figsize=(10, 6))

best_batting_average[
    "Batting_Average"
].sort_values().plot(
    kind="barh"
)

plt.title("Top 10 IPL Players by Batting Average")

plt.xlabel("Batting Average")
plt.ylabel("Player")

plt.tight_layout()

plt.show()
# ============================================
# TOP 10 WICKET TAKERS
# ============================================

# Dismissals that are NOT credited to the bowler
non_bowler_dismissals = [
    "run out",
    "retired hurt",
    "retired out",
    "obstructing the field"
]

bowler_wickets = (
    deliveries[
        deliveries["player_dismissed"].notna() &
        ~deliveries["dismissal_kind"].isin(
            non_bowler_dismissals
        )
    ]
    .groupby("bowler")
    .size()
    .sort_values(ascending=False)
    .head(10)
)

print("\n========== TOP 10 WICKET TAKERS ==========\n")
print(bowler_wickets)

# Plot
plt.figure(figsize=(10, 6))

bowler_wickets.sort_values().plot(
    kind="barh"
)

plt.title("Top 10 IPL Wicket Takers")

plt.xlabel("Wickets")
plt.ylabel("Bowler")

plt.tight_layout()

plt.show()
# ============================================
# BEST BOWLING ECONOMY RATES
# ============================================

bowling_stats = (
    deliveries
    .groupby("bowler")
    .agg(
        Runs_Conceded=("total_runs", "sum"),
        Balls_Bowled=("total_runs", "count")
    )
)

# Minimum 500 balls bowled
bowling_stats = bowling_stats[
    bowling_stats["Balls_Bowled"] >= 500
]

# Economy Rate
bowling_stats["Overs"] = (
    bowling_stats["Balls_Bowled"] / 6
)

bowling_stats["Economy_Rate"] = (
    bowling_stats["Runs_Conceded"] /
    bowling_stats["Overs"]
)

best_economy = (
    bowling_stats
    .sort_values(
        "Economy_Rate",
        ascending=True
    )
    .head(10)
)

print("\n========== BEST BOWLING ECONOMY RATES ==========\n")

print(
    best_economy[
        [
            "Runs_Conceded",
            "Balls_Bowled",
            "Economy_Rate"
        ]
    ].round(2)
)

# Plot
plt.figure(figsize=(10, 6))

best_economy[
    "Economy_Rate"
].sort_values(
    ascending=False
).plot(
    kind="barh"
)

plt.title("Top 10 IPL Bowlers by Economy Rate")

plt.xlabel("Economy Rate")
plt.ylabel("Bowler")

plt.tight_layout()

plt.show()
# ============================================
# BEST BOWLING AVERAGES
# ============================================

# Wickets credited to bowlers
bowler_wickets_all = (
    deliveries[
        deliveries["player_dismissed"].notna() &
        ~deliveries["dismissal_kind"].isin(
            non_bowler_dismissals
        )
    ]
    .groupby("bowler")
    .size()
)

# Add wickets to bowling statistics
bowling_stats["Wickets"] = (
    bowler_wickets_all
    .reindex(bowling_stats.index)
    .fillna(0)
)

# Only bowlers with wickets
bowling_average = bowling_stats[
    bowling_stats["Wickets"] > 0
].copy()

# Bowling Average
bowling_average["Bowling_Average"] = (
    bowling_average["Runs_Conceded"] /
    bowling_average["Wickets"]
)

best_bowling_average = (
    bowling_average
    .sort_values(
        "Bowling_Average",
        ascending=True
    )
    .head(10)
)

print("\n========== BEST BOWLING AVERAGES ==========\n")

print(
    best_bowling_average[
        [
            "Runs_Conceded",
            "Wickets",
            "Bowling_Average"
        ]
    ].round(2)
)

# Plot
plt.figure(figsize=(10, 6))

best_bowling_average[
    "Bowling_Average"
].sort_values(
    ascending=False
).plot(
    kind="barh"
)

plt.title("Top 10 IPL Bowlers by Bowling Average")

plt.xlabel("Bowling Average")
plt.ylabel("Bowler")

plt.tight_layout()

plt.show()
# ============================================
# MOST DOT BALLS
# ============================================

dot_balls = (
    deliveries[
        deliveries["total_runs"] == 0
    ]
    .groupby("bowler")
    .size()
    .sort_values(ascending=False)
    .head(10)
)

print("\n========== MOST DOT BALLS ==========\n")
print(dot_balls)

# Plot
plt.figure(figsize=(10, 6))

dot_balls.sort_values().plot(
    kind="barh"
)

plt.title("Top 10 IPL Bowlers by Dot Balls")

plt.xlabel("Dot Balls")
plt.ylabel("Bowler")

plt.tight_layout()

plt.show()
# ============================================
# MOST EXPERIENCED PLAYERS
# ============================================

# Matches where player appeared as batter
batter_matches = (
    deliveries[
        ["match_id", "batter"]
    ]
    .drop_duplicates()
    .rename(
        columns={"batter": "player"}
    )
)

# Matches where player appeared as bowler
bowler_matches = (
    deliveries[
        ["match_id", "bowler"]
    ]
    .drop_duplicates()
    .rename(
        columns={"bowler": "player"}
    )
)

# Combine batter and bowler appearances
player_matches = pd.concat(
    [
        batter_matches,
        bowler_matches
    ]
)

# Remove duplicate player-match combinations
player_matches = (
    player_matches
    .drop_duplicates()
)

# Count matches played
matches_played = (
    player_matches
    .groupby("player")["match_id"]
    .nunique()
    .sort_values(
        ascending=False
    )
    .head(10)
)

print("\n========== MOST EXPERIENCED PLAYERS ==========\n")
print(matches_played)

# Plot
plt.figure(figsize=(10, 6))

matches_played.sort_values().plot(
    kind="barh"
)

plt.title("Top 10 IPL Players by Matches Played")

plt.xlabel("Matches Played")
plt.ylabel("Player")

plt.tight_layout()

plt.show()
# ============================================
# MOST EXPERIENCED PLAYERS
# ============================================

# Matches where player appeared as batter
batter_matches = (
    deliveries[
        ["match_id", "batter"]
    ]
    .drop_duplicates()
    .rename(
        columns={"batter": "player"}
    )
)

# Matches where player appeared as bowler
bowler_matches = (
    deliveries[
        ["match_id", "bowler"]
    ]
    .drop_duplicates()
    .rename(
        columns={"bowler": "player"}
    )
)

# Combine batter and bowler appearances
player_matches = pd.concat(
    [
        batter_matches,
        bowler_matches
    ]
)

# Remove duplicate player-match combinations
player_matches = (
    player_matches
    .drop_duplicates()
)

# Count matches played
matches_played = (
    player_matches
    .groupby("player")["match_id"]
    .nunique()
    .sort_values(
        ascending=False
    )
    .head(10)
)

print("\n========== MOST EXPERIENCED PLAYERS ==========\n")
print(matches_played)

# Plot
plt.figure(figsize=(10, 6))

matches_played.sort_values().plot(
    kind="barh"
)

plt.title("Top 10 IPL Players by Matches Played")

plt.xlabel("Matches Played")
plt.ylabel("Player")

plt.tight_layout()

plt.show()
# ============================================
# MOST PLAYER OF THE MATCH AWARDS
# ============================================

player_awards = (
    matches["player_of_match"]
    .dropna()
    .value_counts()
    .head(10)
)

print("\n========== MOST PLAYER OF THE MATCH AWARDS ==========\n")
print(player_awards)

# Plot
plt.figure(figsize=(10, 6))

player_awards.sort_values().plot(
    kind="barh"
)

plt.title("Top 10 IPL Players by Player of the Match Awards")
plt.xlabel("Awards")
plt.ylabel("Player")

plt.tight_layout()

plt.show()
# ============================================
# FINAL MODULE 9 SUMMARY
# ============================================

print("\n")
print("=" * 60)
print("             FINAL PLAYER PERFORMANCE ANALYSIS")
print("=" * 60)

print("\nTop Run Scorer:")
print(
    top_run_scorers.index[0],
    "-",
    top_run_scorers.iloc[0],
    "runs"
)

print("\nMost Centuries:")
print(
    centuries.index[0],
    "-",
    centuries.iloc[0],
    "centuries"
)

print("\nMost Sixes:")
print(
    sixes.index[0],
    "-",
    sixes.iloc[0],
    "sixes"
)

print("\nBest Strike Rate:")
print(
    best_strike_rates.index[0],
    "-",
    round(
        best_strike_rates.iloc[0]["Strike_Rate"],
        2
    )
)

print("\nBest Batting Average:")
print(
    best_batting_average.index[0],
    "-",
    round(
        best_batting_average.iloc[0]["Batting_Average"],
        2
    )
)

print("\nTop Wicket Taker:")
print(
    bowler_wickets.index[0],
    "-",
    bowler_wickets.iloc[0],
    "wickets"
)

print("\nBest Economy Rate:")
print(
    best_economy.index[0],
    "-",
    round(
        best_economy.iloc[0]["Economy_Rate"],
        2
    )
)

print("\nBest Bowling Average:")
print(
    best_bowling_average.index[0],
    "-",
    round(
        best_bowling_average.iloc[0]["Bowling_Average"],
        2
    )
)

print("\nMost Dot Balls:")
print(
    dot_balls.index[0],
    "-",
    dot_balls.iloc[0],
    "dot balls"
)

print("\nMost Experienced Player:")
print(
    matches_played.index[0],
    "-",
    matches_played.iloc[0],
    "matches"
)

print("\nMost Player of the Match Awards:")
print(
    player_awards.index[0],
    "-",
    player_awards.iloc[0],
    "awards"
)

print("\n")
print("=" * 60)
print("             MODULE 9 COMPLETE")
print("=" * 60)