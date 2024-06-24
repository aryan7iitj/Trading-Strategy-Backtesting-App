pipeline {
    agent {
        docker { image 'node:20.14.0-alpine3.20' }
    }
    stages {
        stage('Test') {
            steps {
                sh 'node --version'
            }
        }
    }
}
