pipeline {
    agent any

    environment {
        DOCKER_IMAGE = 'backtesting-app:latest'
    }

    stages {
        stage('Checkout') {
            steps {
                // Checkout code from the version control system
                checkout scm
            }
        }

        stage('Build Docker Image') {
            steps {
                script {
                    // Build the Docker image
                    docker.build(DOCKER_IMAGE)
                }
            }
        }
      
    }

    post {
        always {
            // Clean up any resources
            cleanWs()
        }
    }
}
