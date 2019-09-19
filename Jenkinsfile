pipeline {
    agent {
        kubernetes {
            defaultContainer 'python3'
            yamlFile 'cicd/.kube.yml'
        }
    }
    stages {
        stage('test') {
            steps {
                sh 'poetry install'
                sh """
                    poetry run pytest --cov foundry_backend \
                                      --cov-report term-missing \
                                      --cov-report xml \
                                      --cov-config cicd/.coveragerc \
                                      --junitxml=junit.xml
                """
            }
            post {
                always {
                    junit '**/junit.xml'
                    step([$class: 'CoberturaPublisher', autoUpdateHealth: false, autoUpdateStability: false, coberturaReportFile: '**/coverage.xml', failUnhealthy: false, failUnstable: false, maxNumberOfBuilds: 0, onlyStable: false, sourceEncoding: 'ASCII', zoomCoverageChart: false])
                }
            }
        }
        stage('build') {
            steps {
                sh 'poetry install'
                sh 'poetry build'
            }
        }
        stage('publish') {
            environment {
                def build_data = readJSON file: 'cicd/publish.json'
                TARGET_REPOSITORY = "${build_data.repository}"
            }
            when {
                branch 'master'
            }
            steps {
                withCredentials([usernamePassword(credentialsId: 'AutomationUser', passwordVariable: 'password', usernameVariable: 'username')]) {
                    sh "poetry config repositories.deployment $TARGET_REPOSITORY"
                    sh "poetry publish --repository deployment --username $username --password $password"
                }
            }
        }
    }
}
