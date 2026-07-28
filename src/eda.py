import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Improve graph appearance
sns.set_style("whitegrid")

# Load cleaned datasets
matches = pd.read_csv("data/processed/matches_cleaned.csv")
deliveries = pd.read_csv("data/processed/deliveries_cleaned.csv")

print("Datasets loaded successfully!")

# Matches played each season
matches_per_season = matches["season"].value_counts().sort_index()

print("\nMatches Played Each Season:")
print(matches_per_season)

# Plot graph
plt.figure(figsize=(10, 5))

matches_per_season.plot(kind="bar", color="skyblue")

plt.title("Matches Played Each Season")
plt.xlabel("Season")
plt.ylabel("Number of Matches")

plt.xticks(rotation=45)

plt.tight_layout()

plt.savefig("reports/matches_per_season.png")

plt.show()

# Top 10 Most Successful IPL Teams
team_wins = matches["winner"].value_counts().head(10)

print("\nTop 10 Most Successful IPL Teams:")
print(team_wins)

plt.figure(figsize=(12, 6))

sns.barplot(
    x=team_wins.index,
    y=team_wins.values
)

plt.title("Top 10 Most Successful IPL Teams")
plt.xlabel("Team")
plt.ylabel("Number of Wins")

plt.xticks(rotation=45)

plt.tight_layout()

plt.savefig("reports/top_10_teams.png")

plt.show()

# Teams Winning Toss Most Often
toss_wins = matches["toss_winner"].value_counts().head(10)

print("\nTop 10 Teams Winning the Toss:")
print(toss_wins)

plt.figure(figsize=(12, 6))

sns.barplot(
    x=toss_wins.index,
    y=toss_wins.values
)

plt.title("Top 10 Teams Winning the Toss")
plt.xlabel("Team")
plt.ylabel("Number of Toss Wins")

plt.xticks(rotation=45)

plt.tight_layout()

plt.savefig("reports/top_10_toss_winners.png")

plt.show()

# Toss Decision Analysis
toss_decision = matches["toss_decision"].value_counts()

print("\nToss Decision:")
print(toss_decision)

plt.figure(figsize=(6, 6))

plt.pie(
    toss_decision.values,
    labels=toss_decision.index,
    autopct="%1.1f%%",
    startangle=90
)

plt.title("Toss Decision Distribution")

plt.savefig("reports/toss_decision.png")

plt.show()

# Top 10 Player of the Match Award Winners
player_awards = matches["player_of_match"].value_counts().head(10)

print("\nTop 10 Player of the Match Award Winners:")
print(player_awards)

plt.figure(figsize=(12, 6))

sns.barplot(
    x=player_awards.index,
    y=player_awards.values
)

plt.title("Top 10 Player of the Match Award Winners")
plt.xlabel("Player")
plt.ylabel("Awards Won")

plt.xticks(rotation=45)

plt.tight_layout()

plt.savefig("reports/top_players.png")

plt.show()

# Top 10 IPL Venues
venues = matches["venue"].value_counts().head(10)

print("\nTop 10 IPL Venues:")
print(venues)

plt.figure(figsize=(12,6))

sns.barplot(
    x=venues.values,
    y=venues.index
)

plt.title("Top 10 IPL Venues")
plt.xlabel("Matches Hosted")
plt.ylabel("Venue")

plt.tight_layout()

plt.savefig("reports/top_venues.png")

plt.show()

# Top 10 Run Scorers
top_batsmen = (
    deliveries.groupby("batter")["batsman_runs"]
    .sum()
    .sort_values(ascending=False)
    .head(10)
)

print("\nTop 10 Run Scorers:")
print(top_batsmen)

plt.figure(figsize=(12, 6))

sns.barplot(
    x=top_batsmen.values,
    y=top_batsmen.index
)

plt.title("Top 10 IPL Run Scorers")
plt.xlabel("Runs")
plt.ylabel("Batter")

plt.tight_layout()

plt.savefig("reports/top_run_scorers.png")

plt.show()

# Top 10 Wicket Takers
wickets = deliveries[deliveries["is_wicket"] == 1]

top_bowlers = (
    wickets.groupby("bowler")["is_wicket"]
    .sum()
    .sort_values(ascending=False)
    .head(10)
)

print("\nTop 10 Wicket Takers:")
print(top_bowlers)

plt.figure(figsize=(12,6))

sns.barplot(
    x=top_bowlers.values,
    y=top_bowlers.index
)

plt.title("Top 10 IPL Wicket Takers")
plt.xlabel("Wickets")
plt.ylabel("Bowler")

plt.tight_layout()

plt.savefig("reports/top_wicket_takers.png")

plt.show()