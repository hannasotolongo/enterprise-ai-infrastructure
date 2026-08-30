# Enterprise AI Infrastructure Platform

AI infrastructure and MLOps project for training, tracking, containerizing, testing, deploying, monitoring, and benchmarking machine learning inference workloads.

The platform demonstrates how a machine learning model can move from local model development to a containerized API running on Kubernetes with automated testing and infrastructure-as-code configuration.

## Architecture

```text
                         Client
                           |
                           v
                    FastAPI REST API
                     POST /predict
                           |
                           v
                     PyTorch Model
                           |
                           v
                    Docker Container
                           |
                           v
                       Kubernetes
                    /             \
             Deployment           Service
                 |                   |
          Health Probes          Networking
          Resource Limits
                 |
                 v
              Inference
                 |
          -----------------
          |               |
       Metrics        Benchmarking
          |
       /metrics

Training Pipeline
       |
       v
    PyTorch
       |
       v
     MLflow
   /        \
Metrics    Model Artifact


Infrastructure Configuration
       |
       v
    Terraform
       |
       v
       AWS

Development Workflow
       |
       v
      GitHub
       |
       v
 GitHub Actions CI
       |
       v
 Automated Testing
```

## Features

### Machine Learning

- PyTorch model training pipeline
- Apple Metal Performance Shaders (MPS) acceleration when available
- Model serialization and loading
- Reproducible inference workflow

### Experiment Tracking

MLflow is integrated into the training pipeline to track:

- Training parameters
- Loss across epochs
- Training duration
- Compute device
- Model artifacts

Trained model files are automatically stored as MLflow artifacts after training.

### Model Serving

The trained PyTorch model is exposed through a FastAPI inference service.

Available endpoints:

`GET /`

Health endpoint for verifying service availability.

`POST /predict`

Accepts model features and returns an inference result.

`GET /metrics`

Provides runtime inference metrics including:

- Prediction requests
- Successful predictions
- Average prediction latency
- Compute device

### Containerization

The inference application is packaged into a Docker container to provide a consistent runtime environment.

Build the image with:

```bash
docker build -t enterprise-ai-inference:latest -f docker/Dockerfile .
```

### Kubernetes Orchestration

The inference container can be deployed to a local Kubernetes cluster.

The Kubernetes configuration includes:

- Deployment management
- Service networking
- Readiness probes
- Liveness probes
- CPU resource requests and limits
- Memory resource requests and limits

Deploy the application:

```bash
kubectl apply -f kubernetes/deployment.yaml
kubectl apply -f kubernetes/service.yaml
```

Verify the deployment:

```bash
kubectl get deployments
kubectl get pods
kubectl get services
```

Access the service locally:

```bash
kubectl port-forward service/enterprise-ai-service 8000:8000
```

FastAPI interactive documentation is available at:

`http://localhost:8000/docs`

## Automated Testing

The repository contains automated API tests for health checking and model prediction.

Run the test suite with:

```bash
pytest -q
```

Current local test suite:

```text
2 passed
```

## Continuous Integration

GitHub Actions automatically runs the test suite for pushes and pull requests to the `main` branch.

The CI workflow:

1. Checks out the repository
2. Configures Python
3. Installs project dependencies
4. Runs the automated test suite

This provides automated validation of application changes before further deployment.

## Performance Benchmarking

The project includes an inference benchmarking utility:

```bash
python benchmarks/benchmark_api.py
```

A warm local benchmark against the Kubernetes-hosted inference API produced:

```text
Requests: 20
Average latency: 0.0025 seconds
Fastest request: 0.0015 seconds
Slowest request: 0.0179 seconds
```

These measurements represent a local development environment and should not be interpreted as cloud or production performance.

An earlier cold/warm-up run showed higher initial latency, demonstrating the performance difference that can occur during model or service initialization.

## Infrastructure as Code

Terraform configuration is included as the foundation for AWS infrastructure provisioning.

The current Terraform configuration defines:

- AWS provider configuration
- EC2 compute infrastructure
- Security group configuration
- Infrastructure variables
- Infrastructure outputs

The Terraform configuration is currently an infrastructure prototype and has not yet been applied as a production AWS deployment.

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
│       ├── __init__.py
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

## Technology Stack

| Area | Technologies |
|---|---|
| Programming | Python |
| Machine Learning | PyTorch |
| API / Model Serving | FastAPI, Uvicorn |
| Containers | Docker |
| Orchestration | Kubernetes |
| Experiment Tracking | MLflow |
| Testing | Pytest |
| Continuous Integration | GitHub Actions |
| Infrastructure as Code | Terraform |
| Cloud Infrastructure | AWS configuration |
| Version Control | Git, GitHub |

## Engineering Concepts Demonstrated

This project demonstrates experience with:

- Machine learning model lifecycle management
- Model serving through REST APIs
- Containerized application deployment
- Kubernetes workload orchestration
- Health checking and resource management
- Experiment and artifact tracking
- ML inference observability
- Automated software testing
- Continuous integration
- Infrastructure as code
- Performance benchmarking

## Future Improvements

Potential extensions include:

- Deploying the infrastructure to AWS
- Publishing container images to a remote registry
- Prometheus and Grafana observability
- Persistent centralized metrics
- Kubernetes autoscaling
- Load and concurrency testing
- Model versioning and deployment strategies
- Infrastructure security hardening
- Automated cloud deployment

## Project Goal

The goal of this project is to demonstrate the infrastructure lifecycle surrounding a machine learning model—not only model development, but also the systems required to package, serve, test, orchestrate, observe, benchmark, and eventually deploy machine learning workloads in scalable environments.
