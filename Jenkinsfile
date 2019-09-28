pipeline {
    agent {
        kubernetes {
            defaultContainer 'python3'
            yamlFile 'cicd/.kube.yml'
        }
    }
    environment {
        def build_data = readJSON file: 'cicd/publish.json'
        def poetry_source = readFile file: 'pyproject.toml'

        // pypi configuration
        TARGET_PYPI_REPOSITORY = "${build_data.pypi_repository}"

        // Docker configuration
        TARGET_DOCKER_IMAGE = "${build_data.docker_image}"
        TARGET_DOCKER_REPOSITORY = "${build_data.docker_repository}"
        TARGET_DOCKER_NAMESPACE = "${build_data.docker_namespace}"
        TARGET_DOCKER_DESTINATION = "$TARGET_DOCKER_REPOSITORY/$TARGET_DOCKER_NAMESPACE/$TARGET_DOCKER_IMAGE"
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
        stage('publish') {
            when {
                branch 'master'
            }
            steps {
                container("python3") {
                    withCredentials([usernamePassword(credentialsId: 'AutomationUser', passwordVariable: 'password', usernameVariable: 'username')]) {
                        sh "poetry config repositories.deployment $TARGET_PYPI_REPOSITORY"
                        sh "poetry publish --build --repository deployment --username $username --password $password"
                    }
                }
                container('kaniko') {
                    sh """
                       /kaniko/executor -f `pwd`/Dockerfile \
                       -c `pwd` \
                       --cache=true \
                       --destination=$TARGET_DOCKER_DESTINATION:\$(cat pyproject.toml | sed -n 's/^version = "\\([0-9].*\\.[0-9].*\\.[0-9].*\\)"\$/\\1/p')
                    """
                }
            }
            post {
                success {
                    build job: '../foundry_config/master', wait: false
                    discordSend description: "foundry/backend succeeded in master", footer: '', image: '', link: env.BUILD_URL, result: '', thumbnail: '', title: 'Foundry Backend Build Success', webhookURL: 'https://discordapp.com/api/webhooks/625518286313881627/C915tCpq2uscwoX_LIpiR0q3_pVRACG5_FDwUB0HqArqYKmCjwCxyUg3uSef14AfF9Rp'
                }
                failure {
                    discordSend description: "foundry/backend failed in master", footer: '', image: '', link: env.BUILD_URL, result: '', thumbnail: '', title: 'Foundry Backend Build Failed', webhookURL: 'https://discordapp.com/api/webhooks/625518286313881627/C915tCpq2uscwoX_LIpiR0q3_pVRACG5_FDwUB0HqArqYKmCjwCxyUg3uSef14AfF9Rp'
                }
            }
        }
    }
}
