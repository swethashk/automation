pipeline {
  agent any

  environment {
    ROUTING_YAML_FILE = 'routing_data.yaml'
  }

  stages {
    stage('Install Dependencies') {
      steps {
        sh 'pip3 install --user pyyaml'
      }
    }

    stage('Check Routing Expiry') {
      steps {
        sh '''
          python3 routing_expiry_checker.py \
            --action check_routing_expiry \
            --yaml ${ROUTING_YAML_FILE} \
            --days 20
        '''
      }
    }
  }

  post {
    success {
      echo "✅ Routing check passed."
    }
    failure {
      echo "❌ Routing check failed. Expiry detected or error occurred."
    }
  }
}
