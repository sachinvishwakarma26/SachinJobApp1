pipeline {
    agent any

    environment {
        // Docker Configuration
        DOCKER_IMAGE_NAME = "sachinkumar26/djproject"
        DOCKER_IMAGE_TAG = "${BUILD_NUMBER}"
        DOCKER_REGISTRY = "docker.io"
        DOCKER_CREDENTIALS = credentials('docker-hub-credentials')

        // Git Configuration
        GIT_REPO = "https://github.com/sachinvishwakarma26/SachinJobApp1.git"
        GIT_BRANCH = "master"

        // Application Settings
        DJANGO_SETTINGS_MODULE = "djproject.settings"
        PYTHONUNBUFFERED = "1"
    }

    options {
        timestamps()
        timeout(time: 1, unit: 'HOURS')
        buildDiscarder(logRotator(numToKeepStr: '10', artifactNumToKeepStr: '5'))
        disableConcurrentBuilds()
    }

    stages {
        stage('🔍 Preparation') {
            steps {
                echo "========== Pipeline Started =========="
                echo "Job: ${JOB_NAME} - Build #${BUILD_NUMBER}"
                echo "Branch: ${GIT_BRANCH}"
                echo "Python Version: 3.8"
                
                cleanWs()
                checkout([
                    $class: 'GitSCM',
                    branches: [[name: "${GIT_BRANCH}"]],
                    userRemoteConfigs: [[url: "${GIT_REPO}"]]
                ])
            }
        }

        stage('📦 Install Dependencies') {
            steps {
                script {
                    echo "Installing Python dependencies..."
                    if (isUnix()) {
                        sh '''
                            python3 -m pip install --upgrade pip
                            pip install -r djproject/requirements.txt
                        '''
                    } else {
                        bat '''
                            python -m pip install --upgrade pip
                            pip install -r djproject/requirements.txt
                        '''
                    }
                }
            }
        }

        stage('🧪 Run Unit Tests & Code Coverage') {
            steps {
                script {
                    echo "Running Django unit tests..."
                    if (isUnix()) {
                        sh '''
                            cd djproject
                            python manage.py test testapp myapi --verbosity=2 || true
                            echo "Test stage completed"
                        '''
                    } else {
                        bat '''
                            cd djproject
                            python manage.py test testapp myapi --verbosity=2
                            echo Test stage completed
                        '''
                    }
                }
            }
            post {
                always {
                    junit(allowEmptyResults: true, testResults: 'djproject/test-results*.xml')
                }
            }
        }

        stage('🔧 Code Quality Analysis') {
            steps {
                script {
                    echo "Running code quality checks with flake8, black, and isort..."
                    if (isUnix()) {
                        sh '''
                            pip install --upgrade flake8 black isort pylint -q
                            
                            echo "Checking code style with flake8..."
                            flake8 djproject/testapp djproject/myapi --max-line-length=120 --statistics --format=pylint || true
                            
                            echo "Checking format with black..."
                            black --check djproject/testapp djproject/myapi || true
                            
                            echo "Checking import order with isort..."
                            isort --check-only djproject/testapp djproject/myapi || true
                        '''
                    } else {
                        bat '''
                            pip install --upgrade flake8 black isort pylint -q
                            
                            echo Checking code style with flake8...
                            flake8 djproject/testapp djproject/myapi --max-line-length=120 --statistics --format=pylint
                            
                            echo Checking format with black...
                            black --check djproject/testapp djproject/myapi
                            
                            echo Checking import order with isort...
                            isort --check-only djproject/testapp djproject/myapi
                        '''
                    }
                }
            }
            post {
                always {
                    echo "Code quality analysis completed"
                }
            }
        }

        stage('🐳 Build Docker Image') {
            steps {
                script {
                    echo "Building Docker image: ${DOCKER_IMAGE_NAME}:${DOCKER_IMAGE_TAG}"
                    if (isUnix()) {
                        sh '''
                            docker build \
                                --no-cache \
                                -t ${DOCKER_IMAGE_NAME}:${DOCKER_IMAGE_TAG} \
                                -t ${DOCKER_IMAGE_NAME}:latest \
                                -f Dockerfile .
                            echo "Docker image built successfully"
                            docker images | grep djproject
                        '''
                    } else {
                        bat '''
                            docker build --no-cache -t %DOCKER_IMAGE_NAME%:%DOCKER_IMAGE_TAG% -t %DOCKER_IMAGE_NAME%:latest -f Dockerfile .
                            echo Docker image built successfully
                            docker images | findstr djproject
                        '''
                    }
                }
            }
        }

        stage('✅ Docker Image Validation') {
            steps {
                script {
                    echo "Validating Docker image..."
                    if (isUnix()) {
                        sh '''
                            docker run --rm ${DOCKER_IMAGE_NAME}:${DOCKER_IMAGE_TAG} python --version
                            echo "Docker image validation successful"
                        '''
                    } else {
                        bat '''
                            docker run --rm %DOCKER_IMAGE_NAME%:%DOCKER_IMAGE_TAG% python --version
                            echo Docker image validation successful
                        '''
                    }
                }
            }
        }

        stage('📤 Push to Docker Registry') {
            when {
                branch 'master'
            }
            steps {
                script {
                    echo "Pushing Docker image to Docker Hub..."
                    if (isUnix()) {
                        sh '''
                            echo $DOCKER_CREDENTIALS_PSW | docker login -u $DOCKER_CREDENTIALS_USR --password-stdin ${DOCKER_REGISTRY}
                            docker push ${DOCKER_IMAGE_NAME}:${DOCKER_IMAGE_TAG}
                            docker push ${DOCKER_IMAGE_NAME}:latest
                            docker logout ${DOCKER_REGISTRY}
                            echo "Docker image pushed successfully"
                        '''
                    } else {
                        bat '''
                            echo %DOCKER_CREDENTIALS_PSW% | docker login -u %DOCKER_CREDENTIALS_USR% --password-stdin %DOCKER_REGISTRY%
                            docker push %DOCKER_IMAGE_NAME%:%DOCKER_IMAGE_TAG%
                            docker push %DOCKER_IMAGE_NAME%:latest
                            docker logout %DOCKER_REGISTRY%
                            echo Docker image pushed successfully
                        '''
                    }
                }
            }
        }

        stage('🚀 Deploy to Development') {
            when {
                branch 'master'
            }
            steps {
                script {
                    echo "Deploying to Development environment..."
                    if (isUnix()) {
                        sh '''
                            echo "Stopping existing container (if running)..."
                            docker rm -f djproject-dev || true
                            
                            echo "Starting new container..."
                            docker run -d \
                                --name djproject-dev \
                                -p 8001:8000 \
                                -e DJANGO_SETTINGS_MODULE=${DJANGO_SETTINGS_MODULE} \
                                -e DEBUG=True \
                                ${DOCKER_IMAGE_NAME}:${DOCKER_IMAGE_TAG}
                            
                            echo "Waiting for application to start..."
                            sleep 5
                            
                            echo "Container logs:"
                            docker logs djproject-dev || true
                            
                            echo "Development deployment completed"
                        '''
                    } else {
                        bat '''
                            echo Stopping existing container (if running)...
                            docker rm -f djproject-dev
                            
                            echo Starting new container...
                            docker run -d --name djproject-dev -p 8001:8000 -e DJANGO_SETTINGS_MODULE=%DJANGO_SETTINGS_MODULE% -e DEBUG=True %DOCKER_IMAGE_NAME%:%DOCKER_IMAGE_TAG%
                            
                            echo Waiting for application to start...
                            timeout /t 5
                            
                            echo Container logs:
                            docker logs djproject-dev
                            
                            echo Development deployment completed
                        '''
                    }
                }
            }
        }

        stage('🎯 Deploy to Kubernetes (Optional)') {
            when {
                branch 'master'
            }
            steps {
                script {
                    echo "Kubernetes deployment..."
                    if (isUnix()) {
                        sh '''
                            if command -v kubectl &> /dev/null; then
                                echo "Updating Kubernetes deployment with new image..."
                                kubectl set image deployment/django-app \
                                    django-app=${DOCKER_IMAGE_NAME}:${DOCKER_IMAGE_TAG} \
                                    -n default --record || echo "Kubernetes deployment not configured or not available"
                            else
                                echo "kubectl not found. Skipping Kubernetes deployment"
                            fi
                        '''
                    } else {
                        bat '''
                            where kubectl >nul 2>nul
                            if %ERRORLEVEL% equ 0 (
                                echo Updating Kubernetes deployment with new image...
                                kubectl set image deployment/django-app django-app=%DOCKER_IMAGE_NAME%:%DOCKER_IMAGE_TAG% -n default --record 2>nul || echo Kubernetes deployment not configured or not available
                            ) else (
                                echo kubectl not found. Skipping Kubernetes deployment
                            )
                        '''
                    }
                }
            }
        }

        stage('🧹 Cleanup') {
            steps {
                script {
                    if (isUnix()) {
                        sh '''
                            echo "Cleaning up dangling Docker images..."
                            docker image prune -f || true
                            
                            echo "Pipeline cleanup completed"
                        '''
                    } else {
                        bat '''
                            echo Cleaning up dangling Docker images...
                            docker image prune -f
                            
                            echo Pipeline cleanup completed
                        '''
                    }
                }
            }
            post {
                always {
                    cleanWs(
                        deleteDirs: true,
                        patterns: [
                            [pattern: '**/test-results*.xml', type: 'INCLUDE'],
                            [pattern: '**/coverage/**', type: 'INCLUDE']
                        ]
                    )
                }
            }
        }
    }

    post {
        success {
            echo "✅ Pipeline succeeded! Build #${BUILD_NUMBER} completed successfully"
        }
        failure {
            echo "❌ Pipeline failed! Build #${BUILD_NUMBER} encountered errors"
        }
        always {
            echo "========== Pipeline Finished =========="
        }
    }
}