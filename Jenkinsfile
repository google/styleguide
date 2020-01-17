#!groovy

// Use 'ci-jenkins@somebranch' to pull shared lib from a different branch than the default.
// Default is configured in Jenkins and should be from "stable" tag.
@Library("ci-jenkins") import com.swiftnav.ci.*

def context = new Context(context: this)
context.setRepo('styleguide')
def builder = context.getBuilder()
def logger = context.getLogger()

pipeline {
    // Override agent in each stage to make sure we don't share containers among stages.
    agent any
    options {
        // Make sure job aborts after 2 hours if hanging.
        timeout(time: 2, unit: 'HOURS')
        timestamps()
        // Keep builds for 7 days.
        buildDiscarder(logRotator(daysToKeepStr: '7'))
    }

    parameters {
        choice(name: "LOG_LEVEL", choices: ['info', 'debug', 'warning', 'error'], description: 'Log Level')
        string(name: 'STAGE_INCLUDE', defaultValue: '', description: 'Regular expression for stages to run. Leave empty to run all stages.')
    }

    stage('Test') {
        steps {
            println "Hello, this is a test!!"
        }
    }
}

