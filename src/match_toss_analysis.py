import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

sns.set_style("whitegrid")

# ============================================
# MODULE 7 - MATCH & TOSS ANALYSIS
# ============================================

matches = pd.read_csv(
    "data/processed/matches_cleaned.csv"
)

print("========== MATCH & TOSS ANALYSIS ==========\n")

print("Dataset Loaded Successfully!")

print("Shape :", matches.shape)

print("\nColumns:")
print(matches.columns)
# ============================================
# TOSS WINNERS
# ============================================

toss_winners = (
    matches["toss_winner"]
    .value_counts()
)

print("\n========== TOSS WINNERS ==========\n")

print(toss_winners)
# ============================================
# TOSS DECISIONS
# ============================================

toss_decisions = (
    matches["toss_decision"]
    .value_counts()
)

print("\n========== TOSS DECISIONS ==========\n")

print(toss_decisions)
# ============================================
# TOSS DECISION PERCENTAGE
# ============================================

decision_percentage = (
    matches["toss_decision"]
    .value_counts(normalize=True)
    * 100
)

print("\n========== TOSS DECISION PERCENTAGE ==========\n")

print(decision_percentage.round(2))
# ============================================
# TOSS DECISION CHART
# ============================================

plt.figure(figsize=(8, 5))

toss_decisions.plot(
    kind="bar"
)

plt.title("IPL Toss Decisions")
plt.xlabel("Toss Decision")
plt.ylabel("Number of Matches")

plt.xticks(rotation=0)

plt.tight_layout()

plt.show()
# ============================================
# TOSS WINNER -> MATCH WINNER
# ============================================

# Remove matches without a winner
valid_matches = matches[
    matches["winner"].notna()
].copy()

# Check whether toss winner also won the match
valid_matches["toss_match_win"] = (
    valid_matches["toss_winner"] ==
    valid_matches["winner"]
)

toss_match_wins = (
    valid_matches["toss_match_win"]
    .value_counts()
)

print("\n========== TOSS WINNER -> MATCH WINNER ==========\n")

print("Toss Winner Won Match :",
      toss_match_wins.get(True, 0))

print("Toss Winner Lost Match :",
      toss_match_wins.get(False, 0))
# Toss conversion percentage

toss_conversion = (
    valid_matches["toss_match_win"].mean()
    * 100
)

print(
    "Toss Winner -> Match Win % :",
    round(toss_conversion, 2)
)
# ============================================
# TOSS IMPACT CHART
# ============================================

toss_result = pd.Series({
    "Toss Winner Won": toss_match_wins.get(True, 0),
    "Toss Winner Lost": toss_match_wins.get(False, 0)
})

plt.figure(figsize=(8, 5))

toss_result.plot(
    kind="bar"
)

plt.title("Toss Winner vs Match Winner")
plt.xlabel("Result")
plt.ylabel("Number of Matches")

plt.xticks(rotation=0)

plt.tight_layout()

plt.show()
# ============================================
# TEAM-WISE TOSS PERFORMANCE
# ============================================

team_toss = (
    valid_matches
    .groupby("toss_winner")
    .agg(
        Toss_Wins=("toss_winner", "count"),
        Match_Wins_After_Toss=("toss_match_win", "sum")
    )
)

team_toss["Conversion_Rate"] = (
    team_toss["Match_Wins_After_Toss"] /
    team_toss["Toss_Wins"]
    * 100
)

team_toss = team_toss.sort_values(
    "Conversion_Rate",
    ascending=False
)

print("\n========== TEAM-WISE TOSS PERFORMANCE ==========\n")

print(team_toss.round(2))
# ============================================
# BAT FIRST vs CHASING
# ============================================

# Determine whether the toss-winning team chose to bat or field
valid_matches["bat_first"] = (
    valid_matches["toss_decision"] == "bat"
)

