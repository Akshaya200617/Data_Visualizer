pipeline {
    agent any

    stages {

        stage('Checkout') {
            steps {
                git branch: 'main',
                credentialsId: 'Akshaya_Intern',
                url: 'https://github.com/Akshaya200617/Data_Visualizer.git'
            }
        }

        stage('Install Dependencies') {
            steps {
                sh "pip3 install -r requirements.txt"
            }
        }

        stage('Build Docker Image') {
            steps {
                sh 'docker build -t data-visualizer .'
            }
        }

        stage('Run Docker Container') {
            steps {
                sh 'docker run -d -p 2000:5000 data-visualizer'
            }
        }
    }
}
