from pathlib import Path
import pandas as pd
from sklearn.preprocessing import LabelEncoder
import joblib


def load_data(file_path):
    return pd.read_csv(file_path)


def encode_features(df):
    categorical_columns = [
        "service_name",
        "region",
        "deployment_version",
        "day_of_week"
    ]

    encoders = {}

    for column in categorical_columns:
        encoder = LabelEncoder()
        df[column] = encoder.fit_transform(df[column])
        encoders[column] = encoder

    return df, encoders


def save_encoders(encoders, path):
    path.parent.mkdir(parents=True, exist_ok=True)
    joblib.dump(encoders, path)


def save_data(df, path):
    path.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(path, index=False)


def main():
    input_file = Path("data/processed/metrics_preprocessed.csv")
    output_file = Path("data/processed/metrics_encoded.csv")
    encoder_file = Path("saved_models/label_encoders.pkl")

    df = load_data(input_file)

    print("Before encoding:")
    print(df.dtypes)

    df, encoders = encode_features(df)

    print("\nAfter encoding:")
    print(df.dtypes)

    save_data(df, output_file)
    save_encoders(encoders, encoder_file)

    print("\nEncoded data saved:", output_file)
    print("Encoders saved:", encoder_file)


if __name__ == "__main__":
    main()