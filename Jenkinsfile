pipeline {
  agent any
  stages {
    stage('Build ') {
      steps {
        echo '*****CREANDO IMAGEN***'
        sh 'sh ./functional-test/swordphish_test/run_build_script.sh'
        echo 'RUN CONTAINERS'
      }
    }

    stage('Integration-test') {
      steps {
        sh 'sh ./functional-test/swordphish_test/run_linux_tests.sh'
      }
    }

    stage('Deploy staging') {
      steps {
        echo 'downloading containers'
        sh 'docker-compose -f ./functional-test/swordphish_test/docker-compose.yml down'
        sh 'docker ps'
        echo '****CONTAINERS DOWN****'
      }
    }

  }
    post {
    always {
      archiveArtifacts(artifacts: '**/functional-test/swordphish_test/target/s*.jar', fingerprint: true)
    }

    failure {
      mail(to: 'santiago.gomez@appgate.com', subject: "Failed Pipeline ${currentBuild.fullDisplayName}", body: " For details about the failure, see ${env.BUILD_URL}")
    }

  }
}