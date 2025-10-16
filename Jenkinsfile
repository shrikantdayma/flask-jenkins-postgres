pipeline {

agent any



environment {

    // Docker Image & Tagging

    IMAGE_NAME = "flask-postgres-app"

    TAG_NAME = "${env.BUILD_NUMBER}"

    

    // Docker Networking & Container Names

    NETWORK_NAME = "my-network"

    DB_CONTAINER = "postgres-db"

    APP_CONTAINER = "flask-app"

    

    // Database Credentials

    POSTGRES_DB = "app_db"

    POSTGRES_USER = "admin"

    POSTGRES_PASSWORD = "admin"

}



stages {

    stage('Checkout') {

        steps {

            echo '📥 Checking out source code...'

            checkout scm

        }

    }



    stage('Build Docker Image') {

        steps {

            echo '🐳 Building Flask Docker image...'

            sh "docker build -t ${IMAGE_NAME}:${TAG_NAME} -f app/Dockerfile app"

        }

    }



    stage('Setup Environment') {

        steps {

            echo '🌐 Creating Docker network (if needed)...'

            // Create the custom network

            sh "docker network inspect ${NETWORK_NAME} >/dev/null 2>&1 || docker network create ${NETWORK_NAME}"



            echo '🗄️ Starting PostgreSQL container...'

            // IMPORTANT: Removed line continuation backslashes (\)

            sh '''

                docker rm -f ${DB_CONTAINER} || true

                docker run -d --name ${DB_CONTAINER} --network ${NETWORK_NAME} -e POSTGRES_DB=${POSTGRES_DB} -e POSTGRES_USER=${POSTGRES_USER} -e POSTGRES_PASSWORD=${POSTGRES_PASSWORD} -p 5432:5432 postgres:13

            '''

            echo '⏳ Waiting 10 seconds for PostgreSQL to initialize...'

            sleep 10

        }

    }



    stage('Run Tests') {

        steps {

            echo '🧪 Running unit tests...'

            // IMPORTANT: Removed line continuation backslashes (\)

            sh '''

                docker run --rm --network ${NETWORK_NAME} -e POSTGRES_HOST=${DB_CONTAINER} -e POSTGRES_DB=${POSTGRES_DB} -e POSTGRES_USER=${POSTGRES_USER} -e POSTGRES_PASSWORD=${POSTGRES_PASSWORD} -e PYTHONPATH=. ${IMAGE_NAME}:${TAG_NAME} pytest tests

            '''

        }

    }



    stage('Deploy Flask App') {

        steps {

            echo '🚀 Deploying Flask app container...'

            // IMPORTANT: Removed line continuation backslashes (\)

            sh '''

                docker rm -f ${APP_CONTAINER} || true

                docker run -d --name ${APP_CONTAINER} --network ${NETWORK_NAME} -e POSTGRES_HOST=${DB_CONTAINER} -e POSTGRES_DB=${POSTGRES_DB} -e POSTGRES_USER=${POSTGRES_USER} -e POSTGRES_PASSWORD=${POSTGRES_PASSWORD} -p 5000:5000 ${IMAGE_NAME}:${TAG_NAME}

            '''

            echo '✅ Flask app deployed! Access the app on port 5000.'

        }

    }

}



post {

    always {

        echo '🏁 Pipeline finished. Containers remain running for debugging or manual testing.'

    }

}

}
