# AWS deployment

Other AWS components which must be set up before deploying, and local setup for them.

# Meta-requirements

AWS credentials should be set up, and the us-west-2 region configured, in ~/.aws/credentials.

# Setup

## Set up environment secrets

Populate .env to match .env.sample:
- chalicelib/environment/.env

- AWS_DEFAULT_REGION us-west-2

## Set up SNS topic

- aws sns create-topic --name lambda_websocket_experimenter

Note tha ARN and update the SNS_ARN value in .env as described in DEPLOY.md.
