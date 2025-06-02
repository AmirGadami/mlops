pipeline {
    agent {
        docker {
            image 'python:3.9-slim'  // Use a Docker image with Python pre-installed
            args '-v /var/run/docker.sock:/var/run/docker.sock'  // Mount Docker socket
        }
    }

    environment {
        VENV_DIR = 'venv'
        GCP_PROJECT = 'hip-watch-461221-r5'
        GCLOUD_PATH = "/var/jenkins_home/google-cloud-sdk/bin"
        KUBECTL_AUTH_PLUGIN = "/usr/lib/google-cloud-sdk/bin"
        DOCKER_BUILDKIT = "1"  // Enable Docker BuildKit for better builds
    }

    stages {
        stage("Cloning from Github") {
            steps {
                script {
                    echo 'Cloning from Github...'
                    checkout scmGit(
                        branches: [[name: '*/main']], 
                        extensions: [], 
                        userRemoteConfigs: [
                            [credentialsId: 'GitHub-token', 
                             url: 'https://github.com/AmirGadami/mlops.git']
                        ]
                    )
                }
            }
        }

        stage("Setup Environment") {
            steps {
                script {
                    echo 'Setting up environment...'
                    sh '''
                    apt-get update && apt-get install -y python3-venv docker.io
                    python -m venv ${VENV_DIR}
                    . ${VENV_DIR}/bin/activate
                    pip install --upgrade pip
                    pip install -e .
                    pip install dvc
                    '''
                }
            }
        }

        stage('DVC Pull') {
            steps {
                withCredentials([file(credentialsId: 'gcp-key', variable: 'GOOGLE_APPLICATION_CREDENTIALS')]) {
                    script {
                        echo 'DVC Pull...'
                        sh '''
                        . ${VENV_DIR}/bin/activate
                        dvc pull
                        '''
                    }
                }
            }
        }

        stage('Build and Push Image to GCR') {
            steps {
                withCredentials([file(credentialsId: 'gcp-key', variable: 'GOOGLE_APPLICATION_CREDENTIALS')]) {
                    script {
                        echo 'Build and Push Image to GCR'
                        sh '''
                        # Install gcloud CLI if not present
                        if ! command -v gcloud &> /dev/null; then
                            echo "Installing gcloud SDK..."
                            curl -sSL https://sdk.cloud.google.com | bash
                            source ~/.bashrc
                        fi

                        export PATH=$PATH:${GCLOUD_PATH}
                        gcloud auth activate-service-account --key-file=${GOOGLE_APPLICATION_CREDENTIALS}
                        gcloud config set project ${GCP_PROJECT}
                        gcloud auth configure-docker --quiet

                        # Build with Docker
                        docker build -t gcr.io/${GCP_PROJECT}/ml-project:latest .
                        
                        # Push to GCR
                        docker push gcr.io/${GCP_PROJECT}/ml-project:latest
                        '''
                    }
                }
            }
        }

        stage('Deploying to Kubernetes') {
            steps {
                withCredentials([file(credentialsId: 'gcp-key', variable: 'GOOGLE_APPLICATION_CREDENTIALS')]) {
                    script {
                        echo 'Deploying to Kubernetes'
                        sh '''
                        export PATH=$PATH:${GCLOUD_PATH}:${KUBECTL_AUTH_PLUGIN}
                        gcloud auth activate-service-account --key-file=${GOOGLE_APPLICATION_CREDENTIALS}
                        gcloud config set project ${GCP_PROJECT}
                        
                        # Install kubectl if not present
                        if ! command -v kubectl &> /dev/null; then
                            gcloud components install kubectl
                        fi
                        
                        gcloud container clusters get-credentials mlapps-cluster --region us-central1
                        kubectl apply -f deployment.yaml
                        '''
                    }
                }
            }
        }
    }

    post {
        always {
            cleanWs()  // Clean workspace after build
        }
    }
}