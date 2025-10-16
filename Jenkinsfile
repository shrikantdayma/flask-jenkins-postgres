pipeline {
    agent any
    
    // Set environment variables for Docker image and Test Runner
    environment {
        // Build image will be tagged with the build number
        IMAGE_NAME = "flask-postgres-app"
        TAG_NAME = "${env.BUILD_NUMBER}"
        // CRITICAL: Set the Docker network name. 
        // Based on your previous 'docker ps' output, 'bridge' is the most common default
        // if you didn't create a custom one. Adjust if necessary (e.g., 'myproject_default').
        NETWORK_NAME = "bridge" 
    }

    stages {
        stage('Declarative: Checkout SCM') {
            steps {
                echo 'Checking out source code...'
            }
        }
        
        stage('Build Docker Image') {
            steps {
                script {
                    // Correctly specifies Dockerfile path and build context
                    sh "docker build -t ${IMAGE_NAME}:${TAG_NAME} -f app/Dockerfile app"
                }
            }
        }

        stage('Run Tests') {
            steps {
                script {
                    // Added -e PYTHONPATH=. to resolve Python import errors
                    sh "docker run --rm -e POSTGRES_HOST=postgres-db -e POSTGRES_DB=app_db -e POSTGRES_USER=admin -e POSTGRES_PASSWORD=admin -e PYTHONPATH=. ${IMAGE_NAME}:${TAG_NAME} pytest tests"
                }
            }
        }

        stage('Deploy') {
            steps {
                script {
                    echo "Stopping and removing existing application container 'flask-app'..."
                    // Stop and remove the previous container instance (|| true allows the step to pass if the container doesn't exist)
                    sh "docker stop flask-app || true" 
                    sh "docker rm flask-app || true"
                    
                    echo "Starting the new application container..."
                    // Launch the container in detached mode (-d), map the port (-p),
                    // and connect to the database network (--network)
                    sh "docker run -d --name flask-app -p 5000:5000 --network ${NETWORK_NAME} -e POSTGRES_HOST=postgres-db -e POSTGRES_DB=app_db -e POSTGRES_USER=admin -e POSTGRES_PASSWORD=admin ${IMAGE_NAME}:${TAG_NAME}"
                    
                    echo "Deployment complete! Check http://192.168.0.14:5000/"
                }
            }
        }
    }
}
