# train_model.py
import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import LabelEncoder
import joblib
import os

DATA_FILE = "crop_data.csv"
MODEL_FILE = "models/crop_yield_model.pkl"

def train_model():
    if not os.path.exists(DATA_FILE):
        print("❌ ERROR: put your training CSV named 'crop_data.csv' in the project folder.")
        return

    df = pd.read_csv(DATA_FILE)

    features = ["State", "District", "Crop", "Area", "Production", "Rainfall", "Fertilizer", "Pesticide"]
    target = "Yield"

    # Encode categorical features
    le_state = LabelEncoder()
    le_district = LabelEncoder()
    le_crop = LabelEncoder()

    df["State"] = le_state.fit_transform(df["State"])
    df["District"] = le_district.fit_transform(df["District"])
    df["Crop"] = le_crop.fit_transform(df["Crop"])

    X = df[features]
    y = df[target]

    model = RandomForestRegressor(n_estimators=100, random_state=42)
    model.fit(X, y)

    os.makedirs("models", exist_ok=True)
    joblib.dump({
        "model": model,
        "le_state": le_state,
        "le_district": le_district,
        "le_crop": le_crop,
        "features": features
    }, MODEL_FILE)

    print("✅ Model saved at", MODEL_FILE)

if __name__ == "__main__":
    train_model()
