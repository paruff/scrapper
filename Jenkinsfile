pipeline {
  agent any
  options {
    ansiColor('xterm')
    timestamps()
    timeout(time: 20, unit: 'MINUTES')
  }
  environment {
    PYTHONUNBUFFERED = '1'
    VENV_DIR = '.venv'
  }
  stages {
    stage('Checkout') {
      steps {
        checkout scm
      }
    }
    stage('Setup Python venv') {
      steps {
        sh '''
          set -e
          python3 --version
          python3 -m venv "$VENV_DIR"
          . "$VENV_DIR/bin/activate"
          python -m pip install --upgrade pip
          pip install -r requirements.txt
          pip install -r dev-requirements.txt
        '''
      }
    }
    stage('Lint') {
      steps {
        sh '''
          . "$VENV_DIR/bin/activate"
          ruff check .
        '''
      }
    }
    stage('Format Check') {
      steps {
        sh '''
          . "$VENV_DIR/bin/activate"
          ruff format --check .
        '''
      }
    }
    stage('Type Check (non-blocking)') {
      steps {
        sh '''
          . "$VENV_DIR/bin/activate"
          set +e
          mypy vrm_crawl
          echo "mypy completed (non-blocking)"
        '''
      }
    }
    stage('Security (non-blocking)') {
      steps {
        sh '''
          . "$VENV_DIR/bin/activate"
          set +e
          bandit -r vrm_crawl/
          echo "bandit completed (non-blocking)"
        '''
      }
    }
    stage('Tests') {
      steps {
        sh '''
          . "$VENV_DIR/bin/activate"
          pytest -v --tb=short --junitxml=junit.xml --cov=vrm_crawl --cov-report=xml:coverage.xml
        '''
      }
    }
  }
  post {
    always {
      junit 'junit.xml'
      archiveArtifacts artifacts: 'coverage.xml', allowEmptyArchive: true
      archiveArtifacts artifacts: 'output/**/*', allowEmptyArchive: true
    }
  }
}
