pipeline {
    agent any
    
    stages{
        stage('Build api-service Docker image'){
            steps{
                script{
                    sh 'docker build -t ahmedsoliman202/falsk-app-api-service -f ./api_service/Dockerfile .'
                }
            }
        }
        stage('Build stock-service docker image'){
            steps{
                script{
                    sh 'docker build -t ahmedsoliman202/falsk-app-stock-service -f ./stock_service/Dockerfile .'
                }
            }
        }
        stage('Push images to Hub'){
            steps{
                script{
                   sh 'docker login -u ahmedsoliman202 -p Do42615185' 
                // this is production way to define secret_text variable in Jenkins instead of using plain text
                //    withCredentials([string(credentialsId: 'dockerhub-pwd', variable: 'dockerhubpwd')]) { 
                //    sh 'docker login -u ahmedsoliman202 -p ${dockerhubpwd}' 
                   }
                   sh 'docker push ahmedsoliman202/falsk-app-api-service'
                   sh 'docker push ahmedsoliman202/falsk-app-stock-service'
                }
            }
        }
        
    }
