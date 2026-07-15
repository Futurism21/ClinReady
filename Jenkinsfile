pipeline {
    agent any

    stages {

        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Install Dependencies') {
            steps {
                bat '"C://Users//shubhamm//AppData//Local//Programs//Python//Python312//python.exe" -m pip install --upgrade pip'
                bat '"C://Users//shubhamm//AppData//Local//Programs//Python//Python312//python.exe" -m pip install -r requirements.txt'
                bat '"C://Users//shubhamm//AppData//Local//Programs//Python//Python312//Scripts//playwright.exe" install'
                bat '"C://Users//shubhamm//AppData//Local//Programs//Python//Python312//Scripts//pytest.exe"'

            }
        }

        stage('Install Playwright Browsers') {
            steps {
                bat 'playwright install'
            }
        }

        stage('Run Tests') {
            steps {
                bat 'pytest --html=reports/report.html'
            }
        }

        stage('Archive Reports') {
            steps {
                archiveArtifacts artifacts: 'reports/**', fingerprint: true
            }
        }
    }
}