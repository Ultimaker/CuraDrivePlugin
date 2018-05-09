#!/usr/bin/groovy

// Jenkins configuration
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
        // We do a custom checkout
        stage("Checkout")
        {
            checkout scm
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