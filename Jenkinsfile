pipeline {
    agent any

    environment {
        IMAGE_NAME = "flask-postgres-app"
        TAG_NAME = "${env.BUILD_NUMBER}"
        NETWORK_NAME = "my-network"
        DB_CONTAINER = "postgres-db"
        APP_CONTAINER = "flask-app"
        POSTGRES_DB = "app_db"
        POSTGRES_USER = "admin"
        POSTGRES_PASSWORD = "admin"
    }

    stages {
        stage('Checkout') {
            steps {
                echo 'Checking out source code...'
                checkout scm
            }
        }

        stage('Build Docker Image') {
            steps {
                echo "Building Flask Docker image..."
                sh "docker build -t ${IMAGE_NAME}:${TAG_NAME} -f app/Dockerfile app"
            }
        }

        stage('Create Network') {
            steps {
                echo "Creating Docker network if it doesn't exist..."
                sh "docker network inspect ${NETWORK_NAME} >/dev/null 2>&1 || docker network create ${NETWORK_NAME}"
            }
        }

        stage('Start PostgreSQL') {
            steps {
                echo "Starting PostgreSQL container..."
                sh '''
                    docker rm -f ${DB_CONTAINER} || true
                    docker run -d \
                        --name ${DB_CONTAINER} \
                        --network ${NETWORK_NAME} \
                        -e POSTGRES_DB=${POSTGRES_DB} \
                        -e POSTGRES_USER=${POSTGRES_USER} \
                        -e POSTGRES_PASSWORD=${POSTGRES_PASSWORD} \
                        -p 5432:5432 \
                        postgres:13
                '''
            }
        }

        stage('Run Tests') {
            steps {
                echo "Running unit tests inside Flask container..."
                sh '''
                    docker run --rm \
                        --network ${NETWORK_NAME} \
                        -e POSTGRES_HOST=${DB_CONTAINER} \
                        -e POSTGRES_DB=${POSTGRES_DB} \
                        -e POSTGRES_USER=${POSTGRES_USER} \
                        -e POSTGRES_PASSWORD=${POSTGRES_PASSWORD} \
                        -e PYTHONPATH=. \
                        ${IMAGE_NAME}:${TAG_NAME} \
                        pytest tests
                '''
            }
        }

        stage('Deploy Flask App') {
            steps {
                echo "Deploying Flask app container..."
                sh '''
                    docker rm -f ${APP_CONTAINER} || true
                    docker run -d \
                        --name ${APP_CONTAINER} \
                        --network ${NETWORK_NAME} \
                        -e POSTGRES_HOST=${DB_CONTAINER} \
                        -e POSTGRES_DB=${POSTGRES_DB} \
                        -e POSTGRES_USER=${POSTGRES_USER} \
                        -e POSTGRES_PASSWORD=${POSTGRES_PASSWORD} \
                        -p 5000:5000 \
                        ${IMAGE_NAME}:${TAG_NAME}
                '''
                echo "✅ Flask app deployed. Try accessing: http://<YOUR_PWD_EXTERNAL_IP>:5000"
            }
        }
    }

    post {
        always {
            echo 'Cleaning up dangling containers (if any failed mid-pipeline)...'
            // Optionally clean up containers
            // sh "docker rm -f ${APP_CONTAINER} ${DB_CONTAINER} || true"
        }
    }
}

