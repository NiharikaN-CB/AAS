import joblib
import pandas as pd

# Load model
model = joblib.load("ids_model.pkl")

# Load data
df = pd.read_csv("traffic.csv")
X = df[["packet_size", "duration", "failed_logins"]]

# Feature importance (XAI)
importance = model.feature_importances_
features = ["packet_size", "duration", "failed_logins"]

print("\n=== XAI EXPLANATION (Feature Importance) ===")
for f, imp in zip(features, importance):
    print(f"{f}: {round(imp * 100, 2)}% influence")

# Explain one sample
sample_index = 0
sample = X.iloc[sample_index]

print("\n=== SAMPLE ANALYSIS ===")
print(sample)

print("\n=== REASONING ===")

if sample["failed_logins"] > 5:
    print("High failed logins → Brute Force Attack")
elif sample["duration"] < 0.1:
    print("Very short duration → Port Scan Behavior")
else:
    print("Normal traffic pattern")