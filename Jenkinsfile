pipeline {
    agent {
        docker {
            image 'node:20.14.0'
        }
    }
    stages {
        stage('Test') {
            steps {
                bat 'node --version'
            }
        }
    }
}
