import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

sns.set_style("whitegrid")

# Load datasets
matches = pd.read_csv("data/processed/matches_cleaned.csv")
deliveries = pd.read_csv("data/processed/deliveries_cleaned.csv")

print("========== IPL VENUE ANALYSIS ==========\n")

print("Datasets Loaded Successfully!")
print("Matches Shape :", matches.shape)
print("Deliveries Shape :", deliveries.shape)

print("\nMatches Columns:\n")
print(matches.columns)

print("\nDeliveries Columns:\n")
print(deliveries.columns)
# ============================================
# TOP 10 VENUES BY MATCHES HOSTED
# ============================================

venue_matches = (
    matches["venue"]
    .value_counts()
    .head(10)
)

print("\n========== TOP 10 VENUES ==========\n")
print(venue_matches)

# Plot
plt.figure(figsize=(12,6))

venue_matches.plot(
    kind="bar",
    color="royalblue"
)

plt.title("Top 10 IPL Venues by Matches Hosted")
plt.xlabel("Venue")
plt.ylabel("Matches")

plt.xticks(rotation=75)

plt.tight_layout()

plt.show()
# ============================================
# HIGHEST SCORING VENUES
# ============================================

# Merge deliveries with venue information
venue_runs = deliveries.merge(
    matches[["id", "venue"]],
    left_on="match_id",
    right_on="id"
)

# Total runs scored at each venue
highest_runs = (
    venue_runs.groupby("venue")["total_runs"]
    .sum()
    .sort_values(ascending=False)
    .head(10)
)

print("\n========== HIGHEST SCORING VENUES ==========\n")
print(highest_runs)

# Plot
plt.figure(figsize=(12,6))

highest_runs.plot(
    kind="bar",
    color="crimson"
)

plt.title("Top 10 Highest Scoring IPL Venues")
plt.xlabel("Venue")
plt.ylabel("Total Runs")

plt.xticks(rotation=75)

plt.tight_layout()

plt.show()
# ============================================
# AVERAGE FIRST INNINGS SCORE
# ============================================

# First innings only
first_innings = deliveries[deliveries["inning"] == 1]

# Total score in each first innings
first_scores = (
    first_innings
    .groupby(["match_id"])["total_runs"]
    .sum()
    .reset_index()
)

# Merge with venue
first_scores = first_scores.merge(
    matches[["id", "venue"]],
    left_on="match_id",
    right_on="id"
)

# Average first innings score
avg_first = (
    first_scores
    .groupby("venue")["total_runs"]
    .mean()
    .sort_values(ascending=False)
    .head(10)
)

print("\n========== AVERAGE FIRST INNINGS SCORE ==========\n")
print(avg_first.round(2))

# Plot
plt.figure(figsize=(12,6))

avg_first.plot(
    kind="bar",
    color="darkgreen"
)

plt.title("Top 10 Venues by Average First Innings Score")
plt.xlabel("Venue")
plt.ylabel("Average Score")

plt.xticks(rotation=75)

plt.tight_layout()

plt.show()

# ============================================
# AVERAGE SECOND INNINGS SCORE
# ============================================

# Second innings only
second_innings = deliveries[deliveries["inning"] == 2]

# Total score in each second innings
second_scores = (
    second_innings
    .groupby("match_id")["total_runs"]
    .sum()
    .reset_index()
)

# Merge with venue
second_scores = second_scores.merge(
    matches[["id", "venue"]],
    left_on="match_id",
    right_on="id"
)

# Average second innings score
avg_second = (
    second_scores
    .groupby("venue")["total_runs"]
    .mean()
    .sort_values(ascending=False)
    .head(10)
)

print("\n========== AVERAGE SECOND INNINGS SCORE ==========\n")
print(avg_second.round(2))

# Plot
plt.figure(figsize=(12,6))

avg_second.plot(
    kind="bar",
    color="darkorange"
)

plt.title("Top 10 Venues by Average Second Innings Score")
plt.xlabel("Venue")
plt.ylabel("Average Score")

plt.xticks(rotation=75)

plt.tight_layout()

plt.show()
# ============================================
# AVERAGE RUNS PER MATCH
# ============================================

# Total runs scored in each match
match_runs = (
    deliveries.groupby("match_id")["total_runs"]
    .sum()
    .reset_index()
)

# Merge with venue
match_runs = match_runs.merge(
    matches[["id", "venue"]],
    left_on="match_id",
    right_on="id"
)

# Average runs per match at each venue
avg_match_runs = (
    match_runs.groupby("venue")["total_runs"]
    .mean()
    .sort_values(ascending=False)
    .head(10)
)

