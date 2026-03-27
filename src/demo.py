import pandas as pd
import joblib
import time

print("\n⚔️ AI-DRIVEN CYBER ATTACK vs 🛡️ DEFENSE SYSTEM\n")

# Load data
df = pd.read_csv("traffic.csv")
X = df[["packet_size", "duration", "failed_logins"]]

# Load model
model = joblib.load("ids_model.pkl")
le = joblib.load("label_encoder.pkl")

preds = model.predict(X)
labels = le.inverse_transform(preds)

attack_log = []

print("🔍 Phase 1: Reconnaissance (Scanning Target Network...)\n")
time.sleep(1)

for i in range(3):
    sample = X.iloc[i]
    print(f"📡 Scanning Packet {i+1}: {sample.to_dict()}")
    time.sleep(0.5)

print("\n⚠️ Phase 2: Initial Access Attempt (Brute Force Login)\n")
time.sleep(1)

for i in range(3, 6):
    sample = X.iloc[i]
    prediction = labels[i]

    print(f"🔐 Login Attempt Packet {i+1}: {sample.to_dict()}")

    if prediction != "normal":
        print("🚨 ALERT: Suspicious login detected!")
        print("🛑 ACTION: Blocking IP address")
        
        reason = "High failed logins → Brute Force Attack"
        print(f"🧠 REASON: {reason}")

        attack_log.append((i+1, prediction, reason))

    time.sleep(0.5)

print("\n💣 Phase 3: Exploitation Attempt (Abnormal Traffic)\n")
time.sleep(1)

for i in range(6, 10):
    sample = X.iloc[i]
    prediction = labels[i]

    print(f"📦 Packet {i+1}: {sample.to_dict()}")

    if prediction != "normal":
        print("🚨 ALERT: Malicious traffic detected!")
        print("🛑 ACTION: Dropping packets")

        if sample["duration"] < 0.1:
            reason = "Very short duration → Port Scan"
        else:
            reason = "Unusual traffic pattern"

        print(f"🧠 REASON: {reason}")

        attack_log.append((i+1, prediction, reason))
    else:
        print("✅ Normal traffic")

    time.sleep(0.5)

print("\n🛡️ DEFENSE SYSTEM SUMMARY\n")

for log in attack_log:
    print(f"Packet {log[0]} → {log[1]} ({log[2]})")

print("\n✅ SYSTEM SUCCESSFULLY DEFENDED AGAINST ATTACK\n")