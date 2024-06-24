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
        stage('Login') {
            steps {
                script {
                    withCredentials([usernamePassword(credentialsId: '8b0f8fb2-bd38-4b3b-b667-d095bf5e3cc8', usernameVariable: 'DOCKER_USERNAME', passwordVariable: 'DOCKER_PASSWORD')]) {
                        bat 'echo %DOCKER_PASSWORD% | docker login -u %DOCKER_USERNAME% --password-stdin'
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