print("\n========== AVERAGE RUNS PER MATCH ==========\n")
print(avg_match_runs.round(2))

# Plot
plt.figure(figsize=(12,6))

avg_match_runs.plot(
    kind="bar",
    color="purple"
)

plt.title("Top 10 Venues by Average Runs per Match")
plt.xlabel("Venue")
plt.ylabel("Average Total Runs")

plt.xticks(rotation=75)

plt.tight_layout()

plt.show()

# ============================================
# HIGHEST SUCCESSFUL CHASE
# ============================================

# Matches where a target existed
successful_chases = matches[
    matches["target_runs"] > 0
].copy()

# Successful chase score
successful_chases["chase_score"] = successful_chases["target_runs"] - 1

highest_chase = (
    successful_chases.groupby("venue")["chase_score"]
    .max()
    .sort_values(ascending=False)
    .head(10)
)

print("\n========== HIGHEST SUCCESSFUL CHASE ==========\n")
print(highest_chase)

# Plot
plt.figure(figsize=(12,6))

highest_chase.plot(
    kind="bar",
    color="green"
)

plt.title("Highest Successful Chase by Venue")
plt.xlabel("Venue")
plt.ylabel("Runs Chased")

plt.xticks(rotation=75)

plt.tight_layout()

plt.show()

# ============================================
# LOWEST SUCCESSFUL DEFENSE
# ============================================

# Matches won by defending a target
defended = matches[
    (matches["target_runs"] > 0) &
    (matches["result"] == "runs")
].copy()

# First innings score
defended["defended_score"] = defended["target_runs"] - 1

lowest_defense = (
    defended.groupby("venue")["defended_score"]
    .min()
    .sort_values()
    .head(10)
)

print("\n========== LOWEST SUCCESSFUL DEFENSE ==========\n")
print(lowest_defense)

# Plot
plt.figure(figsize=(12,6))

lowest_defense.plot(
    kind="bar",
    color="firebrick"
)

plt.title("Lowest Successfully Defended Scores by Venue")
plt.xlabel("Venue")
plt.ylabel("Runs Defended")

plt.xticks(rotation=75)

plt.tight_layout()

plt.show()
# ============================================
# VENUE-WISE WIN PERCENTAGE
# ============================================

venue_results = matches.copy()

# Bat First wins
bat_first = (
    venue_results[venue_results["result"] == "runs"]
    .groupby("venue")
    .size()
)

# Chase wins
chasing = (
    venue_results[venue_results["result"] == "wickets"]
    .groupby("venue")
    .size()
)

# Total completed matches
total_matches = (
    venue_results[
        venue_results["result"].isin(["runs", "wickets"])
    ]
    .groupby("venue")
    .size()
)

venue_stats = pd.DataFrame({
    "Bat First Wins": bat_first,
    "Chasing Wins": chasing,
    "Matches": total_matches
}).fillna(0)

venue_stats["Bat First %"] = (
    venue_stats["Bat First Wins"] /
    venue_stats["Matches"] * 100
).round(2)

venue_stats["Chasing %"] = (
    venue_stats["Chasing Wins"] /
    venue_stats["Matches"] * 100
).round(2)

print("\n========== VENUE-WISE WIN PERCENTAGE ==========\n")
print(
    venue_stats.sort_values(
        "Matches",
        ascending=False
    ).head(10)
)

# Plot
plt.figure(figsize=(12,6))

venue_stats.sort_values(
    "Matches",
    ascending=False
).head(10)[["Bat First %", "Chasing %"]].plot(
    kind="bar"
)

plt.title("Bat First vs Chasing Win % (Top 10 Venues)")
plt.xlabel("Venue")
plt.ylabel("Win Percentage")

plt.xticks(rotation=75)

plt.tight_layout()

plt.show()

# ============================================
# TOSS IMPACT BY VENUE
# ============================================

# Toss winner also won the match
matches["toss_match_win"] = (
    matches["toss_winner"] == matches["winner"]
)

toss_impact = (
    matches.groupby("venue")["toss_match_win"]
    .mean()
    .mul(100)
    .round(2)
    .sort_values(ascending=False)
    .head(10)
)

print("\n========== TOSS IMPACT BY VENUE ==========\n")
print(toss_impact)

# Plot
plt.figure(figsize=(12,6))

toss_impact.plot(
    kind="bar",
    color="orange"
)

plt.title("Top 10 Venues by Toss Win Impact")
plt.xlabel("Venue")
plt.ylabel("Toss Win → Match Win (%)")

