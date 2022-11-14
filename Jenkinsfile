pipeline {
    agent any
    stages {
        stage('Build') {
//             agent {
//                 dockerfile {
//                     filename 'Dockerfile.build'
//                     dir '.'
//                     additionalBuildArgs  '--build-arg VERSION=1.0.0 --build-arg ITERATION=1'
//                 }
//             }
            steps {
                sh '''
                ansible-galaxy collection install -r ansible/requirements.yml
                echo ${GIT_BRANCH#origin/} | sed -r 's|/|-|g'
                ansible-playbook ansible/playbook.yml -vvv
                '''
            }
        }
    }
}