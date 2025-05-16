pipeline {
  agent any

  environment {
    ROUTING_YAML_FILE = 'routing_data.yaml'
  }

  stages {
    stage('Check Routing Expiry') {
      steps {
        sh '''
          python3 routing_expiry_checker.py \
            --action check_routing_expiry \
            --yaml ${ROUTING_YAML_FILE} \
            --days 15
        '''
      }
    }
  }

  post {
    success {
      echo "Routing check passed."
    }
    failure {
      echo "Routing check failed. Expiry detected."
    }
  }
}
