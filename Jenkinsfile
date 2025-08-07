pipeline {
    agent any

    environment {
        // Define the Docker image name and tag for Docker Hub
        DOCKER_IMAGE = "sachinkumar26/djproject:1.0"
        DOCKER_REGISTRY = "docker.io" // Docker Hub registry URL

        // Hardcoded Docker credentials (NOT recommended for production)
        DOCKER_USERNAME = "sachinkumar26"
        DOCKER_PASSWORD = "Aarush@123#"
    }

    stages {
        stage('Checkout') {
            steps {
                // Checkout the source code from your GitHub repository
                git url: 'https://github.com/sachinvishwakarma26/SachinJobApp1.git', branch: 'master'
            }
        }

        stage('Build Docker Image') {
            steps {
                script {
                    if (isUnix()) {
                        // Build Docker image for Unix-based systems
                        sh 'docker build -t $DOCKER_IMAGE -f djproject/Dockerfile .'
                    } else {
                        // Build Docker image for Windows systems
                        bat 'docker build -t %DOCKER_IMAGE% -f djproject/Dockerfile .'
                    }
                }
            }
        }

        stage('Push Docker Image to Docker Hub') {
            steps {
                script {
                    if (isUnix()) {
                        // Docker login and push for Linux
                        sh 'docker login -u $DOCKER_USERNAME -p $DOCKER_PASSWORD $DOCKER_REGISTRY'
                        sh 'docker push $DOCKER_IMAGE'
                    } else {
                        // Docker login and push for Windows
                        bat 'docker login -u %DOCKER_USERNAME% -p %DOCKER_PASSWORD% %DOCKER_REGISTRY%'
                        bat 'docker push %DOCKER_IMAGE%'
                    }
                }
            }
        }

        stage('Deploy') {
            steps {
                script {
                    if (isUnix()) {
                        // Run Docker container for Linux
                        sh 'docker run -d -p 8000:8000 $DOCKER_IMAGE'
                    } else {
                        // Run Docker container for Windows
                        bat 'start /b docker run -d -p 8000:8000 %DOCKER_IMAGE%'
                    }
                }
            }
        }
    }

    post {
        always {
            // Clean up the workspace after the pipeline finishes
            cleanWs()
        }
    }
}
