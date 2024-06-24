pipeline {
    agent any

    environment {
        PATH = "C:\\Windows\\System32;C:\\Program Files\\Docker\\Docker\\resources\\bin;C:\\Program Files\\Git\\cmd;${env.PATH}"
    }

    stages {
        stage('Build Docker Image') {
            steps {
                bat 'docker build -t aryaniitj7/trading-strategy-backtesting .'
            }
        }
        stage('Login') {
            steps {
                bat 'docker login'
            }
        }
        stage('Push Docker Image') {
            steps {
                bat 'docker push aryaniitj7/trading-strategy-backtesting'
            }
        }
    }
}
