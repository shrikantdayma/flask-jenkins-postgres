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
                echo 'Checking out source code...'
                // The actual checkout happens here implicitly or explicitly.
                // Added a no-op step for clarity.
            }
        }
        
        stage('Build Docker Image') {
            steps {
                script {
                    // FIX: This command correctly handles the Dockerfile in the 'app' subdirectory.
                    // -f app/Dockerfile: specifies the Dockerfile's path (relative to repo root).
                    // app: sets the build context to the 'app' directory, which is needed for 'COPY' commands.
                    sh "docker build -t ${IMAGE_NAME}:${TAG_NAME} -f app/Dockerfile app"
                }
            }
        }

        stage('Run Tests') {
            steps {
                script {
                    // FIX: Added -e PYTHONPATH=. to resolve 'ModuleNotFoundError: No module named 'app'' 
                    // This allows Python to find 'app.py' and other modules in the current directory (/app).
                    // 'pytest tests' is used because 'tests' is at the root of the /app directory inside the container.
                    sh "docker run --rm -e POSTGRES_HOST=postgres-db -e POSTGRES_DB=app_db -e POSTGRES_USER=admin -e POSTGRES_PASSWORD=admin -e PYTHONPATH=. ${IMAGE_NAME}:${TAG_NAME} pytest tests"
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