plt.xticks(rotation=75)

plt.tight_layout()

plt.show()
# ============================================
# BEST BATTING VENUES
# ============================================

batting_venues = deliveries.merge(
    matches[["id", "venue"]],
    left_on="match_id",
    right_on="id"
)

best_batting = (
    batting_venues.groupby("venue")["batsman_runs"]
    .sum()
    .sort_values(ascending=False)
    .head(10)
)

print("\n========== BEST BATTING VENUES ==========\n")
print(best_batting)

# Plot
plt.figure(figsize=(12,6))

best_batting.plot(
    kind="bar",
    color="royalblue"
)

plt.title("Top 10 Batting-Friendly Venues")
plt.xlabel("Venue")
plt.ylabel("Total Batsman Runs")

plt.xticks(rotation=75)

plt.tight_layout()

plt.show()

# ============================================
# BEST BOWLING VENUES
# ============================================

bowling_venues = deliveries.merge(
    matches[["id", "venue"]],
    left_on="match_id",
    right_on="id"
)

best_bowling = (
    bowling_venues.groupby("venue")["is_wicket"]
    .sum()
    .sort_values(ascending=False)
    .head(10)
)

print("\n========== BEST BOWLING VENUES ==========\n")
print(best_bowling)

# Plot
plt.figure(figsize=(12,6))

best_bowling.plot(
    kind="bar",
    color="darkred"
)

plt.title("Top 10 Bowling-Friendly Venues")
plt.xlabel("Venue")
plt.ylabel("Total Wickets")

plt.xticks(rotation=75)

plt.tight_layout()

plt.show()

# ============================================
# MOST SIXES BY VENUE
# ============================================

sixes_data = deliveries.merge(
    matches[["id", "venue"]],
    left_on="match_id",
    right_on="id"
)

venue_sixes = (
    sixes_data[sixes_data["batsman_runs"] == 6]
    .groupby("venue")
    .size()
    .sort_values(ascending=False)
    .head(10)
)

print("\n========== MOST SIXES BY VENUE ==========\n")
print(venue_sixes)

# Plot
plt.figure(figsize=(12,6))

venue_sixes.plot(
    kind="bar",
    color="purple"
)

plt.title("Top 10 Venues by Sixes")
plt.xlabel("Venue")
plt.ylabel("Number of Sixes")

plt.xticks(rotation=75)

plt.tight_layout()

plt.show()

# ============================================
# MOST WICKETS BY VENUE
# ============================================

venue_wickets = (
    bowling_venues.groupby("venue")["is_wicket"]
    .sum()
    .sort_values(ascending=False)
    .head(10)
)

print("\n========== MOST WICKETS BY VENUE ==========\n")
print(venue_wickets)

# Plot
plt.figure(figsize=(12,6))

venue_wickets.plot(
    kind="bar",
    color="teal"
)

plt.title("Top 10 Venues by Wickets")
plt.xlabel("Venue")
plt.ylabel("Total Wickets")

plt.xticks(rotation=75)

plt.tight_layout()

plt.show()

# ============================================
# VENUE DASHBOARD
# ============================================

print("\n========== VENUE DASHBOARD ==========\n")

venue = input("Enter Venue Name: ").strip()

venue_matches = matches[matches["venue"] == venue]

if venue_matches.empty:
    print("Venue not found!")

else:

    venue_deliveries = deliveries.merge(
        venue_matches[["id"]],
        left_on="match_id",
        right_on="id"
    )

    total_matches = len(venue_matches)

    total_runs = venue_deliveries["total_runs"].sum()

    total_wickets = venue_deliveries["is_wicket"].sum()

    total_sixes = (
        venue_deliveries["batsman_runs"] == 6
    ).sum()

    total_fours = (
        venue_deliveries["batsman_runs"] == 4
    ).sum()

    avg_first = (
        venue_deliveries[
            venue_deliveries["inning"] == 1
        ]
        .groupby("match_id")["total_runs"]
        .sum()
        .mean()
    )

    avg_second = (
        venue_deliveries[
            venue_deliveries["inning"] == 2
        ]
        .groupby("match_id")["total_runs"]
        .sum()
        .mean()
    )

    print("\n==========", venue.upper(), "==========\n")

    print("Matches Hosted :", total_matches)
    print("Total Runs :", total_runs)
    print("Total Wickets :", total_wickets)
    print("Total Fours :", total_fours)
    print("Total Sixes :", total_sixes)
    print("Average First Innings :", round(avg_first, 2))
    print("Average Second Innings :", round(avg_second, 2))