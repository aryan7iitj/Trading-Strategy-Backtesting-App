pipeline {
    agent any

    environment {
        PATH = "C:\\Windows\\System32;C:\\Program Files\\Docker\\Docker\\resources\\bin;C:\\Program Files\\Git\\cmd;${env.PATH}"
    }

    stages {
        stage('Build Docker Image') {
            steps {
                catchError(buildResult: 'SUCCESS', stageResult: 'FAILURE') {
                    bat 'docker build -t aryaniitj7/trading-strategy-backtesting .'
                }
            }
        }
        stage('Login to Docker Hub') {
            steps {
                script {
                    withCredentials([usernamePassword(credentialsId: 'Docker_Login', usernameVariable: 'DOCKER_USERNAME', passwordVariable: 'DOCKER_PASSWORD')]) {
                        // Debugging lines to ensure credentials are loaded
                        bat 'echo DOCKER_USERNAME=%DOCKER_USERNAME%'
                        bat 'echo DOCKER_PASSWORD=%DOCKER_PASSWORD'
                        
                        // Attempt login
                        bat 'echo %DOCKER_PASSWORD% | docker login -u %DOCKER_USERNAME% --password-stdin'
                        
                        // Check login status
                        bat 'docker info'
                    }
                }
            }
        }
        stage('Push Docker Image') {
            steps {
                catchError(buildResult: 'SUCCESS', stageResult: 'FAILURE') {
                    bat 'docker push aryaniitj7/trading-strategy-backtesting'
                }
            }
        }
    }

    post {
        always {
            echo 'Pipeline completed'
        }
    }
}
