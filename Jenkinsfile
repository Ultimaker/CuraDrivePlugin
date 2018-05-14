#!/usr/bin/groovy

// Jenkins configuration
def gitCredentials = '28d236ba-4536-4489-b2bf-38cb09241a3a'
def gitCredentialsSSH = '47a97e56-aa4a-43d7-a7b0-c9a352757095'
def slackChannel = "#stardust-alerts"
def defaultNode = "docker"

// App configuration
def environmentName = "testing"
def appName = "cura-drive-plugin"
def imageTag = "${appName}:${environmentName}"

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
            }
        }

        // Build the Docker image for this service
        stage("Build")
        {
            sh "./build.sh ${imageTag}"
        }

        // Build the .curapackage to ensure it still works.
        stage("Package")
        {
            sh "./build_plugin.sh"
        }
    }
    catch(e)
    {
        slackSend (color: 'danger', channel: slackChannel, message: "${env.JOB_NAME} - #${env.BUILD_NUMBER} Failure (<${env.BUILD_URL}|Open>)")
        throw e
    }
}