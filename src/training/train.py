import time

import torch
import torch.nn as nn
import torch.optim as optim
import mlflow

mlflow.set_tracking_uri("http://127.0.0.1:5000")

from model import AIModel


if torch.backends.mps.is_available():
    device = torch.device("mps")
elif torch.cuda.is_available():
    device = torch.device("cuda")
else:
    device = torch.device("cpu")


print("Training device:", device)


# Create synthetic training data
X = torch.randn(1000, 10)

# Create binary labels
y = (X.sum(dim=1) > 0).long()


# Move data to the selected device
X = X.to(device)
y = y.to(device)


# Create model
model = AIModel().to(device)


# Loss function
criterion = nn.CrossEntropyLoss()

# Optimizer
optimizer = optim.Adam(model.parameters(), lr=0.001)


# Number of training cycles
epochs = 10

# MLflow experiment
mlflow.set_experiment("enterprise-ai-training")

# Start MLflow run
with mlflow.start_run():

    # Log training settings
    mlflow.log_param("epochs", epochs)
    mlflow.log_param("learning_rate", 0.001)
    mlflow.log_param("device", str(device))

    # Start timing
    start_time = time.time()

    # Training loop
    for epoch in range(epochs):

        # Make predictions
        predictions = model(X)

        # Calculate loss
        loss = criterion(predictions, y)

        # Clear old gradients
        optimizer.zero_grad()

        # Calculate gradients
        loss.backward()

        # Update the model
        optimizer.step()

        # Record loss in MLflow
        mlflow.log_metric("loss", loss.item(), step=epoch)

        print(
            f"Epoch {epoch + 1}/{epochs} "
            f"- Loss: {loss.item():.4f}"
        )

    # Calculate training time
    training_time = time.time() - start_time

    # Record training time in MLflow
    mlflow.log_metric("training_time_seconds", training_time)

    print()
    print("Training complete!")
    print(f"Training time: {training_time:.2f} seconds")

    # Save the trained model
    torch.save(model.state_dict(), "../../models/model.pth")

    print("Model saved successfully!")