# Determine whether the match winner batted first
valid_matches["winner_batted_first"] = (
    (
        (valid_matches["winner"] == valid_matches["team1"]) &
        (valid_matches["toss_decision"] == "bat") &
        (valid_matches["toss_winner"] == valid_matches["team1"])
    )
    |
    (
        (valid_matches["winner"] == valid_matches["team2"]) &
        (valid_matches["toss_decision"] == "bat") &
        (valid_matches["toss_winner"] == valid_matches["team2"])
    )
)

# More reliable approach:
# Determine actual batting-first team

valid_matches["batting_first_team"] = valid_matches.apply(
    lambda row:
        row["toss_winner"]
        if row["toss_decision"] == "bat"
        else (
            row["team2"]
            if row["toss_winner"] == row["team1"]
            else row["team1"]
        ),
    axis=1
)

# Determine whether winner batted first
valid_matches["winner_batted_first"] = (
    valid_matches["winner"] ==
    valid_matches["batting_first_team"]
)

bat_first_wins = (
    valid_matches["winner_batted_first"]
    .value_counts()
)

print("\n========== BAT FIRST vs CHASING ==========\n")

print(
    "Bat First Wins :",
    bat_first_wins.get(True, 0)
)

print(
    "Chasing Wins :",
    bat_first_wins.get(False, 0)
)
# ============================================
# BAT FIRST vs CHASING PERCENTAGE
# ============================================

total_decided_matches = (
    bat_first_wins.get(True, 0) +
    bat_first_wins.get(False, 0)
)

bat_first_percentage = (
    bat_first_wins.get(True, 0) /
    total_decided_matches
    * 100
)

chasing_percentage = (
    bat_first_wins.get(False, 0) /
    total_decided_matches
    * 100
)

print(
    "\nBat First Success :",
    round(bat_first_percentage, 2),
    "%"
)

print(
    "Chasing Success :",
    round(chasing_percentage, 2),
    "%"
)
# ============================================
# BAT FIRST vs CHASING CHART
# ============================================

bat_chase = pd.Series({
    "Bat First": bat_first_wins.get(True, 0),
    "Chasing": bat_first_wins.get(False, 0)
})

plt.figure(figsize=(8, 5))

bat_chase.plot(
    kind="bar"
)

plt.title("Bat First vs Chasing Success")
plt.xlabel("Match Strategy")
plt.ylabel("Matches Won")

plt.xticks(rotation=0)

plt.tight_layout()

plt.show()
# ============================================
# SEASON-WISE TOSS IMPACT
# ============================================

season_toss = (
    valid_matches
    .groupby("season")
    .agg(
        Matches=("id", "count"),
        Toss_Winner_Match_Wins=("toss_match_win", "sum")
    )
)

season_toss["Toss_Impact_Percentage"] = (
    season_toss["Toss_Winner_Match_Wins"] /
    season_toss["Matches"]
    * 100
)

print("\n========== SEASON-WISE TOSS IMPACT ==========\n")

print(
    season_toss.round(2)
)
# ============================================
# SEASON-WISE TOSS IMPACT CHART
# ============================================

plt.figure(figsize=(12, 6))

season_toss["Toss_Impact_Percentage"].plot(
    kind="line",
    marker="o",
    linewidth=3
)

plt.axhline(
    y=50,
    linestyle="--",
    label="50% Baseline"
)

plt.title("Season-wise Toss Impact")
plt.xlabel("Season")
plt.ylabel("Toss Winner → Match Winner (%)")

plt.xticks(rotation=45)

plt.legend()

plt.tight_layout()

plt.show()
# ============================================
# RELIABLE TEAM TOSS PERFORMANCE
# ============================================

reliable_team_toss = team_toss[
    team_toss["Toss_Wins"] >= 50
].copy()

reliable_team_toss = reliable_team_toss.sort_values(
    "Conversion_Rate",
    ascending=False
)

print(
    "\n========== TEAM TOSS PERFORMANCE "
    "(MINIMUM 50 TOSS WINS) ==========\n"
)

print(
    reliable_team_toss.round(2)
)
# ============================================
# RELIABLE TEAM TOSS PERFORMANCE
# ============================================

