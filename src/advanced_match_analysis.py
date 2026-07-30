import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

sns.set_style("whitegrid")

# ============================================
# MODULE 8 - ADVANCED MATCH ANALYSIS
# ============================================

matches = pd.read_csv(
    "data/processed/matches_cleaned.csv"
)

deliveries = pd.read_csv(
    "data/processed/deliveries_cleaned.csv"
)

print("\n========== ADVANCED MATCH ANALYSIS ==========\n")

print("Datasets Loaded Successfully!")

print("Matches Shape :", matches.shape)
print("Deliveries Shape :", deliveries.shape)

print("\nMatches Columns:")
print(matches.columns)

print("\nDeliveries Columns:")
print(deliveries.columns)
# ============================================
# BIGGEST WINS BY RUNS
# ============================================

wins_by_runs = matches[
    matches["result"] == "runs"
].copy()

top_run_wins = (
    wins_by_runs[
        ["season", "team1", "team2", "winner", "result_margin"]
    ]
    .sort_values(
        "result_margin",
        ascending=False
    )
    .head(10)
)

print("\n========== TOP 10 BIGGEST WINS BY RUNS ==========\n")

print(top_run_wins)
# ============================================
# BIGGEST WINS BY WICKETS
# ============================================

wins_by_wickets = matches[
    matches["result"] == "wickets"
].copy()

top_wicket_wins = (
    wins_by_wickets[
        ["season", "team1", "team2", "winner", "result_margin"]
    ]
    .sort_values(
        "result_margin",
        ascending=False
    )
    .head(10)
)

print("\n========== TOP 10 BIGGEST WINS BY WICKETS ==========\n")

print(top_wicket_wins)
# ============================================
# TEAM INNINGS SCORES
# ============================================

innings_scores = (
    deliveries
    .groupby(
        ["match_id", "inning", "batting_team"]
    )["total_runs"]
    .sum()
    .reset_index()
)

top_team_scores = (
    innings_scores
    .sort_values(
        "total_runs",
        ascending=False
    )
    .head(10)
)

print("\n========== TOP 10 HIGHEST TEAM SCORES ==========\n")

print(top_team_scores)
# ============================================
# LOWEST TEAM SCORES
# ============================================

lowest_team_scores = (
    innings_scores
    .sort_values(
        "total_runs",
        ascending=True
    )
    .head(10)
)

print("\n========== TOP 10 LOWEST TEAM SCORES ==========\n")

print(lowest_team_scores)
# ============================================
# HIGHEST TEAM SCORES CHART
# ============================================

top_scores_chart = (
    top_team_scores
    .sort_values("total_runs")
)

plt.figure(figsize=(10, 6))

plt.barh(
    top_scores_chart["batting_team"],
    top_scores_chart["total_runs"]
)

plt.title("Top 10 Highest IPL Team Scores")

plt.xlabel("Runs")

plt.ylabel("Team")

plt.tight_layout()

plt.show()
# ============================================
# HIGHEST INDIVIDUAL SCORES
# ============================================

individual_scores = (
    deliveries
    .groupby(["match_id", "inning", "batter"])["batsman_runs"]
    .sum()
    .reset_index()
)

top_individual_scores = (
    individual_scores
    .sort_values("batsman_runs", ascending=False)
    .head(10)
)

print("\n========== TOP 10 INDIVIDUAL SCORES ==========\n")
print(top_individual_scores)
# ============================================
# BEST BOWLING FIGURES
# ============================================

# Exclude wickets that are not credited to the bowler
bowler_wickets = deliveries[
    (deliveries["is_wicket"] == 1) &
    (~deliveries["dismissal_kind"].isin([
        "run out",
        "retired hurt",
        "obstructing the field"
    ]))
]

bowling_figures = (
    bowler_wickets
    .groupby(
        ["match_id", "inning", "bowler"]
    )
    .size()
    .reset_index(name="wickets")
)

