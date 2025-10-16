pipeline {
    agent any

    environment {
        IMAGE_NAME = "flask-postgres-app"
        CONTAINER_NAME = "flask-postgres-app"
        POSTGRES_CONTAINER = "postgres-db"
        POSTGRES_DB = "app_db"
        POSTGRES_USER = "admin"
        POSTGRES_PASSWORD = "admin"
    }

    stages {

        stage('Checkout') {
            steps {
                git branch: 'main', url: 'https://github.com/shrikantdayma/flask-jenkins-postgres'
            }
        }

        stage('Build Docker Image') {
            steps {
                dir('app') {
                    sh "docker build -t $IMAGE_NAME:latest ."
                }
            }
        }

        stage('Run Postgres') {
            steps {
                // Run Postgres container in background
                sh '''
                    docker run -d \
                        --name $POSTGRES_CONTAINER \
                        -e POSTGRES_DB=$POSTGRES_DB \
                        -e POSTGRES_USER=$POSTGRES_USER \
                        -e POSTGRES_PASSWORD=$POSTGRES_PASSWORD \
                        -p 5432:5432 \
                        postgres:13
                '''
            }
        }

        stage('Run Flask App') {
            steps {
                sh '''
                    docker run -d \
                        --name $CONTAINER_NAME \
                        --link $POSTGRES_CONTAINER:postgres-db \
                        -e POSTGRES_HOST=postgres-db \
                        -e POSTGRES_DB=$POSTGRES_DB \
                        -e POSTGRES_USER=$POSTGRES_USER \
                        -e POSTGRES_PASSWORD=$POSTGRES_PASSWORD \
                        -p 5000:5000 \
                        $IMAGE_NAME:latest
                '''
            }
        }

        stage('Run Tests') {
            steps {
                sh "docker exec $CONTAINER_NAME pytest"
            }
        }
    }

    post {
        always {
            echo '🧹 Cleaning up containers...'
            sh '''
                docker rm -f $CONTAINER_NAME || true
                docker rm -f $POSTGRES_CONTAINER || true
            '''
        }
    }
}

