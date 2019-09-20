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
//         TARGET_DOCKER_VERSION = "${poetry_source =~ /^version ?= ?\"(\d.\d.\d)\"$/}"
        TARGET_DOCKER_VERSION = "0.1.0"
        TARGET_DOCKER_IMAGE = "${build_data.image}"
        TARGET_DOCKER_REPOSITORY = "${build_data.docker_repository}"
        TARGET_DOCKER_NAMESPACE = "${build_data.docker_namespace}"
        TARGET_DOCKER_DESTINATION = "$TARGET_DOCKER_REPOSITORY/$TARGET_DOCKER_NAMESPACE/$TARGET_DOCKER_IMAGE:$TARGET_DOCKER_VERSION"
    }
    stages {
//         stage('test') {
//             steps {
//                 sh 'poetry install'
//                 sh """
//                     poetry run pytest --cov foundry_backend \
//                                       --cov-report term-missing \
//                                       --cov-report xml \
//                                       --cov-config cicd/.coveragerc \
//                                       --junitxml=junit.xml
//                 """
//             }
//             post {
//                 always {
//                     junit '**/junit.xml'
//                     step([$class: 'CoberturaPublisher', autoUpdateHealth: false, autoUpdateStability: false, coberturaReportFile: '**/coverage.xml', failUnhealthy: false, failUnstable: false, maxNumberOfBuilds: 0, onlyStable: false, sourceEncoding: 'ASCII', zoomCoverageChart: false])
//                 }
//             }
//         }
//         stage('build') {
//             steps {
//                 container('python3') {
//                     sh 'poetry install'
//                     sh 'poetry build'
//                 }
//             }
//         }
        stage('publish') {
            when {
                branch 'master'
            }
            steps {
//                 container("python3") {
//                     withCredentials([usernamePassword(credentialsId: 'AutomationUser', passwordVariable: 'password', usernameVariable: 'username')]) {
//                         sh "poetry config repositories.deployment $TARGET_PYPI_REPOSITORY"
//                         sh "poetry publish --repository deployment --username $username --password $password"
//                     }
//                 }
                container('kaniko') {
                    sh """
                       /kaniko/executor -f `pwd`/Dockerfile \
                       -c `pwd` \
                       --cache=false \
                       --destination=$TARGET_DOCKER_DESTINATION \
                    """
                }
            }
        }
    }
}