top_bowling_figures = (
    bowling_figures
    .sort_values(
        "wickets",
        ascending=False
    )
    .head(10)
)

print("\n========== TOP 10 BOWLING FIGURES ==========\n")
print(top_bowling_figures)
# ============================================
# BOWLING RUNS CONCEDED
# ============================================

bowling_runs = (
    deliveries
    .groupby(
        ["match_id", "inning", "bowler"]
    )["total_runs"]
    .sum()
    .reset_index(name="runs_conceded")
)

bowling_performance = top_bowling_figures.merge(
    bowling_runs,
    on=["match_id", "inning", "bowler"],
    how="left"
)

bowling_performance = bowling_performance.sort_values(
    ["wickets", "runs_conceded"],
    ascending=[False, True]
)

print("\n========== BEST BOWLING PERFORMANCES ==========\n")
print(bowling_performance)
# ============================================
# CLOSEST MATCHES - BY RUNS
# ============================================

closest_run_matches = (
    matches[
        matches["result"] == "runs"
    ]
    [
        [
            "season",
            "team1",
            "team2",
            "winner",
            "result_margin"
        ]
    ]
    .sort_values("result_margin")
    .head(10)
)

print(
    "\n========== TOP 10 CLOSEST WINS BY RUNS ==========\n"
)

print(closest_run_matches)
# ============================================
# CLOSEST MATCHES - BY WICKETS
# ============================================

closest_wicket_matches = (
    matches[
        matches["result"] == "wickets"
    ]
    [
        [
            "season",
            "team1",
            "team2",
            "winner",
            "result_margin"
        ]
    ]
    .sort_values("result_margin")
    .head(10)
)

print(
    "\n========== TOP 10 CLOSEST WINS BY WICKETS ==========\n"
)

print(closest_wicket_matches)
# ============================================
# SUPER OVER ANALYSIS
# ============================================

super_over_matches = matches[
    matches["super_over"] == "Y"
].copy()

print(
    "\n========== SUPER OVER ANALYSIS ==========\n"
)

print(
    "Total Super Over Matches :",
    len(super_over_matches)
)

print("\nSuper Over Matches:\n")

print(
    super_over_matches[
        [
            "season",
            "team1",
            "team2",
            "winner",
            "venue"
        ]
    ]
)
# ============================================
# SUPER OVER TEAM PARTICIPATION
# ============================================

super_over_teams = pd.concat([
    super_over_matches["team1"],
    super_over_matches["team2"]
])

super_over_team_count = (
    super_over_teams
    .value_counts()
    .head(10)
)

print(
    "\n========== TOP SUPER OVER PARTICIPATING TEAMS ==========\n"
)

print(super_over_team_count)
# ============================================
# SUPER OVER WINNERS
# ============================================

super_over_winners = (
    super_over_matches["winner"]
    .value_counts()
)

print(
    "\n========== SUPER OVER WINNERS ==========\n"
)

print(super_over_winners)
# ============================================
# SEASON-WISE AVERAGE MATCH SCORE
# ============================================

season_match_scores = (
    innings_scores
    .groupby("match_id")["total_runs"]
    .sum()
    .reset_index()
)

season_match_scores = season_match_scores.merge(
    matches[["id", "season"]],
    left_on="match_id",
    right_on="id",
    how="left"
)

avg_match_score = (
    season_match_scores
    .groupby("season")["total_runs"]
    .mean()
    .sort_values(ascending=False)
)

print(
    "\n========== SEASON-WISE AVERAGE MATCH SCORE ==========\n"
)

print(avg_match_score.round(2))
# ============================================
# SEASON-WISE HIGHEST TEAM SCORE
# ============================================

season_highest_score = innings_scores.merge(
    matches[["id", "season"]],
    left_on="match_id",
    right_on="id",
    how="left"
)

season_highest_score = (
    season_highest_score
    .groupby("season")["total_runs"]
    .max()
)

