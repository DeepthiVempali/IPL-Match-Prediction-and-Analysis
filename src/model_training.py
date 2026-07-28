import pandas as pd

# Load cleaned matches dataset
matches = pd.read_csv("data/processed/matches_cleaned.csv")

print("Dataset Loaded Successfully!")

print("\nDataset Shape:")
print(matches.shape)

print("\nColumns:")
print(matches.columns)

# Select Features (Input)
X = matches[[
    "team1",
    "team2",
    "toss_winner",
    "toss_decision",
    "venue",
    "city"
]]

# Select Target (Output)
y = matches["winner"]

print("\nFeatures Selected:")
print(X.head())

print("\nTarget Variable:")
print(y.head())

from sklearn.preprocessing import LabelEncoder

# Store encoders for each column
encoders = {}

# Encode each feature column
for column in X.columns:
    le = LabelEncoder()
    X[column] = le.fit_transform(X[column])
    encoders[column] = le

# Encode target
target_encoder = LabelEncoder()
y = target_encoder.fit_transform(y)



print("\nEncoded Features:")
print(X.head())

print("\nEncoded Target:")
print(y[:5])

from sklearn.model_selection import train_test_split

# Split the dataset
X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42
)

print("\nTraining Data Shape:", X_train.shape)
print("Testing Data Shape:", X_test.shape)

print("\nTraining Target Shape:", y_train.shape)
print("Testing Target Shape:", y_test.shape)

from sklearn.ensemble import RandomForestClassifier

# Create the model
model = RandomForestClassifier(
    n_estimators=100,
    random_state=42
)

# Train the model
model.fit(X_train, y_train)

print("\nModel trained successfully!")

from sklearn.metrics import accuracy_score, classification_report

# Make predictions on test data
y_pred = model.predict(X_test)

# Calculate accuracy
accuracy = accuracy_score(y_test, y_pred)

print("\nModel Accuracy:")
print(f"{accuracy * 100:.2f}%")

# Print detailed report
print("\nClassification Report:")
print(classification_report(y_test, y_pred))

import joblib
import os

# Create models folder if it doesn't exist
os.makedirs("models", exist_ok=True)

# Save the trained model
joblib.dump(model, "models/ipl_winner_prediction_model.pkl")

print("\nModel saved successfully!")
# Save encoders
joblib.dump(encoders, "models/feature_encoders.pkl")
joblib.dump(target_encoder, "models/target_encoder.pkl")

print("Encoders saved successfully!")