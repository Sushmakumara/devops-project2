pipeline {
    agent any

    stages {

        stage('Build Docker Image') {
            steps {
                sh 'docker build -t my-devops-app .'
            }
        }

        stage('Run Container') {
            steps {
                sh 'docker stop my-container || true'
                sh 'docker rm my-container || true'
                sh 'docker run -d -p 5006:5000 --name my-container my-devops-app'
            }
        }

    }
}
