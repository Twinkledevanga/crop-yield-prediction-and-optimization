from flask import Flask, render_template, request, redirect, url_for, flash
import joblib
import numpy as np
import os

app = Flask(__name__)
app.secret_key = "supersecretkey"

# ------------------ Load Model ------------------
MODEL_PATH = "models/crop_yield_model.pkl"
if not os.path.exists(MODEL_PATH):
    raise FileNotFoundError(f"Model not found at {MODEL_PATH}")

model_data = joblib.load(MODEL_PATH)
model = model_data["model"]
le_state = model_data["le_state"]
le_district = model_data["le_district"]
le_crop = model_data["le_crop"]
features = model_data["features"]

STATE_DISTRICTS = {
    "Karnataka": ["Bangalore", "Mysore", "Mangalore"],
    "AP": ["Vijayawada", "Guntur", "Tirupati"],
    "TN": ["Chennai", "Coimbatore", "Madurai"],
    "MP": ["Indore", "Bhopal", "Jabalpur"],
    "Telangana": ["Hyderabad", "Warangal", "Nizamabad"],
    "Kerala": ["Thiruvananthapuram", "Kochi", "Kozhikode"],
    "Goa": ["Panaji", "Margao"]
}

CROPS = ["Wheat", "Rice", "Ragi", "Maize", "Cotton", "Sugarcane"]

# Historical data storage
historical_data = []

# ------------------ Routes ------------------
@app.route("/", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        if username == "admin" and password == "admin":
            return redirect(url_for("dashboard"))
        else:
            flash("Invalid credentials")
    return render_template("login.html")


@app.route("/dashboard", methods=["GET", "POST"])
def dashboard():
    prediction_chart = None
    optimization_chart = None
    historical_chart = None
    profit_chart = None
    suggestions = None

    # Example input for demonstration
    yield_pred = None
    cost = None
    revenue = None
    profit = None

    if request.method == "POST":
        # Prediction inputs
        try:
            state = request.form["state"]
            district = request.form["district"]
            crop = request.form["crop"]
            area = float(request.form["area"])
            production = float(request.form["production"])
            rainfall = float(request.form["rainfall"])
            fertilizer = float(request.form["fertilizer"])
            pesticide = float(request.form["pesticide"])
            cost_per_unit = float(request.form["cost_per_unit"])
            selling_price = float(request.form["selling_price"])
        except (ValueError, KeyError):
            flash("Please enter valid numeric values")
            return redirect(url_for("dashboard"))

        # Encode categorical inputs
        state_enc = le_state.transform([state])[0]
        district_enc = le_district.transform([district])[0]
        crop_enc = le_crop.transform([crop])[0]

        X_input = np.array([[state_enc, district_enc, crop_enc, area, production, rainfall, fertilizer, pesticide]])
        yield_pred = round(model.predict(X_input)[0], 2)

        # Optimization suggestions
        suggestions = {
            "rainfall": "Increase rainfall to ~920 mm/year" if rainfall < 900 else "Rainfall sufficient",
            "fertilizer": "Increase fertilizer usage" if fertilizer < 50 else "Fertilizer sufficient",
            "pesticide": "Increase pesticide usage" if pesticide < 5 else "Pesticide sufficient"
        }

        # Profit/Cost
        cost = cost_per_unit * area
        revenue = selling_price * yield_pred * area
        profit = round(revenue - cost, 2)

        # Save historical data
        historical_data.append({
            "crop": crop,
            "district": district,
            "predicted_yield": yield_pred
        })

    return render_template(
        "dashboard.html",
        states=list(STATE_DISTRICTS.keys()),
        crops=CROPS,
        DISTRICTS=STATE_DISTRICTS,
        yield_pred=yield_pred,
        suggestions=suggestions,
        historical_data=historical_data,
        cost=cost,
        revenue=revenue,
        profit=profit
    )


# ------------------ Run ------------------
if __name__ == "__main__":
    app.run(debug=True)
