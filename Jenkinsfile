pipeline {
    agent any

    stages {

        stage('Checkout') {
            steps {
                git branch: 'main',
                credentialsId: 'HariniGitID',
                url: 'https://github.com/Akshaya200617/Simple-Data-Visualizer.git'
            }
        }

        stage('Install Dependencies') {
            steps {
                bat 'py -m pip install -r requirements.txt'
            }
        }

        stage('Build Docker Image') {
            steps {
                bat 'docker build -t data-visualizer .'
            }
        }

        stage('Run Docker Container') {
            steps {
                bat 'docker run -d -p 2000:5000 data-visualizer'
            }
        }
    }
}
