pipeline {
  agent any
  stages {
    stage('Build ') {
      steps {
        echo '*****CREANDO IMAGEN***'
        sh 'sh ./run_build_script.sh'
        echo 'RUN CONTAINERS'
      }
    }

    stage('Integration-test') {
      steps {
        sh 'sh ./run_linux_tests.sh'
      }
    }

    stage('Deploy staging') {
      steps {
        echo 'downloading containers'
        sh 'docker-compose -f ./swordphish_test/docker-compose.yml down'
        sh 'docker ps'
        echo '****CONTAINERS DOWN****'
      }
    }

  }
}