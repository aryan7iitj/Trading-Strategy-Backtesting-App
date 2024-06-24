pipeline {
    agent any

    environment {
        PATH = "C:\\Windows\\System32;C:\\Program Files\\Docker\\Docker\\resources\\bin;${env.PATH}"
    }

    stages {
        stage('Build Docker Image') {
            steps {
                bat 'docker build -t backtesting-app .'
            }
        }
    }
}
