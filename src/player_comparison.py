import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

sns.set_style("whitegrid")

# ============================================
# IPL PLAYER COMPARISON
# ============================================

# Load datasets
deliveries = pd.read_csv(
    "data/processed/deliveries_cleaned.csv"
)

matches = pd.read_csv(
    "data/processed/matches_cleaned.csv"
)

print("========== IPL PLAYER COMPARISON ==========\n")

print("Datasets Loaded Successfully!")

print("Deliveries Shape :", deliveries.shape)
print("Matches Shape :", matches.shape)
# ============================================
# SELECT PLAYERS
# ============================================

player1 = input("\nEnter First Player Name: ").strip()
player2 = input("Enter Second Player Name: ").strip()

players = deliveries["batter"].unique()

if player1 not in players:
    print(f"\nPlayer not found: {player1}")
    exit()

if player2 not in players:
    print(f"\nPlayer not found: {player2}")
    exit()

print("\nPlayers Found:")
print("Player 1 :", player1)
print("Player 2 :", player2)
# ============================================
# BASIC BATTING STATISTICS
# ============================================

def batting_stats(player):

    data = deliveries[
        deliveries["batter"] == player
    ]

    runs = data["batsman_runs"].sum()

    balls = len(data)

    fours = (
        data["batsman_runs"] == 4
    ).sum()

    sixes = (
        data["batsman_runs"] == 6
    ).sum()

    dismissals = (
        data["player_dismissed"] == player
    ).sum()

    if balls > 0:
        strike_rate = (runs / balls) * 100
    else:
        strike_rate = 0

    if dismissals > 0:
        average = runs / dismissals
    else:
        average = runs

    # Runs per match
    match_runs = (
        data.groupby("match_id")["batsman_runs"]
        .sum()
    )

    centuries = (
        match_runs >= 100
    ).sum()

    fifties = (
        (match_runs >= 50) &
        (match_runs < 100)
    ).sum()

    return {
        "Runs": runs,
        "Balls": balls,
        "Fours": fours,
        "Sixes": sixes,
        "Strike Rate": round(strike_rate, 2),
        "Batting Average": round(average, 2),
        "Centuries": centuries,
        "Half-Centuries": fifties
    }
stats1 = batting_stats(player1)
stats2 = batting_stats(player2)

comparison = pd.DataFrame(
    [stats1, stats2],
    index=[player1, player2]
)

print("\n========== BATTING COMPARISON ==========\n")

print(comparison)

# ============================================
# BATTING STATISTICS COMPARISON CHART
# ============================================

chart_stats = [
    "Runs",
    "Fours",
    "Sixes",
    "Centuries",
    "Half-Centuries"
]

comparison[chart_stats].plot(
    kind="bar",
    figsize=(12, 6)
)

plt.title(f"{player1} vs {player2} - Batting Comparison")
plt.xlabel("Player")
plt.ylabel("Value")

plt.xticks(rotation=0)

plt.legend(title="Statistics")

plt.tight_layout()

plt.show()

# ============================================
# RATE COMPARISON
# ============================================

rate_stats = [
    "Strike Rate",
    "Batting Average"
]

comparison[rate_stats].plot(
    kind="bar",
    figsize=(8, 5)
)

plt.title(f"{player1} vs {player2} - Batting Rates")
plt.xlabel("Player")
plt.ylabel("Rate")

plt.xticks(rotation=0)

plt.tight_layout()

plt.show()
# ============================================
# DETAILED PLAYER COMPARISON
# ============================================

print("\n========== DETAILED COMPARISON ==========\n")

for stat in comparison.columns:
    print(f"{stat}:")
    print(f"  {player1}: {comparison.loc[player1, stat]}")
    print(f"  {player2}: {comparison.loc[player2, stat]}")
    print()
    # ============================================
# SEASON-WISE PLAYER COMPARISON
# ============================================

season_data = deliveries.merge(
    matches[["id", "season"]],
    left_on="match_id",
    right_on="id"
)

player1_season = (
    season_data[season_data["batter"] == player1]
    .groupby("season")["batsman_runs"]
    .sum()
)

player2_season = (
    season_data[season_data["batter"] == player2]
    .groupby("season")["batsman_runs"]
    .sum()
)

season_comparison = pd.DataFrame({
    player1: player1_season,
    player2: player2_season
}).fillna(0)

print("\n========== SEASON-WISE COMPARISON ==========\n")
print(season_comparison)
# ============================================
# SEASON-WISE RUNS CHART
# ============================================

season_comparison.plot(
    kind="line",
    marker="o",
    figsize=(12, 6),
    linewidth=2
)

