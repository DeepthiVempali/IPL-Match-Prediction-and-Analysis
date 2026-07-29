import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

sns.set_style("whitegrid")

# Load cleaned dataset
matches = pd.read_csv("data/processed/matches_cleaned.csv")

print("========== IPL TEAM ANALYSIS ==========\n")

print("Dataset Loaded Successfully!")
print("Shape:", matches.shape)

print("\nColumns:\n")
print(matches.columns)

# ============================================
# MOST SUCCESSFUL IPL TEAMS
# ============================================

team_wins = (
    matches["winner"]
    .value_counts()
    .head(10)
)

print("\n========== MOST SUCCESSFUL IPL TEAMS ==========\n")
print(team_wins)

# Plot
plt.figure(figsize=(10,6))

team_wins.plot(
    kind="bar",
    color="royalblue"
)

plt.title("Top 10 Most Successful IPL Teams")
plt.xlabel("Team")
plt.ylabel("Wins")

plt.xticks(rotation=45)

plt.tight_layout()

plt.show()

# ============================================
# TEAM PERFORMANCE BY SEASON
# ============================================

team = input("\nEnter Team Name: ").strip()

# Filter matches won by selected team
team_season = matches[
    matches["winner"] == team
]

if team_season.empty:
    print("\nTeam not found!")
    exit()

season_wins = (
    team_season.groupby("season")
    .size()
)

print(f"\n========== {team.upper()} - SEASON-WISE WINS ==========\n")
print(season_wins)

# Plot
plt.figure(figsize=(12,6))

season_wins.plot(
    kind="line",
    marker="o",
    linewidth=3
)

plt.title(f"{team} - Season-wise Wins")
plt.xlabel("Season")
plt.ylabel("Wins")

plt.xticks(rotation=45)

plt.grid(True)

plt.tight_layout()

plt.show()
# ============================================
# TEAM WIN PERCENTAGE
# ============================================

# Count matches played by each team
matches_played = pd.concat([
    matches["team1"],
    matches["team2"]
]).value_counts()

# Count matches won
matches_won = matches["winner"].value_counts()

# Create DataFrame
team_stats = pd.DataFrame({
    "Matches Played": matches_played,
    "Matches Won": matches_won
}).fillna(0)

# Calculate win percentage
team_stats["Win Percentage"] = (
    team_stats["Matches Won"] /
    team_stats["Matches Played"] * 100
)

team_stats = team_stats[
    team_stats["Matches Played"] >= 50
]

team_stats = team_stats.sort_values(
    by="Win Percentage",
    ascending=False
)

print("\n========== TEAM WIN PERCENTAGE ==========\n")
print(team_stats.round(2))

# Plot Top 10
plt.figure(figsize=(12,6))

team_stats["Win Percentage"].head(10).plot(
    kind="bar",
    color="purple"
)

plt.title("Top 10 Teams by Win Percentage")
plt.xlabel("Team")
plt.ylabel("Win Percentage (%)")

plt.xticks(rotation=45)

plt.tight_layout()

plt.show()

# ============================================
# HEAD TO HEAD ANALYSIS
# ============================================

print("\n========== HEAD TO HEAD ANALYSIS ==========\n")

team1 = input("Enter Team 1: ").strip()
team2 = input("Enter Team 2: ").strip()

# Matches between the two teams
h2h = matches[
    (
        (matches["team1"] == team1) &
        (matches["team2"] == team2)
    ) |
    (
        (matches["team1"] == team2) &
        (matches["team2"] == team1)
    )
]

if h2h.empty:
    print("\nNo matches found!")
else:

    team1_wins = (h2h["winner"] == team1).sum()
    team2_wins = (h2h["winner"] == team2).sum()
    no_result = h2h["winner"].isna().sum()

    total_matches = len(h2h)

    print("\n========== HEAD TO HEAD RECORD ==========\n")
    print("Matches Played :", total_matches)
    print(team1, "Wins :", team1_wins)
    print(team2, "Wins :", team2_wins)
    print("No Result :", no_result)

    # Win percentages
    if total_matches > 0:
        print(
            team1,
            "Win % :",
            round(team1_wins / total_matches * 100, 2)
        )

        print(
            team2,
            "Win % :",
            round(team2_wins / total_matches * 100, 2)
        )

    # Plot
    plt.figure(figsize=(6,5))

    plt.bar(
        [team1, team2],
        [team1_wins, team2_wins]
    )

    plt.title(f"{team1} vs {team2}")
    plt.ylabel("Wins")

    plt.tight_layout()

    plt.show()

    # ============================================
