# Testing and monitoring

# Setup

To be done once.

- source venv/bin/activate
- pip install websocket-client

# Unit test

These test against the local source.

- source venv/bin/activate
- pytest app/test

# Smoke API integration test

These test against the current stage deployment. Note that these will cause side effects like log generation.

- source venv/bin/activate
 - pytest app/itest

# Smoke manual test

These test against the current stage deployment. Note that these will cause side effects like log generation.

Use wsdump against the Websocket API URL given during deploy e.g.

- wsdump wss://stage.experimenter.phu73l.net

XXX

Hit the URL on the TwiML page e.g.

        wget https://ws.app-dev.phu73l.net/index.xml

# Acceptance test

XXX

# View logs

- cd app
- aws logs tail /aws/lambda/experimenter-stage-websocket_connect --format short --follow

XXX other groups also, is this possible with the logs cli command?

# View logs

- aws logs start-live-tail --log-group-identifiers arn:aws:logs:us-west-2:168594572693:log-group:/aws/lambda/experimenter-stage-websocket_connect

XXX sub ARN from cloudwatch log groups page or from the chalice deploy output
XXX other groups also, is this possible with the start-live-tail cli command?

# View logs in AWS console

- cloudwatch
- live tail
- filter log groups
  - /aws/lambda/experimenter-stage-websocket_connect
  - /aws/lambda/experimenter-stage-websocket_disconnect
  - /aws/lambda/experimenter-stage-websocket_message
- start
