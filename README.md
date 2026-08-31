# Enterprise AI Infrastructure Platform

Infrastructure for deploying and operating machine learning inference workloads using PyTorch, FastAPI, Docker, Kubernetes, MLflow, GitHub Actions, Prometheus, and Terraform.

The platform supports model training and experiment tracking, containerized API based inference, Kubernetes orchestration, runtime monitoring, automated testing, CI based container publishing, performance benchmarking, and infrastructure as code configuration for AWS.

## Architecture

```text
                    ┌─────────────────────┐
                    │   PyTorch Training  │
                    └──────────┬──────────┘
                               │
                               ▼
                    ┌─────────────────────┐
                    │       MLflow        │
                    │ Experiments/Models  │
                    └──────────┬──────────┘
                               │
                               ▼
                    ┌─────────────────────┐
                    │   FastAPI Service   │
                    │   Model Inference   │
                    └──────────┬──────────┘
                               │
                               ▼
                    ┌─────────────────────┐
                    │       Docker        │
                    │ Containerized API   │
                    └──────────┬──────────┘
                               │
                               ▼
                    ┌─────────────────────┐
                    │        GHCR         │
                    │  Container Registry │
                    └──────────┬──────────┘
                               │
                               ▼
                    ┌─────────────────────┐
                    │     Kubernetes      │
                    │ Deployment/Service  │
                    └──────────┬──────────┘
                               │
                    ┌──────────┴──────────┐
                    ▼                     ▼
             Health Probes        Prometheus Metrics
```

## Core Components

### Model Training

PyTorch training pipeline with hardware-aware execution across Apple MPS, NVIDIA CUDA, and CPU environments.

MLflow records experiment parameters, training metrics, execution time, and model artifacts.

### Model Serving

FastAPI exposes the trained model through:

- `GET /` — service health
- `POST /predict` — model inference
- `GET /metrics` — inference statistics
- `GET /metrics/prometheus` — Prometheus-compatible metrics

Prediction requests are validated before inference and invalid feature dimensions return HTTP 422 responses.

### Containers & Kubernetes

The inference service is packaged as a Docker image and published to GitHub Container Registry through GitHub Actions.

Kubernetes manages the inference workload with:

- Deployment and Service resources
- readiness and liveness probes
- CPU and memory requests/limits
- automatic image retrieval from GHCR

The containerized service has been successfully deployed and verified on a local Kubernetes cluster.

### Monitoring

The API tracks inference request counts, successful predictions, and request latency.

Prometheus-compatible counters and latency histograms are exposed through `/metrics/prometheus` for external monitoring systems.

### Testing & CI

The automated pytest suite covers:

- service health
- prediction requests
- response types
- malformed input
- incorrect model feature dimensions
- runtime metrics
- Prometheus metrics

GitHub Actions runs the test suite on pushes and pull requests. Successful pushes to `main` build the Docker image and publish it to GitHub Container Registry.

### Infrastructure as Code

Terraform defines an AWS infrastructure foundation including:

- EC2 compute
- security group configuration
- configurable region and instance type
- infrastructure outputs

The Terraform configuration has been initialized, formatted, and successfully validated with the Terraform CLI. It has not been applied to AWS.

## Performance Benchmarking

The benchmark utility measures inference latency across repeated API requests.

Example warm-run results from the local Kubernetes deployment:

```text
Requests: 20
Average latency: 0.0025 sec
Fastest request: 0.0015 sec
Slowest request: 0.0179 sec
```

These measurements represent local development performance and are not cloud or production benchmarks.

## Run Locally

### Install dependencies

```bash
pip install -r requirements.txt
```

### Start the inference API

```bash
uvicorn src.inference.app:app --host 0.0.0.0 --port 8000
```

API documentation:

```text
http://localhost:8000/docs
```

### Run tests

```bash
pytest -q
```

### Build the Docker image

```bash
docker build -f docker/Dockerfile -t enterprise-ai-inference .
```

### Deploy to Kubernetes

```bash
kubectl apply -f kubernetes/deployment.yaml
kubectl apply -f kubernetes/service.yaml
kubectl rollout status deployment/enterprise-ai-inference
```

### Run the benchmark

```bash
python benchmarks/benchmark_api.py
```

## Project Structure

```text
enterprise-ai-infrastructure/
├── .github/
│   └── workflows/
│       └── ci.yml
├── benchmarks/
│   └── benchmark_api.py
├── docker/
│   └── Dockerfile
├── kubernetes/
│   ├── deployment.yaml
│   └── service.yaml
├── models/
│   └── model.pth
├── src/
│   ├── inference/
│   │   └── app.py
│   └── training/
│       ├── model.py
│       └── train.py
├── terraform/
│   ├── main.tf
│   ├── outputs.tf
│   └── variables.tf
├── tests/
│   └── test_api.py
├── pytest.ini
└── requirements.txt
```

## Technology Stack

**Machine Learning:** PyTorch  
**Experiment Tracking:** MLflow  
**API:** FastAPI  
**Containers:** Docker  
**Container Registry:** GitHub Container Registry  
**Orchestration:** Kubernetes  
**Monitoring:** Prometheus-compatible metrics  
**Testing:** pytest  
**CI:** GitHub Actions  
**Infrastructure as Code:** Terraform  
**Cloud Configuration:** AWS

## Current Status

Verified components include:

- PyTorch model training
- MLflow experiment and artifact tracking
- FastAPI inference service
- input validation and error handling
- Docker containerization
- GitHub Actions automated testing
- GHCR container publishing
- Kubernetes deployment and service
- Kubernetes health probes and resource controls
- Prometheus-compatible inference metrics
- API performance benchmarking
- Terraform CLI validation

AWS infrastructure deployment and a standalone Prometheus/Grafana monitoring stack are outside the current implementation.
