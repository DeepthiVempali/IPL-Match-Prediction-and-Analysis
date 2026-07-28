import pandas as pd

# Load datasets
matches = pd.read_csv("data/matches.csv")
deliveries = pd.read_csv("data/deliveries.csv")

# Dataset information
print("========== MATCHES DATASET ==========")
print(matches.info())

print("\n========== DELIVERIES DATASET ==========")
print(deliveries.info())

# Missing values
print("\nMissing Values in Matches:")
print(matches.isnull().sum())

print("\nMissing Values in Deliveries:")
print(deliveries.isnull().sum())