plt.title(
    f"{player1} vs {player2} - Season-wise Runs"
)

plt.xlabel("Season")
plt.ylabel("Runs")

plt.xticks(rotation=45)

plt.legend(title="Player")

plt.grid(True)

plt.tight_layout()

plt.show()

# ============================================
# RUNS AGAINST TEAMS
# ============================================

team_data = deliveries[
    deliveries["batter"].isin([player1, player2])
].copy()

runs_against = (
    team_data
    .groupby(["batter", "bowling_team"])["batsman_runs"]
    .sum()
    .reset_index()
)

runs_against_comparison = runs_against.pivot(
    index="bowling_team",
    columns="batter",
    values="batsman_runs"
).fillna(0)

print("\n========== RUNS AGAINST TEAMS ==========\n")
print(runs_against_comparison)

# ============================================
# RUNS AGAINST TEAMS CHART
# ============================================

runs_against_comparison.plot(
    kind="bar",
    figsize=(14, 7)
)

plt.title(
    f"{player1} vs {player2} - Runs Against Teams"
)

plt.xlabel("Opposition Team")
plt.ylabel("Runs")

plt.xticks(rotation=60)

plt.legend(title="Player")

plt.tight_layout()

plt.show()

# ============================================
# HEAD-TO-HEAD COMPARISON
# ============================================

merged = deliveries.merge(
    matches[["id", "season"]],
    left_on="match_id",
    right_on="id"
)

player1_matches = set(
    merged[merged["batter"] == player1]["match_id"]
)

player2_matches = set(
    merged[merged["batter"] == player2]["match_id"]
)

common_matches = player1_matches.intersection(player2_matches)

p1_common = merged[
    (merged["batter"] == player1) &
    (merged["match_id"].isin(common_matches))
]

p2_common = merged[
    (merged["batter"] == player2) &
    (merged["match_id"].isin(common_matches))
]

print("\n========== HEAD-TO-HEAD ==========\n")

print("Common Matches :", len(common_matches))
print()

print(player1)
print("Runs :", p1_common["batsman_runs"].sum())

print()

print(player2)
print("Runs :", p2_common["batsman_runs"].sum())

# ============================================
# OVERALL COMPARISON WINNER
# ============================================

print("\n========== CATEGORY WINNERS ==========\n")

for stat in comparison.columns:

    p1 = comparison.loc[player1, stat]
    p2 = comparison.loc[player2, stat]

    if p1 > p2:
        winner = player1
    elif p2 > p1:
        winner = player2
    else:
        winner = "Tie"

    print(f"{stat:<20} : {winner}")

# ============================================
# BOWLING COMPARISON
# ============================================

print("\n========== BOWLING COMPARISON ==========\n")

bowler1 = input("Enter First Bowler Name: ").strip()
bowler2 = input("Enter Second Bowler Name: ").strip()

bowlers = deliveries["bowler"].unique()

if bowler1 not in bowlers:
    print(f"\nBowler not found: {bowler1}")
    exit()

if bowler2 not in bowlers:
    print(f"\nBowler not found: {bowler2}")
    exit()

print("\nBowlers Found:")
print("Bowler 1 :", bowler1)
print("Bowler 2 :", bowler2) 
# ============================================
# BOWLING STATISTICS FUNCTION
# ============================================

def bowling_stats(bowler):

    data = deliveries[
        deliveries["bowler"] == bowler
    ].copy()

    # Balls bowled
    balls = len(data)

    # Runs conceded
    runs_conceded = data["total_runs"].sum()

    # Remove byes and leg-byes from bowler's conceded runs
    if "extras_type" in data.columns:
        bowler_runs = data[
            ~data["extras_type"].isin(
                ["byes", "legbyes"]
            )
        ]["total_runs"].sum()
    else:
        bowler_runs = runs_conceded

    # Wickets credited to bowler
    excluded_dismissals = [
        "run out",
        "retired hurt",
        "obstructing the field"
    ]

    wickets = data[
        (data["is_wicket"] == 1) &
        (~data["dismissal_kind"].isin(excluded_dismissals))
    ].shape[0]

    # Dot balls
    dot_balls = (
        data["total_runs"] == 0
    ).sum()

    # Economy
    overs = balls / 6

    if overs > 0:
        economy = bowler_runs / overs
    else:
        economy = 0

    # Bowling strike rate
    if wickets > 0:
        strike_rate = balls / wickets
    else:
        strike_rate = 0

    # Bowling average
    if wickets > 0:
        average = bowler_runs / wickets
    else:
        average = 0

    return {
        "Balls Bowled": balls,
        "Runs Conceded": bowler_runs,
        "Wickets": wickets,
        "Dot Balls": dot_balls,
        "Economy": round(economy, 2),
        "Strike Rate": round(strike_rate, 2),
        "Bowling Average": round(average, 2)
    }
