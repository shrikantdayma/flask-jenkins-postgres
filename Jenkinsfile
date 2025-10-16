pipeline {
    agent any

    environment {
        IMAGE_NAME = 'flask-postgres-app'
        DOCKER_TAG = 'latest'
        DOCKER_IMAGE = "${IMAGE_NAME}:${DOCKER_TAG}"
    }

    stages {

        stage('Checkout') {
            steps {
                // Explicit Git checkout to avoid branch issues
                checkout([
                    $class: 'GitSCM',
                    branches: [[name: '*/main']],
                    userRemoteConfigs: [[
                        url: 'https://github.com/shrikantdayma/flask-jenkins-postgres'
                    ]]
                ])
            }
        }

        stage('Build Docker Image') {
            steps {
                dir('app') {
                    script {
                        sh "docker build -t ${DOCKER_IMAGE} ."
                    }
                }
            }
        }

        stage('Run Tests') {
            steps {
                script {
                    sh """
                        docker run --rm \
                        -e POSTGRES_HOST=postgres-db \
                        -e POSTGRES_DB=app_db \
                        -e POSTGRES_USER=admin \
                        -e POSTGRES_PASSWORD=admin \
                        ${DOCKER_IMAGE} \
                        pytest tests/
                    """
                }
            }
        }

        stage('Deploy') {
            when {
                expression { currentBuild.result == null || currentBuild.result == 'SUCCESS' }
            }
            steps {
                echo "🚀 Deploying the application (this is a placeholder)."
                // Add actual deployment logic here (e.g., docker-compose, kubectl, SCP, etc.)
            }
        }
    }

    post {
        always {
            echo "🧹 Cleaning up..."
        }
        success {
            echo "✅ Build succeeded!"
        }
        failure {
            echo "❌ Pipeline failed."
        }
    }
}

