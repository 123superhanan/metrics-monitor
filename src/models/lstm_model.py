#%%
import numpy as np
def create_sequences(X, y, seq_len):

    X_sequences = []
    y_sequences = []

    for i in range(len(X) - seq_len):

        X_sequences.append(X[i:i+seq_len])

        y_sequences.append(y[i+seq_len])

    return np.array(X_sequences), np.array(y_sequences)

# %%
import pandas as pd

df = pd.read_csv("./data/processed/metrics_encoded.csv")

# Create features and target
X_df = df.drop(
    columns=[
        "timestamp",
        "anomaly_type",
        "is_anomaly"
    ]
)

y = df["is_anomaly"]

# Handle missing values in features
X_df = X_df.fillna(0)

# Convert dataframe to numpy array
X = X_df.values




# %%
from sklearn.preprocessing import StandardScaler

scaler = StandardScaler()

X = scaler.fit_transform(X)


X_seq, y_seq = create_sequences(
    X,
    y.to_numpy(),
    seq_len=20
)

print("X_seq:", X_seq.shape)
print("NaN in X_seq:", np.isnan(X_seq).sum())
# %%
from sklearn.model_selection import train_test_split

X_train, X_test, y_train, y_test = train_test_split(
    X_seq,
    y_seq,
    test_size=0.2,
    shuffle=False
)
print(X_train.shape)
print(X_test.shape)
print(y_train.shape)
print(y_test.shape)

# %%
import torch

X_train = torch.tensor(X_train, dtype=torch.float32)
X_test = torch.tensor(X_test, dtype=torch.float32)

y_train = torch.tensor(y_train, dtype=torch.float32)
y_test = torch.tensor(y_test, dtype=torch.float32)
# %%
from torch.utils.data import TensorDataset

train_dataset = TensorDataset(
    X_train,
    y_train
)

test_dataset = TensorDataset(
    X_test,
    y_test
)
#%%
from torch.utils.data import DataLoader

BATCH_SIZE = 32

train_loader = DataLoader(
    train_dataset,
    batch_size=BATCH_SIZE,
    shuffle=False
)

test_loader = DataLoader(
    test_dataset,
    batch_size=BATCH_SIZE,
    shuffle=False
)
# %%
for X_batch, y_batch in train_loader:
    print(X_batch.shape)
    print(y_batch.shape)
    break
print(np.isnan(X_seq).sum())
# %%
import torch
import torch.nn as nn

class LSTMClassifier(nn.Module):

    def __init__(self, input_size, hidden_size=64, num_layers=2):
        super().__init__()

        self.lstm = nn.LSTM(
            input_size=input_size,
            hidden_size=hidden_size,
            num_layers=num_layers,
            batch_first=True,
            dropout=0.2
        )

        self.dropout = nn.Dropout(0.3)

        self.fc = nn.Linear(hidden_size, 1)

        self.sigmoid = nn.Sigmoid()

    def forward(self, x):

        output, (hidden, cell) = self.lstm(x)

        x = hidden[-1]

        x = self.dropout(x)

        x = self.fc(x)

        x = self.sigmoid(x)

        return x
# %%
device = torch.device(
    "cuda" if torch.cuda.is_available() else "cpu"
)

model = LSTMClassifier(
    input_size=19
).to(device)

print(model)
# %%
criterion = nn.BCELoss()
# %%
optimizer = torch.optim.Adam(
    model.parameters(),
    lr=0.001
)
# %%
X_batch, y_batch = next(iter(train_loader))

X_batch = X_batch.to(device)

output = model(X_batch)

print(output.shape)
# %%
EPOCHS = 20

train_losses = []

for epoch in range(EPOCHS):

    model.train()

    running_loss = 0

    for X_batch, y_batch in train_loader:

        X_batch = X_batch.to(device)
        y_batch = y_batch.to(device).unsqueeze(1)

        optimizer.zero_grad()

        outputs = model(X_batch)

        loss = criterion(outputs, y_batch)

        loss.backward()

        optimizer.step()

        running_loss += loss.item()

    epoch_loss = running_loss / len(train_loader)

    train_losses.append(epoch_loss)

    print(f"Epoch {epoch+1}/{EPOCHS}  Loss: {epoch_loss:.4f}")
# %%
from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    confusion_matrix
)

model.eval()

predictions = []
actual = []

with torch.no_grad():

    for X_batch, y_batch in test_loader:

        X_batch = X_batch.to(device)

        outputs = model(X_batch)

        preds = (outputs >= 0.5).float()

        predictions.extend(preds.cpu().numpy().flatten())

        actual.extend(y_batch.numpy())

print("Accuracy :", accuracy_score(actual, predictions))
print("Precision:", precision_score(actual, predictions))
print("Recall   :", recall_score(actual, predictions))
print("F1 Score :", f1_score(actual, predictions))

print("\nConfusion Matrix")

print(confusion_matrix(actual, predictions))
# %%
probs = torch.sigmoid(outputs)

print(probs[:10])
# %%
print(np.isnan(X_seq).sum())
print(np.isinf(X_seq).sum())
# %%
print(np.isnan(y_seq).sum())
print(np.unique(y_seq))
# %%
from pathlib import Path
import torch

Path("saved_models").mkdir(exist_ok=True)

torch.save(
    model.state_dict(),
    "saved_models/lstm_model.pth"
)

print("LSTM model saved")
# %%

import joblib

joblib.dump(
    scaler,
    "saved_models/lstm_scaler.pkl"
)

joblib.dump(
    X_df.columns.tolist(),
    "saved_models/lstm_columns.pkl"
)

print("Scaler and columns saved")
# %%