reliable_team_toss = team_toss[
    team_toss["Toss_Wins"] >= 50
].copy()

reliable_team_toss = reliable_team_toss.sort_values(
    "Conversion_Rate",
    ascending=False
)

print(
    "\n========== TEAM TOSS PERFORMANCE "
    "(MINIMUM 50 TOSS WINS) ==========\n"
)

print(
    reliable_team_toss.round(2)
)
# ============================================
# VENUE-WISE TOSS IMPACT
# ============================================

venue_toss = (
    valid_matches
    .groupby("venue")
    .agg(
        Matches=("id", "count"),
        Toss_Winner_Match_Wins=("toss_match_win", "sum")
    )
)

venue_toss["Toss_Impact_Percentage"] = (
    venue_toss["Toss_Winner_Match_Wins"] /
    venue_toss["Matches"]
    * 100
)

# Only consider venues with at least 10 matches
venue_toss_reliable = venue_toss[
    venue_toss["Matches"] >= 10
].copy()

venue_toss_reliable = venue_toss_reliable.sort_values(
    "Toss_Impact_Percentage",
    ascending=False
)

print("\n========== VENUE-WISE TOSS IMPACT ==========\n")

print(
    venue_toss_reliable.head(10).round(2)
)
# ============================================
# VENUE-WISE TOSS IMPACT CHART
# ============================================

top_venue_toss = (
    venue_toss_reliable
    .head(10)
    .sort_values("Toss_Impact_Percentage")
)

plt.figure(figsize=(12, 7))

top_venue_toss[
    "Toss_Impact_Percentage"
].plot(
    kind="barh"
)

plt.axvline(
    x=50,
    linestyle="--",
    label="50% Baseline"
)

plt.title("Top 10 Venues by Toss Impact")

plt.xlabel(
    "Toss Winner → Match Winner (%)"
)

plt.ylabel("Venue")

plt.legend()

plt.tight_layout()

plt.show()
# ============================================
# MOST TOSS-INFLUENTIAL VENUE
# ============================================

best_venue = venue_toss_reliable.iloc[0]

print(
    "\n========== MOST TOSS-INFLUENTIAL VENUE ==========\n"
)

print(
    "Venue :",
    venue_toss_reliable.index[0]
)

print(
    "Matches :",
    int(best_venue["Matches"])
)

print(
    "Toss Winner -> Match Win % :",
    round(
        best_venue["Toss_Impact_Percentage"],
        2
    )
)
# ============================================
# FINAL MODULE 7 SUMMARY
# ============================================

print("\n")
print("=" * 55)
print("          FINAL MATCH & TOSS ANALYSIS")
print("=" * 55)

print("\nOverall Toss Impact:")
print(
    "Toss Winner -> Match Win :",
    round(toss_conversion, 2),
    "%"
)

print("\nBat First vs Chasing:")
print(
    "Bat First Success :",
    round(bat_first_percentage, 2),
    "%"
)

print(
    "Chasing Success :",
    round(chasing_percentage, 2),
    "%"
)

print("\nBest Team at Converting Toss Wins:")

best_team = reliable_team_toss.iloc[0]

print(
    "Team :",
    reliable_team_toss.index[0]
)

print(
    "Conversion Rate :",
    round(best_team["Conversion_Rate"], 2),
    "%"
)

print("\nMost Toss-Influential Venue:")

print(
    "Venue :",
    venue_toss_reliable.index[0]
)

print(
    "Toss Impact :",
    round(
        venue_toss_reliable.iloc[0][
            "Toss_Impact_Percentage"
        ],
        2
    ),
    "%"
)

print("\nHighest Toss Impact Season:")

best_season = season_toss[
    "Toss_Impact_Percentage"
].idxmax()

print(
    "Season :",
    best_season
)

print(
    "Toss Impact :",
    round(
        season_toss.loc[
            best_season,
            "Toss_Impact_Percentage"
        ],
        2
    ),
    "%"
)

print("\n")
print("=" * 55)
print("          MODULE 7 COMPLETE")
print("=" * 55)