# 🛡️ AI Cyber Defense System (AAS)

An AI-powered intrusion detection system that simulates cyber attacks and defends against them using machine learning and explainable AI.

---

## 🚀 Overview

This project demonstrates a complete cybersecurity pipeline:

* ⚔️ **Attacker Module** → Simulates network traffic (normal + malicious)
* 🧠 **AI Defense Model** → Detects attacks using Machine Learning
* 🛡️ **Defense Simulation** → Responds to threats in real-time
* 🔍 **Explainable AI (XAI)** → Explains why attacks are detected

---

## 🧩 Project Structure

```
AAS/
│── attacker.py      # Generates synthetic network traffic
│── ids_model.py     # Trains ML model (Random Forest)
│── demo.py          # Simulates attack vs defense system
│── explain.py       # Explains model decisions (XAI)
│── traffic.csv      # Generated dataset
│── ids_model.pkl    # Trained model
│── label_encoder.pkl
```

---

## ⚙️ How It Works

### 1️⃣ Traffic Generation (Attacker)

* Simulates:

  * Normal traffic
  * Port scanning attacks
  * Brute force attacks
* Generates features:

  * `packet_size`
  * `duration`
  * `failed_logins`

---

### 2️⃣ Model Training (Defender)

* Uses **Random Forest Classifier**
* Learns patterns of malicious behavior
* Saves trained model for detection

---

### 3️⃣ Attack vs Defense Simulation

* Simulates real attack phases:

  * Reconnaissance
  * Initial Access (Brute Force)
  * Exploitation
* System responds by:

  * 🚨 Detecting threats
  * 🛑 Blocking attackers
  * 📦 Dropping malicious packets

---

### 4️⃣ Explainable AI (XAI)

* Shows feature importance
* Provides human-readable reasoning:

  * High failed logins → Brute force
  * Short duration → Port scan

---

## 🧪 How to Run

```bash
# Step 1: Generate traffic
python attacker.py

# Step 2: Train model
python ids_model.py

# Step 3: Run simulation
python demo.py

# Step 4: Explain predictions
python explain.py
```

---

## 📊 Example Output

```
🚨 ALERT: Suspicious login detected!
🛑 ACTION: Blocking IP address
🧠 REASON: High failed logins → Brute Force Attack
```

---

## 🧠 Key Concepts

* Intrusion Detection Systems (IDS)
* Machine Learning for Cybersecurity
* Behavioral Analysis
* Explainable AI (XAI)

---

## 🔥 Future Improvements

* Real-time packet capture (Scapy/Wireshark)
* Web dashboard for monitoring
* Advanced attack simulations
* Integration with SIEM tools

---

## 👩‍💻 Author

**Niharika Niranjan**
Cybersecurity Student | AI + Security Enthusiast

---

## ⭐ If you found this useful

Give this repo a ⭐ and feel free to contribute!
