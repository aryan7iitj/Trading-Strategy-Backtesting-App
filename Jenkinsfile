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
                        bat 'docker login -u %DOCKER_USERNAME% -p %DOCKER_PASSWORD%'
                    }
                }
            }
        }
        stage('Push Docker Image') {
            steps {
                bat 'docker push aryaniitj7/trading-strategy-backtesting'    
            }
        }
    }

    post {
        always {
            echo 'Pipeline completed...'
        }
    }
}
