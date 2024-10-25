# Experimenter deployment

Uses AWS Lambda, AWS API Gateway, and whatever else the Chalice framework creates to provide experiment.

# Meta-requirements

AWS credentials should be set up, and the us-west-2 region configured, in ~/.aws/credentials.

An AWS Certificate Manager certificate should be set up as described in ssl.md.

Domains should be created with DigitalOcean:
- experimenter.phu73l.net

# Requirements

- debian box (trixie, ubuntu 23)
- Python 3.11-3.12, but this should be Python 3.10
- apt package awscli

# Deploy and development docs

We use dev, stage, and prod instances. We will document stage here.

The instance type is determined by the domain and related attributes configured for it. The Twilio Programmable Voice components are pointed at URLs on the domain. An instance can be deleted when the relevant Twilio components don't point to it.

---

# Setup

To be done once.

## Set up environment secrets

Populate .env to match .env.sample as described in aws.md:

- chalicelib/environment/.env

## Create deployment virtualenv

- python3 -m venv venv
- source venv/bin/activate
- pip install -r requirements.txt
- python3 -m pip install chalice pytest

---

# Create and deploy new instances

## Create or check out branch

If deploying stage or prod, check out or create relevant release branch.

## Test

See test.md. Run the local tests.

## Deploy instances

- source venv/bin/activate
- chalice deploy --stage stage

Note the AliasDomainName.

## Update domain

XXX add alias domain name for REST back

XXX This is for the alias domain name for REST, not working, see websocket_api_custom_domain in .config.json, needs regional cert?

Have the AliasDomainName from the deploy or find the alias_domain_name:
- .chalice/deployed/stage.json

Using the DigitalOcean network web console, add or update CNAME records for domains:
- experimenter.phu73l.net
  - hostname stage.experimenter.phu73l.net
  - alias: <alias domain name>

Wait for DNS to be updated:

- nslookup stage.experimenter.phu73l.net

## Update Twilio Programmable Voice stage components to point to dialplan URLs

XXX have a twilio.md
twiml app publishes twiml pointing to websocket? or conference?
phone number points to twiml
sip domain points to twiml

Update the stage TwiML Application Resources and SIP Domains to point to the dialplan URL in the updated domain as in twilio-sip-server deploy.md.

For the SIP domains, the URL path is "/dial_outgoing".

For the Application Resources, the URL path is "/dial_sip_e164".

## Test

If stage, see test.md. Run the tests against the deployed instance.

# Update an existing instance

## Test

See test.md. Run the local tests.

## Deploy instances

- source venv/bin/activate
- chalice deploy --stage stage

## Test

If stage, see test.md. Run the tests against the deployed instance.

# Delete instances

- source venv/bin/activate
- chalice delete --stage stage

Using the DigitalOcean network web console, remove CNAME records for domains:
- experimenter.phu73l.net


# Notes

- wsdump must be in a term
- source venv/bin/activate
- wsdump wss://wwisk9qvg7.execute-api.us-west-2.amazonaws.com/api
- wsdump wss://stage.experimenter.phu73l.net
- chalice logs --stage stage -n websocket_message --follow
