pipeline {
    agent any
    stages {
        stage('Build') {
            agent {
                dockerfile {
                    filename 'Dockerfile.build'
                    dir '.'
                    additionalBuildArgs  '-u 169654:169654 --build-arg VERSION=1.0.0 --build-arg ITERATION=1'
                }
            }
            steps {
                sh 'ls -all'
            }
        }
    }
}