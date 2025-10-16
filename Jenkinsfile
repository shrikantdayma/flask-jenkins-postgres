pipeline {
    agent any
    
    // Set environment variables for Docker image and Test Runner
    environment {
        // Build image will be tagged with the build number
        IMAGE_NAME = "flask-postgres-app"
        TAG_NAME = "${env.BUILD_NUMBER}"
    }

    stages {
        stage('Declarative: Checkout SCM') {
            steps {
                // Initial checkout is done automatically by Declarative Pipeline
                // Adding a placeholder step for clarity
                echo 'Checking out source code...'
            }
        }
        
        stage('Build Docker Image') {
            steps {
                script {
                    // Fix: We run this from the repo root.
                    // -f app/Dockerfile: specifies the Dockerfile's location
                    // app: sets the build context to the 'app' directory, which is needed for 'COPY' commands inside the Dockerfile
                    sh "docker build -t ${IMAGE_NAME}:${TAG_NAME} -f app/Dockerfile app"
                }
            }
        }

        stage('Run Tests') {
            steps {
                script {
                    // Fix from previous errors: Test runner needs to use the correct directory.
                    // The Dockerfile WORKDIR is /app, and files were copied relative to the context (app/).
                    // Therefore, tests are at /app/tests inside the container.
                    sh "docker run --rm -e POSTGRES_HOST=postgres-db -e POSTGRES_DB=app_db -e POSTGRES_USER=admin -e POSTGRES_PASSWORD=admin ${IMAGE_NAME}:${TAG_NAME} pytest tests"
                }
            }
        }

        stage('Deploy') {
            steps {
                echo "Deployment logic goes here..."
            }
        }
    }
}
