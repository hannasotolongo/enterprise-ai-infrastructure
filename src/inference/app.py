from fastapi import FastAPI, Response
from pydantic import BaseModel
import torch
import time

from prometheus_client import (
    Counter,
    Histogram,
    generate_latest,
    CONTENT_TYPE_LATEST,
)

from src.training.model import AIModel


app = FastAPI(
    title="Enterprise AI Inference Service",
    description="Production-oriented model inference API",
    version="1.0.0",
)


prediction_requests = 0
successful_predictions = 0
total_prediction_time = 0.0


PREDICTION_REQUESTS = Counter(
    "inference_requests_total",
    "Total number of inference requests",
)

PREDICTION_SUCCESSES = Counter(
    "inference_successes_total",
    "Total number of successful inference requests",
)

PREDICTION_LATENCY = Histogram(
    "inference_latency_seconds",
    "Inference request latency in seconds",
)


if torch.backends.mps.is_available():
    device = torch.device("mps")
elif torch.cuda.is_available():
    device = torch.device("cuda")
else:
    device = torch.device("cpu")


model = AIModel().to(device)

model.load_state_dict(
    torch.load(
        "models/model.pth",
        map_location=device,
    )
)

model.eval()


class PredictionRequest(BaseModel):
    features: list[float]


@app.get("/")
def health_check():
    return {
        "status": "healthy",
        "service": "enterprise-ai-inference",
        "device": str(device),
    }


@app.post("/predict")
def predict(request: PredictionRequest):
    global prediction_requests
    global successful_predictions
    global total_prediction_time

    prediction_requests += 1
    PREDICTION_REQUESTS.inc()

    start_time = time.time()

    features = request.features

    if len(features) != 10:
        return {
            "error": "Model requires exactly 10 features."
        }

    X = torch.tensor(
        [features],
        dtype=torch.float32,
        device=device,
    )

    with torch.no_grad():
        output = model(X)

        prediction = torch.argmax(
            output,
            dim=1,
        ).item()

    prediction_time = time.time() - start_time

    successful_predictions += 1
    total_prediction_time += prediction_time

    PREDICTION_SUCCESSES.inc()
    PREDICTION_LATENCY.observe(prediction_time)

    return {
        "prediction": prediction,
        "device": str(device),
    }


@app.get("/metrics")
def metrics():
    average_latency = (
        total_prediction_time / successful_predictions
        if successful_predictions > 0
        else 0
    )

    return {
        "prediction_requests": prediction_requests,
        "successful_predictions": successful_predictions,
        "average_prediction_latency_seconds": average_latency,
        "device": str(device),
    }


@app.get("/metrics/prometheus")
def prometheus_metrics():
    return Response(
        content=generate_latest(),
        media_type=CONTENT_TYPE_LATEST,
    )