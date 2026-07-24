from pathlib import Path
import pandas as pd
import joblib

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    confusion_matrix
)


def load_data(file_path):
    return pd.read_csv(file_path)


def prepare_data(df):
    X = df.drop(
        [
            "is_anomaly",
            "timestamp",
            "anomaly_type"
        ],
        axis=1
    )

    y = df["is_anomaly"]

    return X, y


def train_model(X_train, y_train):
    model = RandomForestClassifier(
        n_estimators=100,
        random_state=42,
        class_weight="balanced"
    )

    model.fit(X_train, y_train)

    return model


def evaluate_model(model, X_test, y_test):
    predictions = model.predict(X_test)

    print("Accuracy:", accuracy_score(y_test, predictions))
    print("Precision:", precision_score(y_test, predictions))
    print("Recall:", recall_score(y_test, predictions))
    print("F1 Score:", f1_score(y_test, predictions))

    print("\nConfusion Matrix:")
    print(confusion_matrix(y_test, predictions))


def save_model(model, scaler, column_order):
    Path("saved_models").mkdir(exist_ok=True)

    joblib.dump(model, "saved_models/random_forest_model.pkl")
    joblib.dump(scaler, "saved_models/scaler.pkl")
    joblib.dump(column_order, "saved_models/column_order.pkl")


def main():
    file_path = "data/processed/metrics_encoded.csv"

    df = load_data(file_path)
    X, y = prepare_data(df)

    # capture column order BEFORE train_test_split/scaling turns X into arrays
    column_order = X.columns.tolist()

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )

    scaler = StandardScaler()
    X_train = scaler.fit_transform(X_train)
    X_test = scaler.transform(X_test)

    model = train_model(X_train, y_train)
    evaluate_model(model, X_test, y_test)

    save_model(model, scaler, column_order)


if __name__ == "__main__":
    main()