library 'pipeline-utils@master'

pipeline {
    agent {
        kubernetes {
            yaml '''
kind: Pod
metadata:
  name: kaniko
spec:
  containers:
  - name: jnlp
    workingDir: /home/jenkins/agent
  - name: kaniko
    workingDir: /home/jenkins/agent
    image: gcr.io/kaniko-project/executor:debug
    imagePullPolicy: Always
    resources:
      requests:
        cpu: "500m"
        memory: "1Gi"
        ephemeral-storage: "4Gi"
      limits:
        cpu: "1000m"
        memory: "2Gi"
        ephemeral-storage: "4Gi"
    command:
    - /busybox/cat
    tty: true
    volumeMounts:
    - name: jenkins-docker-cfg
      mountPath: /kaniko/.docker
  - name: crane
    workingDir: /tmp/jenkins
    image: gcr.io/go-containerregistry/crane:debug
    imagePullPolicy: Always
    command:
    - /busybox/cat
    tty: true
  volumes:
  - name: jenkins-docker-cfg
    projected:
      sources:
      - secret:
          name: rencibuild-imagepull-secret
          items:
            - key: .dockerconfigjson
              path: config.json
'''
        }
    }
    environment {
        PATH = "/busybox:/kaniko:/ko-app/:$PATH"
        DOCKERHUB_CREDS = credentials("${env.REGISTRY_CREDS_ID_STR}")
        REGISTRY = "${env.DOCKER_REGISTRY}"
        REG_OWNER="helxplatform"
        REG_APP="heal-sparc-converter"
        COMMIT_HASH="${sh(script:"git rev-parse --short HEAD", returnStdout: true).trim()}"
        VERSION_FILE="./_version.py"
        VERSION="${sh(script:'awk \'{ print $3 }\' ./_version.py | xargs', returnStdout: true).trim()}"
        IMAGE_NAME="${REG_OWNER}/${REG_APP}"
        TAG1="$BRANCH_NAME"
        TAG2="$COMMIT_HASH"
        TAG3="$VERSION"
        TAG4="latest"
    }
    stages {
        stage('Test') {
            steps {
                sh '''
                echo "Stage test"
                '''
            }
        }
        stage('Build') {
            steps {
                script {
                    container(name: 'kaniko', shell: '/busybox/sh') {
                        kaniko.build("./Dockerfile", ["$IMAGE_NAME:$TAG1", "$IMAGE_NAME:$TAG2", "$IMAGE_NAME:$TAG3", "$IMAGE_NAME:$TAG4"])
                    }
                }
            }
            post {
                always {
                    archiveArtifacts artifacts: 'image.tar', onlyIfSuccessful: true
                }
            }
        }
        stage('Publish') {
            steps {
                script {
                    container(name: 'crane', shell: '/busybox/sh') {
                        def imageTagsToPushAlways = ["$IMAGE_NAME:$TAG1", "$IMAGE_NAME:$TAG2"]
                        def imageTagsToPushForDevelopBranch = ["$IMAGE_NAME:$TAG3"]
                        def imageTagsToPushForMasterBranch = ["$IMAGE_NAME:$TAG4"]
                        image.publish(imageTagsToPushAlways, imageTagsToPushForDevelopBranch, imageTagsToPushForMasterBranch)
                    }
                }
            }
            post {
                cleanup {
                    sh '''
                    echo "Remove archived artifacts."
                    '''
                }
            }
        }
    }
}
