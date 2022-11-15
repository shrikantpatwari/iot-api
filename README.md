# IOT-API APP (iot-api)

This project contains source code and supporting files for a serverless application that you can deploy with the SAM CLI.
this project is basically a python flask rest api project to add device and its sensor data. It includes the following files and folders.

- flask_api - Code for the application's Lambda function to add device, rename device, add sensor data and query sensor data.
- template.yaml - A template that defines the application's AWS resources.

The application uses several AWS resources, including Lambda functions and an API Gateway API. These resources are defined in the `template.yaml` file in this project.

## Deploy the iot-api application

With SAM we can deploy our serverless app to aws which creates all service instance defined in template.yml. To use the SAM CLI, you need the following tools.

* SAM CLI - [Install the SAM CLI](https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/serverless-sam-cli-install.html)
* [Python 3 installed](https://www.python.org/downloads/)
* Docker - [Install Docker community edition](https://hub.docker.com/search/?type=edition&offering=community)

To build and deploy your application for the first time, run the following in your shell:

```bash
sam build --region us-east-2
sam deploy --stack-name iot-api-v1 --region us-east-2
```

The first command will build the source of your application. The second command will package and deploy your application to AWS, with a series of prompts:

* **Stack Name**: The name of the stack to deploy to CloudFormation. This should be unique to your account and region, and a good starting point would be something matching your project name.
* **AWS Region**: The AWS region you want to deploy your app to.
* **Confirm changes before deploy**: If set to yes, any change sets will be shown to you before execution for manual review. If set to no, the AWS SAM CLI will automatically deploy application changes.
* **Allow SAM CLI IAM role creation**: Many AWS SAM templates, including this example, create AWS IAM roles required for the AWS Lambda function(s) included to access AWS services. By default, these are scoped down to minimum required permissions. To deploy an AWS CloudFormation stack which creates or modifies IAM roles, the `CAPABILITY_IAM` value for `capabilities` must be provided. If permission isn't provided through this prompt, to deploy this example you must explicitly pass `--capabilities CAPABILITY_IAM` to the `sam deploy` command.
* **Save arguments to samconfig.toml**: If set to yes, your choices will be saved to a configuration file inside the project, so that in the future you can just re-run `sam deploy` without parameters to deploy changes to your application.

You can find your API Gateway Endpoint URL in the output values displayed after deployment.

## Table structure

IOT-API app has 3 tables strored on aws dynamodb, details are below

<b>iot-devices </b>

| field | description |
|-------|-------------|
| deviceId | device id is auto generated UUID |
| deviceName | User proviced device name |
| userId | User id from auth token |
| sensors | List of sensor id, sensor table has sensor details |
| createdAt | Record created timestamp in milliseconds |
| updatedAt | Record updated timestamp in milliseconds |


<b>iot-device-sensors</b>

| field | description |
|-------|-------------|
| sensorId | sensor id is auto generated UUID |
| sensorType | Type of sensor e.g. TEMP or PRESSURE |
| sensorName | Name of sensor |
| createdAt | Record created timestamp in milliseconds |
| updatedAt | Record updated timestamp in milliseconds |


<b>iot-device-sensors-data</b>

| field | description |
|-------|-------------|
| deviceId | device id |
| sensorId | sensor id |
| timeKey | time at which data is sent |
| data | Actual data sent by sensor |
| createdAt | Record created timestamp in milliseconds |
| updatedAt | Record updated timestamp in milliseconds |

-------------------------------

## API availble

Please import Insomnia_API_Collection.json in Insomnia client

## Use the SAM CLI to build and test locally

Build your application with the `sam build --use-container` command.

```bash
iot-api$ sam build --use-container
```

The SAM CLI installs dependencies defined in `flask_api/requirements.txt`, creates a deployment package, and saves it in the `.aws-sam/build` folder.

The SAM CLI can also emulate your application's API. Use the `sam local start-api` to run the API locally on port 3000.

```bash
iot-api$ sam local start-api
iot-api$ curl http://localhost:3000/
```


## Cleanup

To delete the sample application that you created, use the AWS CLI. Assuming you used your project name for the stack name, you can run the following:

```bash
aws cloudformation delete-stack --stack-name iot-api-v1
```