print(
    "\n========== SEASON-WISE HIGHEST TEAM SCORE ==========\n"
)

print(season_highest_score)
# ============================================
# SEASON-WISE AVERAGE WINNING MARGIN
# ============================================

run_margin_season = (
    matches[matches["result"] == "runs"]
    .groupby("season")["result_margin"]
    .mean()
)

wicket_margin_season = (
    matches[matches["result"] == "wickets"]
    .groupby("season")["result_margin"]
    .mean()
)

print(
    "\n========== SEASON-WISE AVERAGE WINNING MARGIN ==========\n"
)

print("\nWins by Runs:")

print(run_margin_season.round(2))

print("\nWins by Wickets:")

print(wicket_margin_season.round(2))
# ============================================
# AVERAGE MATCH SCORE CHART
# ============================================

plt.figure(figsize=(12, 6))

avg_match_score.sort_index().plot(
    kind="line",
    marker="o"
)

plt.title("Season-wise Average IPL Match Score")

plt.xlabel("Season")

plt.ylabel("Average Combined Score")

plt.xticks(rotation=45)

plt.tight_layout()

plt.show()
# ============================================
# SEASON-WISE HIGHEST SCORE CHART
# ============================================

plt.figure(figsize=(12, 6))

season_highest_score.sort_index().plot(
    kind="bar"
)

plt.title("Highest Team Score by IPL Season")

plt.xlabel("Season")

plt.ylabel("Highest Score")

plt.xticks(rotation=45)

plt.tight_layout()

plt.show()
# ============================================
# FINAL MODULE 8 SUMMARY
# ============================================

print("\n")
print("=" * 60)
print("             FINAL ADVANCED MATCH ANALYSIS")
print("=" * 60)

# Biggest win by runs
biggest_run_win = matches[
    matches["result"] == "runs"
]["result_margin"].max()

print("\nBiggest Win by Runs :")
print(biggest_run_win, "runs")

# Biggest win by wickets
biggest_wicket_win = matches[
    matches["result"] == "wickets"
]["result_margin"].max()

print("\nBiggest Win by Wickets :")
print(biggest_wicket_win, "wickets")

# Highest team score
highest_team_score = innings_scores[
    "total_runs"
].max()

print("\nHighest Team Score :")
print(highest_team_score)

# Highest individual score
highest_individual_score = individual_scores[
    "batsman_runs"
].max()

print("\nHighest Individual Score :")
print(highest_individual_score)

# Best bowling figures
best_wickets = bowling_performance[
    "wickets"
].max()

best_bowling = bowling_performance[
    bowling_performance["wickets"] == best_wickets
].sort_values(
    "runs_conceded"
).iloc[0]

print("\nBest Bowling Performance :")
print(
    best_bowling["wickets"],
    "wickets for",
    best_bowling["runs_conceded"],
    "runs"
)

# Closest run win
closest_run = matches[
    matches["result"] == "runs"
]["result_margin"].min()

print("\nClosest Win by Runs :")
print(closest_run, "run")

# Closest wicket win
closest_wicket = matches[
    matches["result"] == "wickets"
]["result_margin"].min()

print("\nClosest Win by Wickets :")
print(closest_wicket, "wicket(s)")

# Super Overs
print("\nSuper Over Matches :")
print(len(super_over_matches))

# Most Super Over wins
most_super_over_wins = super_over_winners.idxmax()

print("\nMost Super Over Wins :")
print(
    most_super_over_wins,
    "-",
    super_over_winners.max()
)

# Highest scoring season
highest_scoring_season = avg_match_score.idxmax()

print("\nHighest Average Scoring Season :")
print(
    highest_scoring_season,
    "-",
    round(
        avg_match_score.max(),
        2
    )
)

print("\n")
print("=" * 60)
print("             MODULE 8 COMPLETE")
print("=" * 60)