# ============================================
# BOWLING COMPARISON TABLE
# ============================================

bowler_stats1 = bowling_stats(bowler1)
bowler_stats2 = bowling_stats(bowler2)

bowling_comparison = pd.DataFrame(
    [bowler_stats1, bowler_stats2],
    index=[bowler1, bowler2]
)

print("\n========== BOWLING COMPARISON ==========\n")

print(bowling_comparison)
# ============================================
# BOWLING CATEGORY WINNERS
# ============================================

print("\n========== BOWLING CATEGORY WINNERS ==========\n")

# Higher is better
higher_is_better = [
    "Wickets",
    "Dot Balls"
]

# Lower is better
lower_is_better = [
    "Economy",
    "Strike Rate",
    "Bowling Average"
]

# Balls bowled and runs conceded are not used
# to determine the overall bowling winner.

for stat in higher_is_better:

    p1 = bowling_comparison.loc[bowler1, stat]
    p2 = bowling_comparison.loc[bowler2, stat]

    if p1 > p2:
        winner = bowler1
    elif p2 > p1:
        winner = bowler2
    else:
        winner = "Tie"

    print(f"{stat:<20} : {winner}")


for stat in lower_is_better:

    p1 = bowling_comparison.loc[bowler1, stat]
    p2 = bowling_comparison.loc[bowler2, stat]

    if p1 < p2:
        winner = bowler1
    elif p2 < p1:
        winner = bowler2
    else:
        winner = "Tie"

    print(f"{stat:<20} : {winner}")
    # ============================================
# BOWLING PERFORMANCE CHART
# ============================================

bowling_chart_stats = [
    "Wickets",
    "Dot Balls"
]

bowling_comparison[bowling_chart_stats].plot(
    kind="bar",
    figsize=(10, 6)
)

plt.title(
    f"{bowler1} vs {bowler2} - Bowling Performance"
)

plt.xlabel("Bowler")
plt.ylabel("Count")

plt.xticks(rotation=0)

plt.legend(title="Statistics")

plt.tight_layout()

plt.show()
# ============================================
# BOWLING RATE COMPARISON
# ============================================

bowling_rate_stats = [
    "Economy",
    "Strike Rate",
    "Bowling Average"
]

bowling_comparison[bowling_rate_stats].plot(
    kind="bar",
    figsize=(10, 6)
)

plt.title(
    f"{bowler1} vs {bowler2} - Bowling Rates"
)

plt.xlabel("Bowler")
plt.ylabel("Rate")

plt.xticks(rotation=0)

plt.legend(title="Statistics")

plt.tight_layout()

plt.show()
# ============================================
# SEASON-WISE WICKET COMPARISON
# ============================================

bowling_season_data = deliveries.merge(
    matches[["id", "season"]],
    left_on="match_id",
    right_on="id"
)

def season_wickets(bowler):

    data = bowling_season_data[
        bowling_season_data["bowler"] == bowler
    ].copy()

    excluded_dismissals = [
        "run out",
        "retired hurt",
        "obstructing the field"
    ]

    wickets = data[
        (data["is_wicket"] == 1) &
        (~data["dismissal_kind"].isin(excluded_dismissals))
    ]

    return (
        wickets
        .groupby("season")
        .size()
    )


bowler1_season = season_wickets(bowler1)
bowler2_season = season_wickets(bowler2)

season_wicket_comparison = pd.DataFrame({
    bowler1: bowler1_season,
    bowler2: bowler2_season
}).fillna(0)

print("\n========== SEASON-WISE WICKET COMPARISON ==========\n")

print(season_wicket_comparison)
# ============================================
# SEASON-WISE WICKET CHART
# ============================================

season_wicket_comparison.plot(
    kind="line",
    marker="o",
    figsize=(12, 6),
    linewidth=2
)

plt.title(
    f"{bowler1} vs {bowler2} - Season-wise Wickets"
)

plt.xlabel("Season")
plt.ylabel("Wickets")

plt.xticks(rotation=45)

plt.legend(title="Bowler")

plt.grid(True)

plt.tight_layout()

plt.show()
# ============================================
# WICKETS AGAINST TEAMS
# ============================================

bowler_team_data = deliveries[
    deliveries["bowler"].isin([bowler1, bowler2])
].copy()

