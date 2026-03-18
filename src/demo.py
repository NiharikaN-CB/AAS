import pandas as pd
import joblib

print("\n[AI DEFENSE SYSTEM STARTED]\n")

# Load data
df = pd.read_csv("traffic.csv")
X = df[["packet_size", "duration", "failed_logins"]]

# Load model
model = joblib.load("ids_model.pkl")
le = joblib.load("label_encoder.pkl")

# Predict
preds = model.predict(X)
labels = le.inverse_transform(preds)

print("=== DETECTION RESULTS ===\n")

for i in range(10):
    sample = X.iloc[i]
    prediction = labels[i]

    print(f"\nSample {i+1}")
    print(sample.to_dict())
    print(f"Prediction: {prediction}")

    # Explainability logic
    if sample["failed_logins"] > 5:
        print("Reason: High failed logins → brute force attack")
    elif sample["duration"] < 0.1:
        print("Reason: Very short duration → port scan")
    else:
        print("Reason: Normal behavior")

print("\n[DEMO COMPLETE]")