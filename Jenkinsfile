pipeline {
    agent any
    stages {
        stage('Login') {
            steps {
                withCredentials([usernamePassword(credentialsId: 'ecda8ec0-1a31-429e-b5b4-05f285cbf738', usernameVariable: 'USERNAME', passwordVariable: 'PASSWORD')]) {
                    sh 'docker login -u $USERNAME -p $PASSWORD'
                }
            }
        }
        stage("Docker build container apache") {
            steps {
                dir('apache') {
                    sh """
                        docker build -t foxtail220/apache-jenkins2:1.${env.BUILD_NUMBER} .
                        docker push foxtail220/apache-jenkins2:1.${env.BUILD_NUMBER}
                        docker rmi -f foxtail220/apache-jenkins2:1.${env.BUILD_NUMBER}
                    """
                }
            }
        }
        stage('Docker build container nginx') {
            steps {
                dir('nginx') {
                    sh """
                        docker build -t foxtail220/nginx-jenkins2:1.${env.BUILD_NUMBER} .
                        docker push foxtail220/nginx-jenkins2:1.${env.BUILD_NUMBER}
                        docker rmi -f foxtail220/nginx-jenkins2:1.${env.BUILD_NUMBER}
                    """
                }
            }
        }
    }
}
