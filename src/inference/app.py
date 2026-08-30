from fastapi import FastAPI
from pydantic import BaseModel
import torch

from src.training.model import AIModel


# Create FastAPI application
app = FastAPI(
    title="Enterprise AI Inference Service",
    description="Production-oriented model inference API",
    version="1.0.0",
)


# Select available device
if torch.backends.mps.is_available():
    device = torch.device("mps")
elif torch.cuda.is_available():
    device = torch.device("cuda")
else:
    device = torch.device("cpu")


# Create model
model = AIModel().to(device)


# Load trained model
model.load_state_dict(
    torch.load(
        "models/model.pth",
        map_location=device,
    )
)


# Put model into inference mode
model.eval()


# Request format for predictions
class PredictionRequest(BaseModel):
    features: list[float]


# Health check endpoint
@app.get("/")
def health_check():
    return {
        "status": "healthy",
        "service": "enterprise-ai-inference",
        "device": str(device),
    }


# Prediction endpoint
@app.post("/predict")
def predict(request: PredictionRequest):

    # Get features from request
    features = request.features

    # Make sure the model receives exactly 10 features
    if len(features) != 10:
        return {
            "error": "Model requires exactly 10 features."
        }

    # Convert input into a PyTorch tensor
    X = torch.tensor(
        [features],
        dtype=torch.float32,
        device=device,
    )

    # Run inference without calculating gradients
    with torch.no_grad():

        # Run the model
        output = model(X)

        # Find predicted class
        prediction = torch.argmax(
            output,
            dim=1,
        ).item()

    return {
        "prediction": prediction,
        "device": str(device),
    }