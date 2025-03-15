# Twilio deployment

# Requirements

- Twilio CLI package eg twilio-5.22.3-amd64.deb.
- Twilio profile or other way to use creds
  - twilio profiles:create
  - twilio profiles:use [id]

# Setup

To be done once.

## Create TwiML Bin

- Visit the web console for TwiML Bins.
- Create new TwiML Bin
- Friendy name experimenter-stage
- Twiml <deploy/lambda-websocket-experimenter-stage>

Note the URL.

XXX Instead of pause, redirect to handle stream close.

## Create SIP domain

    twilio api:core:sip:domains:create \
        --domain-name=experimenter-stage.sip.twilio.com \
        --friendly-name=experimenter-stage \
        --sip-registration \
        --no-emergency-calling-enabled \
        --voice-method=GET \
        --voice-url='<BIN URL>'

Note that if the SIP Domain already exists, this will fail instead of updating the domain.

Note the SID.

## Create the Credential List

- twilio api:core:sip:credential-lists:create --friendly-name experimenter-stage

## List the Credential Lists to get the created SID

- twilio api:core:sip:credential-lists:list

## Create auth registrations Credential List Mappings

- twilio api:core:sip:domains:auth:registrations:credential-list-mappings:create --domain-sid <SIP DOMAIN SID> --credential-list-sid <CREDENTIAL LIST SID>

## Set voice authentication credentials for SIP Domain

Visit the GUI for the SIP Domains and add the same "experimenter-stage" credential list to "voice authentication", then save.

---

# Add configuration for a new SIP client

## Create credential

Create a new credential in the Credential List. Use the SID found in the previous step, or list to get it.

- twilio api:core:sip:credential-lists:list
- twilio api:core:sip:credential-lists:credentials:create --credential-list-sid <SID> --username '<USER>' --password '<PASSWORD>'

# Delete configuration for a SIP client

Delete the credential from the Credential List with the web GUI.
