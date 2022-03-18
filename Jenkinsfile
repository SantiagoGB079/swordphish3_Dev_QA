@Library('jenkinslib@v1.1.7') _

final HELPER = new PipelineHelper()
final REPO_URL = 'https://github.com/AppGate-TFP/dms-swordphish3'

def CONFIG
def PROJECT
def IMAGE

String REGISTRY

pipeline {

    agent { label 'ms-docker' }
    options { skipDefaultCheckout true }

    environment {
        registry = "https://devops-tools.dtp.appgate.com:9443"
        registryCredential = 'dtp_prod'
        namespace = 'swordphish3'
        imageBuildName = "${namespace}/dtp-swordphish3:${env.BRANCH_NAME}-${env.BUILD_NUMBER}-release"
        credentialsIdDev = 'kubeconfigbeta'
        kubeConfigInAmi = "tempConfig.yaml"
    }

    stages {
        stage('Get from GIT') {
            steps {
                script {
                    HELPER.pullChanges('9c58deea-9a1f-43bd-8283-81de50db2e15', REPO_URL, 'dtp-swordphish3')
                }
            }
        }

        stage('Configure Registry & Variables') {
            steps {
                script {
                    CONFIG = HELPER.getConfig()
                    CONFIG.PROJECT_NAME = CONFIG.PROJECT_NAME.replace('dtp-', '')
                    PROJECT = "$CONFIG.PROJECT_NAME:$CONFIG.APP_VERSION".toString()
                    REGISTRY = "devops-tools.dtp.appgate.com:9443/dtp/$PROJECT"
                }
            }
        }

        stage('Unit Test') {
            steps {
                script {
                    echo 'ToDo: Enable unit tests!'
                }
            }
        }

        stage('Integration Test') {
            steps {
                script {
                    echo 'ToDo: Enable integration tests!'
                }
            }
        }

        stage('Build Artifact') {
            steps {
                script {
                    echo 'Python doesnt build!'
                }
            }
        }

        stage('Build & Push Docker Image') {
            steps {
                script {
                    def REGISTRY_URL = "http://$REGISTRY".toString()
                    IMAGE = REGISTRY.replace('/', '\\/')
                    docker.withRegistry(REGISTRY_URL, 'dtp_prod') {
                        sh "docker build -t $IMAGE -f Dockerfile ."
                        sh "docker tag $IMAGE $IMAGE"
                        sh "docker push $IMAGE"
                    }
                }
            }
        }
    }
}
