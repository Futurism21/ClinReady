pipeline {
    agent any

    environment {
        PYTHON = "C://Users//shubhamm//AppData//Local//Programs//Python//Python312//python.exe"
    }

    stages {

        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Install Dependencies') {
            steps {
                bat '"%PYTHON%" -m pip install --upgrade pip'
                bat '"%PYTHON%" -m pip install -r requirements.txt'
            }
        }

        stage('Install Playwright Browsers') {
            steps {
                bat '"%PYTHON%" -m playwright install'
            }
        }

        stage('Run Tests') {
            steps {
                bat '"%PYTHON%" -m pytest --html=reports/report.html'
            }
        }

        stage('Archive Reports') {
            steps {
                archiveArtifacts artifacts: 'reports/**/*', fingerprint: true
            }
        }
    }
}