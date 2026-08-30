# Enterprise AI Infrastructure Platform

A production-oriented AI infrastructure project for training, containerizing, deploying, and serving machine learning models using PyTorch, FastAPI, Docker, Kubernetes, MLflow, Terraform, and AWS.

## Overview

This project demonstrates an end-to-end machine learning infrastructure workflow, from model training to containerized inference and Kubernetes deployment.

The platform provides a foundation for scalable machine learning workloads while demonstrating infrastructure and MLOps concepts used in modern AI systems.

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
                /          \
         Deployment        Service
              |
             Pods
              |
              v
           Inference

        MLflow       Monitoring
           \           /
            \         /
          Infrastructure
                |
             Terraform
                |
               AWS
```

## Current Features

- PyTorch model training pipeline
- Model serialization and loading
- FastAPI inference service
- REST-based prediction endpoint
- Dockerized inference application
- Kubernetes Deployment
- Kubernetes Service networking
- Local Kubernetes model serving
- Interactive API testing through Swagger UI
- MLflow experiment tracking foundation

## Technology Stack

| Area | Technologies |
|---|---|
| Machine Learning | PyTorch |
| Programming | Python |
| API | FastAPI, Uvicorn |
| Containers | Docker |
| Orchestration | Kubernetes |
| Experiment Tracking | MLflow |
| Infrastructure as Code | Terraform |
| Cloud | AWS |

## API

### Health Check

`GET /`

Example response:

```json
{
  "status": "healthy",
  "service": "enterprise-ai-inference",
  "device": "cpu"
}
```

### Model Prediction

`POST /predict`

The prediction endpoint accepts model features through the REST API and returns a model prediction.

## Kubernetes Deployment

The inference service is packaged inside a Docker container and deployed to Kubernetes.

```bash
kubectl apply -f kubernetes/deployment.yaml
kubectl get deployments
kubectl get pods
```

A successfully deployed instance reports:

```text
READY   STATUS    RESTARTS
1/1     Running   0
```

The service can be accessed locally using:

```bash
kubectl port-forward service/enterprise-ai-service 8000:8000
```

FastAPI's interactive API documentation is then available at:

`http://localhost:8000/docs`

## Project Structure

```text
enterprise-ai-infrastructure/
├── docker/
│   └── Dockerfile
├── kubernetes/
│   └── deployment.yaml
├── models/
│   └── model.pth
├── src/
│   ├── inference/
│   │   └── app.py
│   └── training/
│       ├── __init__.py
│       ├── model.py
│       └── train.py
├── requirements.txt
└── README.md
```

## Development Roadmap

Planned infrastructure improvements include:

- Kubernetes health probes and resource management
- Monitoring and observability
- Terraform-based cloud infrastructure
- AWS deployment
- Automated testing
- CI/CD
- Model and infrastructure performance benchmarking
- Scalable model-serving architecture

## Project Goal

The goal of this project is to build an increasingly production-oriented AI infrastructure stack while developing hands-on experience across model training, containerization, orchestration, experiment tracking, infrastructure as code, cloud infrastructure, and ML observability.