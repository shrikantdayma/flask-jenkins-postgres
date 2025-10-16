pipeline {
    agent any

    environment {
        IMAGE_NAME = "flask-postgres-app"
    }

    stages {
        stage('Checkout') {
            steps {
                git 'https://github.com/shrikantdayma/flask-jenkins-postgres'
            }
        }

        stage('Build Docker Image') {
            steps {
                script {
                    sh "docker build -t ${IMAGE_NAME} ."
                }
            }
        }

        stage('Run Tests') {
            steps {
                script {
                    sh '''
                        docker run --rm \
                            -e POSTGRES_HOST=localhost \
                            -e POSTGRES_DB=app_db \
                            -e POSTGRES_USER=admin \
                            -e POSTGRES_PASSWORD=admin \
                            ${IMAGE_NAME} \
                            pytest tests
                    '''
                }
            }
        }

        // Optional: Push Docker image to Docker Hub
        /*
        stage('Push Image') {
            steps {
                withCredentials([usernamePassword(credentialsId: 'dockerhub-creds', usernameVariable: 'DOCKER_USER', passwordVariable: 'DOCKER_PASS')]) {
                    sh """
                        echo $DOCKER_PASS | docker login -u $DOCKER_USER --password-stdin
                        docker tag ${IMAGE_NAME} your-dockerhub-username/${IMAGE_NAME}
                        docker push your-dockerhub-username/${IMAGE_NAME}
                    """
                }
            }
        }
        */

        stage('Deploy') {
            steps {
                echo 'Deploy stage (add your script here)'
            }
        }
    }

    post {
        success {
            echo '✅ Pipeline succeeded!'
        }
        failure {
            echo '❌ Pipeline failed.'
        }
    }
}

