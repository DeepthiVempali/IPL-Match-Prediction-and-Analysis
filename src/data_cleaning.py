import pandas as pd
matches = pd.read_csv("data/matches.csv")
deliveries = pd.read_csv("data/deliveries.csv")

print("Datasets loaded successfully!")

print("Duplicate rows in Matches:", matches.duplicated().sum())
print("Duplicate rows in Deliveries:", deliveries.duplicated().sum())

matches.drop_duplicates(inplace=True)
deliveries.drop_duplicates(inplace=True)

print("\nMissing Values in Matches:")
print(matches.isnull().sum())

print("\nMissing Values in Deliveries:")
print(deliveries.isnull().sum())

matches["city"] = matches["city"].fillna("Unknown")
matches["player_of_match"] = matches["player_of_match"].fillna("No Award")
matches["winner"] = matches["winner"].fillna("No Result")
matches["method"] = matches["method"].fillna("Normal")
matches["result_margin"] = matches["result_margin"].fillna(0)
matches["target_runs"] = matches["target_runs"].fillna(0)
matches["target_overs"] = matches["target_overs"].fillna(0)

matches["date"] = pd.to_datetime(matches["date"])

print("\nData Types:")
print(matches.dtypes)

team_replacements = {
    "Delhi Daredevils": "Delhi Capitals",
    "Kings XI Punjab": "Punjab Kings",
    "Rising Pune Supergiant": "Rising Pune Supergiants"
}

matches.replace(team_replacements, inplace=True)
deliveries.replace(team_replacements, inplace=True)

print("\nRemaining Missing Values:")
print(matches.isnull().sum())

matches.to_csv("data/processed/matches_cleaned.csv", index=False)
deliveries.to_csv("data/processed/deliveries_cleaned.csv", index=False)

print("\nCleaned datasets saved successfully!")