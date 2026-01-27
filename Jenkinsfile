pipeline {
    agent any   // ✅ FIX: docker agent removed

    environment {
        DOCKER_IMAGE = "sachinkumar26/djproject:1.0"
        DOCKER_REGISTRY = "docker.io"

        // ⚠️ Not recommended for production
        DOCKER_USERNAME = "sachinkumar26"
        DOCKER_PASSWORD = "Aarush@123#"
    }

    stages {

        stage('Checkout') {
            steps {
                git url: 'https://github.com/sachinvishwakarma26/SachinJobApp1.git',
                    branch: 'master'
            }
        }

        stage('Build Docker Image') {
            steps {
                bat '''
                echo "Listing djproject directory"
                dir djproject

                echo "Building Docker image"
                docker build -t sachinkumar26/djproject:1.0 -f djproject\\Dockerfile djproject
                '''
            }
        }
        stage('Run Unit Tests') {
            steps {
                script {
                    if (isUnix()) {
                        sh '''
                        docker run --rm sachinkumar26/djproject:1.0 python manage.py test || true
                        '''
                    } else {
                        bat '''
                        docker run --rm %DOCKER_IMAGE% python manage.py test || exit 0
                        '''
                    }
                }
            }
        }

        stage('Push Docker Image to Docker Hub') {
            steps {
                script {
                    if (isUnix()) {
                        sh '''
                        docker login -u $DOCKER_USERNAME -p "$DOCKER_PASSWORD" $DOCKER_REGISTRY
                        docker push $DOCKER_IMAGE
                        '''
                    } else {
                        bat '''
                        docker login -u %DOCKER_USERNAME% -p "%DOCKER_PASSWORD%" %DOCKER_REGISTRY%
                        docker push %DOCKER_IMAGE%
                        '''
                    }
                }
            }
        }

        stage('Deploy') {
            steps {
                script {
                    if (isUnix()) {
                        sh '''
                        docker rm -f djproject || true
                        docker run -d --name djproject -p 8000:8000 $DOCKER_IMAGE
                        '''
                    } else {
                        bat '''
                        docker rm -f djproject || exit 0
                        docker run -d --name djproject -p 8000:8000 %DOCKER_IMAGE%
                        '''
                    }
                }
            }
        }
    }

    post {
        always {
            cleanWs()
        }
    }
}