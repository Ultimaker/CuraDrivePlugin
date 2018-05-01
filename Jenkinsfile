#!/usr/bin/groovy

// Jenkins configuration
def gitCredentials = '28d236ba-4536-4489-b2bf-38cb09241a3a'
def gitCredentialsSSH = '47a97e56-aa4a-43d7-a7b0-c9a352757095'
def secretsRepo = "stardust-k8s_secrets"
def slackChannel = "#stardust-alerts"
def defaultNode = "docker"

// Google Cloud configuration.
def gcloudRegistry = "eu.gcr.io"
def gcloudProjectName = "stardust-193112"
def gcloudComputeZone = "europe-west1-d"
def gcloudClusterNamePrefix = "stardust"

// App configuration.
def environmentName = "staging"
def appName = "cura-cloud-slicer"
def imageTag = "${gcloudRegistry}/${gcloudProjectName}/${appName}:${env.BRANCH_NAME}.${env.BUILD_NUMBER}"

node(defaultNode)
{
    try
    {
        // We do a custom checkout to pull the submodules
        stage("Checkout")
        {
            checkout scm

            sshagent(credentials: [gitCredentialsSSH])
            {
                sh "git submodule update --init"

                // Checking if the common lib is behind master.
                def masterDiff = sh(script: "lib/stardustCommons/master-diff.sh", returnStdout: true).toInteger()

                // last commit in master is always a merge commit, so we may ignore it.
                if (masterDiff > 1)
                {
                    slackSend (color: 'warning', channel: env.SLACK_CHANNEL,
                        message: "${env.JOB_NAME} - #${env.BUILD_NUMBER} Common lib is ${masterDiff} commits behind master (<${env.BUILD_URL}|Open>)")
                }
            }
        }

        // Build the Docker image for this service
        stage("Build")
        {
            sh "docker build --tag ${imageTag} ."
        }

        // All branches except master and staging are only used for CI.
        if (env.BRANCH_NAME != "master" && env.BRANCH_NAME != "staging")
        {
            currentBuild.result = "SUCCESS"
            return
        }

        // Let Slack know about our new deployment.
        stage('Notify')
        {
            slackSend (color: 'good', channel: slackChannel, message: "${env.JOB_NAME} - #${env.BUILD_NUMBER} Success (<${env.BUILD_URL}|Open>)")
        }
    }
    catch(e)
    {
        slackSend (color: 'danger', channel: slackChannel, message: "${env.JOB_NAME} - #${env.BUILD_NUMBER} Failure (<${env.BUILD_URL}|Open>)")
        throw e
    }
}