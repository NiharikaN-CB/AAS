import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
import joblib

# Load data
df = pd.read_csv("traffic.csv")

X = df[["packet_size", "duration", "failed_logins"]]
y = df["label"]

le = LabelEncoder()
y = le.fit_transform(y)

# Train
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)

model = RandomForestClassifier()
model.fit(X_train, y_train)

# Save model
joblib.dump(model, "ids_model.pkl")
joblib.dump(le, "label_encoder.pkl")

print("Model trained and saved!")