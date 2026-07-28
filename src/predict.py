import joblib
import pandas as pd

# Load saved model and encoders
model = joblib.load("models/ipl_winner_prediction_model.pkl")
encoders = joblib.load("models/feature_encoders.pkl")
target_encoder = joblib.load("models/target_encoder.pkl")

print("===== IPL Winner Prediction =====")

# Take user input
team1 = input("Enter Team 1: ").strip()
team2 = input("Enter Team 2: ").strip()
toss_winner = input("Enter Toss Winner: ").strip()
toss_decision = input("Enter Toss Decision (bat/field): ").strip()
venue = input("Enter Venue: ").strip()
city = input("Enter City: ").strip()
# Create DataFrame
new_match = pd.DataFrame({
    "team1": [team1],
    "team2": [team2],
    "toss_winner": [toss_winner],
    "toss_decision": [toss_decision],
    "venue": [venue],
    "city": [city]
})

# Encode input
for column in new_match.columns:
    new_match[column] = encoders[column].transform(new_match[column])

# Predict
prediction = model.predict(new_match)

# Decode prediction
winner = target_encoder.inverse_transform(prediction)

print("\n🏆 Predicted Winner:", winner[0])