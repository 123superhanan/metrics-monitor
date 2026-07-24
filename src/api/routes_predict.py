from fastapi import APIRouter
from datetime import datetime
import pandas as pd
import joblib

from .schemas import MetricInput

router = APIRouter()
model = joblib.load("saved_models/random_forest_model.pkl")
scaler = joblib.load("saved_models/scaler.pkl")
expected_columns = joblib.load("saved_models/column_order.pkl")
encoders = joblib.load("saved_models/label_encoders.pkl")  # new


@router.post("/predict")
def predict(data: MetricInput):
    df = pd.DataFrame([data.model_dump()])

    now = datetime.now()
    df["day"] = now.day
    df["month"] = now.month

    df["system_load"] = (df["cpu_usage"] + df["memory_usage"] + df["disk_usage"]) / 3
    df["network_traffic"] = df["network_in"] + df["network_out"]

    # encode categorical columns using the SAME fitted encoders from training
    for column, encoder in encoders.items():
        df[column] = encoder.transform(df[column])

    df = df[expected_columns]
    scaled_data = scaler.transform(df)
    prediction = model.predict(scaled_data)[0]

    result = "Normal" if prediction == 0 else "Anomaly"
    return {"prediction": result, "class": int(prediction)}