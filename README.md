# Enterprise AI Infrastructure Platform

Infrastructure for deploying and operating machine learning inference workloads using PyTorch, FastAPI, Docker, Kubernetes, MLflow, GitHub Actions, and Terraform.

The platform supports model training and experiment tracking, containerized API-based inference, Kubernetes orchestration, runtime monitoring, automated testing, CI validation, and infrastructure-as-code configuration for AWS.

## Architecture

```text
                    Client
                      │
                      ▼
                FastAPI API
               /predict  /metrics
                      │
                      ▼
                 PyTorch Model
                      │
                      ▼
               Docker Container
                      │
                      ▼
                  Kubernetes
               ┌──────┴──────┐
               │             │
          Deployment       Service
               │
        Health Probes
        Resource Limits


Training ──────► MLflow
                 │
          Metrics + Artifacts


Git Push ──────► GitHub Actions
                 │
              Tests
                 │
              Docker Build


Terraform ─────► AWS Infrastructure
                 Configuration
```

## Core Components

**Model Training**
- PyTorch training pipeline
- MPS/CUDA/CPU device selection
- Model serialization

**Model Serving**
- FastAPI inference service
- `/predict` prediction endpoint
- `/` health endpoint
- `/metrics` runtime metrics endpoint

**MLOps**
- MLflow experiment tracking
- Training parameter and metric logging
- Model artifact storage
- Inference latency benchmarking

**Containers & Orchestration**
- Dockerized inference service
- Kubernetes Deployment and Service
- Readiness and liveness probes
- CPU and memory resource controls

**Testing & CI**
- Automated API tests with Pytest
- Input validation and response contract tests
- GitHub Actions CI on pushes and pull requests
- Automated Docker image build validation

**Infrastructure**
- Terraform configuration for AWS infrastructure
- EC2 and security group definitions
- Configurable infrastructure variables and outputs

## Run Locally

### Build the container

```bash
docker build -t enterprise-ai-inference:latest -f docker/Dockerfile .
```

### Deploy to Kubernetes

```bash
kubectl apply -f kubernetes/deployment.yaml
kubectl apply -f kubernetes/service.yaml
```

Verify:

```bash
kubectl get pods
kubectl get services
```

Forward the service:

```bash
kubectl port-forward service/enterprise-ai-service 8000:8000
```

API documentation:

```text
http://localhost:8000/docs
```

## Testing

```bash
pytest -q
```

Current test suite covers:

- Service health
- Model inference
- Prediction response types
- Invalid API input
- Runtime metrics

## Performance

Benchmark:

```bash
python benchmarks/benchmark_api.py
```

Warm local Kubernetes benchmark:

```text
Requests: 20
Average latency: 0.0025 seconds
Fastest request: 0.0015 seconds
Slowest request: 0.0179 seconds
```

Results reflect the local development environment and are not representative of cloud production performance.

## Project Structure

```text
enterprise-ai-infrastructure/
├── .github/workflows/
│   └── ci.yml
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
├── requirements.txt
└── README.md
```

## Stack

Python · PyTorch · FastAPI · Docker · Kubernetes · MLflow · Pytest · GitHub Actions · Terraform · AWS

## Current Status

The training, inference, containerization, Kubernetes deployment, experiment tracking, monitoring endpoint, benchmarking, automated testing, and CI pipeline are implemented and tested locally.

Terraform AWS infrastructure configuration is included but has not yet been deployed to AWS.

### Next

- Validate Terraform configuration
- Publish Docker image to a container registry
- Add Prometheus/Grafana observability
- Extend CI toward automated deployment
