pipeline {
    agent any

    environment {
        POSTGRES_HOST = "postgres-db"
        POSTGRES_DB   = "app_db"
        POSTGRES_USER = "admin"
        POSTGRES_PASSWORD = "admin"
        DOCKER_IMAGE = "flask-postgres-app"
        FLASK_CONTAINER = "flask-app"
    }

    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Build Docker Image') {
            steps {
                script {
                    docker.build(env.DOCKER_IMAGE)
                }
            }
        }

        stage('Run Tests') {
            steps {
                // Use a Docker container to run tests, mounting code
                sh '''
                    docker run --rm \
                        -e POSTGRES_HOST=${POSTGRES_HOST} \
                        -e POSTGRES_DB=${POSTGRES_DB} \
                        -e POSTGRES_USER=${POSTGRES_USER} \
                        -e POSTGRES_PASSWORD=${POSTGRES_PASSWORD} \
                        ${DOCKER_IMAGE} pytest app/tests
                '''
            }
        }

        stage('Deploy') {
            steps {
                script {
                    // Stop existing container if running
                    sh "docker rm -f ${FLASK_CONTAINER} || true"
                    // Run app container
                    sh """
                        docker run -d \
                          --network app-network \
                          --name ${FLASK_CONTAINER} \
                          -e POSTGRES_HOST=${POSTGRES_HOST} \
                          -e POSTGRES_DB=${POSTGRES_DB} \
                          -e POSTGRES_USER=${POSTGRES_USER} \
                          -e POSTGRES_PASSWORD=${POSTGRES_PASSWORD} \
                          -p 5000:5000 \
                          ${DOCKER_IMAGE}
                    """
                }
            }
        }
    }

    post {
        success {
            echo "Pipeline succeeded!"
        }
        failure {
            echo "Pipeline failed!"
        }
    }
}
post {
    success {
        slackSend(
            color: "good",
            message: "✅ Pipeline *${env.JOB_NAME}* #${env.BUILD_NUMBER} succeeded: ${env.BUILD_URL}",
            webhookUrl: "${SLACK_WEBHOOK_URL}"
        )
    }
    failure {
        slackSend(
            color: "danger",
            message: "❌ Pipeline *${env.JOB_NAME}* #${env.BUILD_NUMBER} failed: ${env.BUILD_URL}",
            webhookUrl: "${SLACK_WEBHOOK_URL}"
        )
    }
}

