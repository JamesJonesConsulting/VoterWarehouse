pipeline {
    agent any
    stages {
        stage('Build') {
            agent {
                dockerfile {
                    filename 'Dockerfile.build'
                    dir '.'
                    label 'podman'
                    additionalBuildArgs  '--build-arg VERSION=1.0.0 --build-arg ITERATION=1'
                }
            }
            steps {
                sh 'ls -all'
            }
        }
    }
}