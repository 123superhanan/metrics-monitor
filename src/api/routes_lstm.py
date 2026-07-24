
from fastapi import APIRouter
import torch
import numpy as np
import joblib
from collections import deque
from datetime import datetime
from .schemas import MetricInput
from src.models.lstm_model import LSTMClassifier


router = APIRouter()


# Load model
model = LSTMClassifier(
    input_size=19
)
encoders = joblib.load(
    "saved_models/label_encoders.pkl"
)
model.load_state_dict(
    torch.load(
        "saved_models/lstm_model.pth",
        map_location="cpu"
    )
)

model.eval()


# Load scaler
scaler = joblib.load(
    "saved_models/lstm_scaler.pkl"
)


# Store last 20 metrics
sequence_buffer = deque(maxlen=20)


@router.post("/predict-lstm")
def predict_lstm(data: MetricInput):

    df = data.model_dump()
    for column, encoder in encoders.items():
        df[column] = encoder.transform(
            [df[column]]
        )[0]
    df["system_load"] = (
        df["cpu_usage"]
        + df["memory_usage"]
        + df["disk_usage"]
    ) / 3

    df["network_traffic"] = (
        df["network_in"]
        + df["network_out"]
    )

    features = [
    df["cpu_usage"],
    df["memory_usage"],
    df["disk_usage"],
    df["disk_io"],
    df["network_in"],
    df["network_out"],
    df["response_time"],
    df["request_count"],
    df["error_rate"],
    df["active_users"],
    df["service_name"],
    df["region"],
    df["deployment_version"],
    df["day_of_week"],
    df["hour"],
    df.get("day",0),
    df.get("month",0),
    df["system_load"],
    df["network_traffic"]
]
        


    scaled = scaler.transform(
        [features]
    )[0]


    sequence_buffer.append(scaled)


    if len(sequence_buffer) < 20:
        return {
            "prediction": "Collecting data",
            "samples": len(sequence_buffer)
        }


    sequence = np.array(
        sequence_buffer
    )


    sequence = torch.tensor(
        sequence,
        dtype=torch.float32
    )


    sequence = sequence.unsqueeze(0)


    with torch.no_grad():

        output = model(sequence)

        probability = output.item()


        prediction = 1 if probability >= 0.5 else 0


    return {
        "prediction": "Anomaly" if prediction else "Normal",
        "class": prediction,
        "confidence": round(probability,4)
    }