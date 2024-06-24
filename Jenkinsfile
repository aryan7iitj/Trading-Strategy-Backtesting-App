pipeline {
    agent any

    environment {
        PATH = "C:\\Windows\\System32;${env.PATH}"
    }

    stages {
        stage('Test') {
            steps {
                bat 'node --version'
            }
        }
    }
}
