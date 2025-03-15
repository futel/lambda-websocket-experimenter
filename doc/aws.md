# AWS deployment

Other AWS components which must be set up before deploying, and local setup for them.

# Meta-requirements

AWS credentials should be set up, and the us-west-2 region configured, in ~/.aws/credentials.

# Setup

## Set up environment secrets

Populate .env to match .env.sample:
- app/chalicelib/environment/.env

- AWS_DEFAULT_REGION us-west-2

## Set up DynamoDB table

- aws dynamodb create-table --cli-input-json file://deploy/dynamodb.json 

## Set up SNS topic

XXX Obsolete, but we will need some kind of logging?

- aws sns create-topic --name lambda_websocket_experimenter

Note the ARN and update the SNS_ARN value in .env as described in DEPLOY.md.
XXX DEPLOY.md doesn't describe this? .env says that this is updated by chalice on deploy?
