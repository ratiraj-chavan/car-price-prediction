from flask import Flask, render_template, request
import joblib
import pandas as pd

app = Flask(__name__)

import os
import joblib

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
model_path = os.path.join(BASE_DIR, "models", "car_price_model.pkl")

model = joblib.load(model_path)
@app.route("/")
def home():
    return render_template("index.html")
@app.route("/predict", methods=["POST"])

def predict():

    try:
        vehicle_age = int(request.form["vehicle_age"])
        km_driven = int(request.form["km_driven"])

        mileage_raw = request.form["mileage"]
        max_power_raw = request.form["max_power"]


        mileage = float(mileage_raw.split()[0])
        max_power = float(max_power_raw.split()[0])

        engine = int(request.form["engine"])
        seats = int(request.form["seats"])               


        input_data = pd.DataFrame(columns=model.feature_names_in_)
        input_data.loc[0] = 0

        input_data["vehicle_age"] = vehicle_age
        input_data["km_driven"] = km_driven
        input_data["mileage"] = mileage
        input_data["engine"] = engine
        input_data["max_power"] = max_power
        input_data["seats"] = seats

        prediction = model.predict(input_data)[0]

        result = f"₹ {int(prediction):,}"

    except Exception as e:
        print("Prediction error:", e)
        result = "Error in prediction input"

    return render_template("index.html", prediction_text=result)
if __name__ == "__main__":
    app.run(debug=True)