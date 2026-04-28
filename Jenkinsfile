pipeline {
    agent any

    stages {
        stage('Clone Code') {
            steps {
                git 'https://github.com/Sushmakumara/devops-project2.git'
            }
        }

        stage('Build Docker Image') {
            steps {
                sh 'docker build -t my-devops-app .'
            }
        }

        stage('Run Container') {
            steps {
                sh 'docker run -d -p 5006:5000 my-devops-app'
            }
        }
    }
}