excluded_dismissals = [
    "run out",
    "retired hurt",
    "obstructing the field"
]

valid_wickets = bowler_team_data[
    (bowler_team_data["is_wicket"] == 1) &
    (~bowler_team_data["dismissal_kind"].isin(excluded_dismissals))
]

wickets_against = (
    valid_wickets
    .groupby(["bowler", "batting_team"])
    .size()
    .reset_index(name="Wickets")
)

wickets_against_comparison = wickets_against.pivot(
    index="batting_team",
    columns="bowler",
    values="Wickets"
).fillna(0)

print("\n========== WICKETS AGAINST TEAMS ==========\n")

print(wickets_against_comparison)
# ============================================
# WICKETS AGAINST TEAMS CHART
# ============================================

wickets_against_comparison.plot(
    kind="bar",
    figsize=(14, 7)
)

plt.title(
    f"{bowler1} vs {bowler2} - Wickets Against Teams"
)

plt.xlabel("Opposition Team")
plt.ylabel("Wickets")

plt.xticks(rotation=60)

plt.legend(title="Bowler")

plt.tight_layout()

plt.show()
# ============================================
# DOT BALLS AGAINST TEAMS
# ============================================

dot_ball_data = deliveries[
    deliveries["bowler"].isin([bowler1, bowler2])
].copy()

dot_balls_against = (
    dot_ball_data[
        dot_ball_data["total_runs"] == 0
    ]
    .groupby(["bowler", "batting_team"])
    .size()
    .reset_index(name="Dot Balls")
)

dot_balls_comparison = dot_balls_against.pivot(
    index="batting_team",
    columns="bowler",
    values="Dot Balls"
).fillna(0)

print("\n========== DOT BALLS AGAINST TEAMS ==========\n")

print(dot_balls_comparison)
# ============================================
# DOT BALLS AGAINST TEAMS CHART
# ============================================

dot_balls_comparison.plot(
    kind="bar",
    figsize=(14, 7)
)

plt.title(
    f"{bowler1} vs {bowler2} - Dot Balls Against Teams"
)

plt.xlabel("Opposition Team")
plt.ylabel("Dot Balls")

plt.xticks(rotation=60)

plt.legend(title="Bowler")

plt.tight_layout()

plt.show()
# ============================================
# FINAL PLAYER COMPARISON SUMMARY
# ============================================

print("\n" + "=" * 50)
print("          FINAL PLAYER COMPARISON")
print("=" * 50)

print("\nBATSMAN:")
print("Player 1 :", player1)
print("Player 2 :", player2)

# Count batting category wins
batting_wins_1 = 0
batting_wins_2 = 0

for stat in comparison.columns:

    p1 = comparison.loc[player1, stat]
    p2 = comparison.loc[player2, stat]

    if p1 > p2:
        batting_wins_1 += 1
    elif p2 > p1:
        batting_wins_2 += 1

print("\nBatting Category Wins:")
print(player1, ":", batting_wins_1)
print(player2, ":", batting_wins_2)

if batting_wins_1 > batting_wins_2:
    batting_winner = player1
elif batting_wins_2 > batting_wins_1:
    batting_winner = player2
else:
    batting_winner = "Tie"

print("Batting Winner :", batting_winner)


print("\nBOWLER:")
print("Bowler 1 :", bowler1)
print("Bowler 2 :", bowler2)

# Count bowling category wins
bowling_wins_1 = 0
bowling_wins_2 = 0

# Higher is better
for stat in ["Wickets", "Dot Balls"]:

    p1 = bowling_comparison.loc[bowler1, stat]
    p2 = bowling_comparison.loc[bowler2, stat]

    if p1 > p2:
        bowling_wins_1 += 1
    elif p2 > p1:
        bowling_wins_2 += 1


# Lower is better
for stat in [
    "Economy",
    "Strike Rate",
    "Bowling Average"
]:

    p1 = bowling_comparison.loc[bowler1, stat]
    p2 = bowling_comparison.loc[bowler2, stat]

    if p1 < p2:
        bowling_wins_1 += 1
    elif p2 < p1:
        bowling_wins_2 += 1

print("\nBowling Category Wins:")
print(bowler1, ":", bowling_wins_1)
print(bowler2, ":", bowling_wins_2)

if bowling_wins_1 > bowling_wins_2:
    bowling_winner = bowler1
elif bowling_wins_2 > bowling_wins_1:
    bowling_winner = bowler2
else:
    bowling_winner = "Tie"

print("Bowling Winner :", bowling_winner)

print("\n" + "=" * 50)
print("             COMPARISON COMPLETE")
print("=" * 50)