# TOSS WINNER ANALYSIS
# ============================================

toss_wins = (
    matches["toss_winner"]
    .value_counts()
)

print("\n========== TOSS WINNERS ==========\n")
print(toss_wins)

# Plot
plt.figure(figsize=(12,6))

toss_wins.plot(
    kind="bar",
    color="orange"
)

plt.title("Most Toss Wins by Team")
plt.xlabel("Team")
plt.ylabel("Toss Wins")

plt.xticks(rotation=45)

plt.tight_layout()

plt.show()

# ============================================
# TOSS DECISION ANALYSIS
# ============================================

toss_decision = (
    matches["toss_decision"]
    .value_counts()
)

print("\n========== TOSS DECISION ANALYSIS ==========\n")
print(toss_decision)

# Plot
plt.figure(figsize=(6,6))

toss_decision.plot(
    kind="pie",
    autopct="%1.1f%%",
    startangle=90
)

plt.ylabel("")
plt.title("Toss Decisions in IPL")

plt.tight_layout()

plt.show()

# ============================================
# CHASING vs DEFENDING ANALYSIS
# ============================================

# Teams batting first won
defending_wins = matches[
    matches["toss_decision"] == "bat"
].shape[0]

# Teams chasing won
chasing_wins = matches[
    matches["toss_decision"] == "field"
].shape[0]

print("\n========== CHASING vs DEFENDING ==========\n")
print("Matches Won while Defending :", defending_wins)
print("Matches Won while Chasing :", chasing_wins)

# Percentages
total = defending_wins + chasing_wins

print("\nDefending Success :",
      round(defending_wins / total * 100, 2), "%")

print("Chasing Success :",
      round(chasing_wins / total * 100, 2), "%")

# Plot
plt.figure(figsize=(6,6))

plt.bar(
    ["Defending", "Chasing"],
    [defending_wins, chasing_wins],
    color=["royalblue", "green"]
)

plt.title("Chasing vs Defending Wins")
plt.ylabel("Matches")

plt.tight_layout()

plt.show()

# ============================================
# BEST VENUES FOR A TEAM
# ============================================

team = input("\nEnter Team Name for Venue Analysis: ").strip()

team_matches = matches[matches["winner"] == team]

if team_matches.empty:
    print("\nTeam not found!")
else:

    venue_wins = (
        team_matches.groupby("venue")
        .size()
        .sort_values(ascending=False)
        .head(10)
    )

    print(f"\n========== {team.upper()} - BEST VENUES ==========\n")
    print(venue_wins)

    # Plot
    plt.figure(figsize=(12,6))

    venue_wins.plot(
        kind="bar",
        color="steelblue"
    )

    plt.title(f"{team} - Wins by Venue")
    plt.xlabel("Venue")
    plt.ylabel("Wins")

    plt.xticks(rotation=75)

    plt.tight_layout()

    plt.show()
    # ============================================
# HOME vs AWAY WINS
# ============================================

team = input("\nEnter Team Name for Home/Away Analysis: ").strip()

home_wins = matches[
    (matches["team1"] == team) &
    (matches["winner"] == team)
].shape[0]

away_wins = matches[
    (matches["team2"] == team) &
    (matches["winner"] == team)
].shape[0]

print("\n========== HOME vs AWAY WINS ==========\n")
print("Home Wins :", home_wins)
print("Away Wins :", away_wins)

# Plot
plt.figure(figsize=(6,6))

plt.bar(
    ["Home", "Away"],
    [home_wins, away_wins],
    color=["royalblue", "darkorange"]
)

plt.title(f"{team} - Home vs Away Wins")
plt.ylabel("Wins")

plt.tight_layout()

plt.show()
# ============================================
# LONGEST WINNING STREAK
# ============================================

print("\n========== LONGEST WINNING STREAK ==========\n")

team = input("Enter Team Name: ").strip()

# Sort matches by date
team_matches = matches.sort_values("date")

# Keep only matches played by the team
team_matches = team_matches[
    (team_matches["team1"] == team) |
    (team_matches["team2"] == team)
]

if team_matches.empty:
    print("Team not found!")
else:

    longest = 0
    current = 0

    for winner in team_matches["winner"]:

        if winner == team:
            current += 1

            if current > longest:
                longest = current

        else:
            current = 0

    print(f"\n{team}'s Longest Winning Streak :", longest)