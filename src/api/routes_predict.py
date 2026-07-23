from fastapi import APIRouter
import pandas as pd
import joblib

from .schemas import MetricInput


router = APIRouter()


model = joblib.load(
    "saved_models/random_forest_model.pkl"
)

scaler = joblib.load(
    "saved_models/scaler.pkl"
)


@router.post("/predict")
def predict(data: MetricInput):

    df = pd.DataFrame([data.model_dump()])

    df["day"] = 10
    df["month"] = 7

    df["system_load"] = (
        df["cpu_usage"]
        + df["memory_usage"]
        + df["disk_usage"]
    ) / 3

    df["network_traffic"] = (
        df["network_in"]
        + df["network_out"]
    )

    scaled_data = scaler.transform(df)

    prediction = model.predict(
        scaled_data
    )[0]

    if prediction == 0:
        result = "Normal"
    else:
        result = "Anomaly"

    return {
        "prediction": result,
        "class": int(prediction)
    }