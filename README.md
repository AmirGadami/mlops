# AniRecNet: Anime Recommendation System with MLOps Integration

AniRecNet is a deep learning-based recommendation system that predicts personalized anime preferences using collaborative filtering. The project is built with TensorFlow and follows MLOps principles for reproducibility, modularity, and deployment readiness. It includes a Flask-based API for serving predictions and uses Kubernetes for orchestration in learning environments.

## Features

- Deep learning-based collaborative filtering using TensorFlow and Keras
- Flask API for serving recommendations
- MLOps practices: DVC for versioning, Docker for containerization, Jenkins for optional CI/CD
- Kubernetes deployment configuration (for learning and testing)
- Training with learning rate scheduling, early stopping, and checkpointing

## Tools Used

- **TensorFlow/Keras**: Model architecture and training
- **Pandas/NumPy**: Data processing
- **Matplotlib**: Visualization
- **Flask**: Serving the trained model
- **DVC**: Data and model artifact versioning
- **Docker**: Containerization
- **Jenkins** *(optional)*: CI/CD integration
- **Kubernetes**: Deployment and orchestration (learning purpose)

## Installation

```bash
git clone https://github.com/yourusername/anirecnet.git
cd anirecnet
pip install -r requirements.txt
```

To set up DVC (optional but recommended):

```bash
dvc pull
```

## Running the Flask App Locally

```bash
python application.py
```

This will start a local Flask server for model inference.

## Running with Docker (Without Jenkins or GCP)

First, build the Docker image:

```bash
docker build -t anirecnet .
```

Then, run the container:

```bash
docker run -p 8080:8080 anirecnet
```

- `-p 8080:8080` maps the container port to your local machine
- You can then access the Flask app at `http://localhost:8080`

## Optional: Run with Kubernetes

If you want to deploy the project using Kubernetes (for learning purposes):

1. Make sure Docker image is pushed to a container registry (e.g., Docker Hub or GCR)
2. Apply the deployment configuration:

```bash
kubectl apply -f deployment.yaml
```

This will start a Pod running your Flask app inside a Kubernetes cluster.

## Datasets

- `animelist.csv`: User-anime interactions
- `anime.csv`: Anime metadata

Place these in: `artifacts/raw/`

## Contact

Developed by Amir Ghadami  
Email: ah.ghadami75@gmail.com  
GitHub: https://github.com/amirgadami  
LinkedIn: https://www.linkedin.com/in/amirhosseinghadami/