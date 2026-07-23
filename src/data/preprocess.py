from pathlib import Path
import pandas as pd


def load_data(file_path):
    return pd.read_csv(",,/../data/raw/metrics.csv")


def preprocess_data(df):
    df["timestamp"] = pd.to_datetime(df["timestamp"], errors="coerce")

    df = df.sort_values("timestamp").reset_index(drop=True)

    numeric_columns = [
        "cpu_usage",
        "memory_usage",
        "disk_usage",
        "disk_io",
        "network_in",
        "network_out",
        "response_time",
        "request_count",
        "error_rate",
        "active_users",
    ]

    for column in numeric_columns:
        df[column] = df[column].interpolate(method="linear")
        df[column] = df[column].fillna(df[column].median())

    categorical_columns = [
        "service_name",
        "region",
        "deployment_version",
        "day_of_week",
        "anomaly_type",
    ]

    for column in categorical_columns:
        df[column] = df[column].fillna(df[column].mode()[0])

    df["hour"] = df["timestamp"].dt.hour
    df["day"] = df["timestamp"].dt.day
    df["month"] = df["timestamp"].dt.month

    df["system_load"] = (
        df["cpu_usage"]
        + df["memory_usage"]
        + df["disk_usage"]
    ) / 3

    df["network_traffic"] = (
        df["network_in"]
        + df["network_out"]
    )

    return df


def save_data(df, output_path):
    output_path.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(output_path, index=False)


def main():
    input_file = Path("data/raw/metrics.csv")
    output_file = Path("data/processed/metrics_preprocessed.csv")

    df = load_data(input_file)

    print("Original shape:", df.shape)

    df = preprocess_data(df)

    print("Processed shape:", df.shape)
    print(df.isnull().sum())

    save_data(df, output_file)


if __name__ == "__main__":
    main()