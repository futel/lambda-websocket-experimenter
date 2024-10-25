# SSL certificate

Certificates are needed to for AWS Lambda to publish http and websocket endpoints with a custom domain name.

# Meta-requirements

AWS ACM console access must have been set up.

Domains should be created with DigitalOcean:
- experimenter.phu73l.net

The phu73l.net certificate (and not *.phu37l.net) should have been set up for the dialplan-functions component.

# Requirements

- debian box (trixie, ubuntu 23)
- openssl (3.2.2-1)
- snapd apt package
  - sudo apd install snapd
- snapd snap package
  - sudo snap install snapd
- certbot and plugin snap (2.11.0)
  - sudo snap install --classic certbot
  - sudo ln -s /snap/bin/certbot /usr/bin/certbot
  - sudo snap set certbot trust-plugin-with-root=ok
  - sudo snap install certbot-dns-digitalocean
- DigitalOcean access token with all the domain scopes in conf/certbot-creds.ini

---

# Create certificate

This needs to be done to create the first certificate, or to create a replacement after changing attributes.

This should be done on whatever box is handling renewals. This deployment process doesn't outline requirements to make automatic renewal reliable, eg it is probably running on a laptop, so manual renewals or at least verification are assumed.

- sudo certbot certonly --dns-digitalocean --dns-digitalocean-credentials conf/certbot-creds.ini -d experimenter.phu73l.net -d *.experimenter.phu73l.net
- add expiration to calendar
- sudo cat /etc/letsencrypt/live/experimenter.phu73l.net/cert.pem /etc/letsencrypt/live/experimenter.phu73l.net/chain.pem /etc/letsencrypt/live/experimenter.phu73l.net/fullchain.pem >/tmp/all.pem

# Import or reimport and deploy certificate

This needs to be done after a certificate is created or renewed.

- visit AWS certificate manager (ACM) web console
- change region to us-west-2
- import a certificate, or list, visit, reimport certificate with domain experimenter.phu73l.net
 - certificate body /etc/letsencrypt/live/experimenter.phu73l.net/cert.pem
 - certificate private key /etc/letsencrypt/live/experimenter.phu73l.net/privkey.pem
 - certificate chain /tmp/all.pem
 
If this is a new certificate, note the ARN. This is needed to deploy the AWS API Gateway.

# Update Lambda functions to use new certificate

This needs to be done after a certificate is created.

- update config files:
  - .chalice/config.json
  - Update every certificate_arn
- deploy affected stages as described in DEPLOY.md.

---

# Renew and deploy certificate

Certificates must be renewed before they expire.

The certificate creation method might set up automatic renewal using systemd? Notice the renewal warning email, check, and be prepared to manually renew at the end of the certificate's life. This deployment process doesn't outline requirements to make automatic renewal reliable, eg it is probably running on a laptop, and we need to reimport to aws after renewal?

sudo certbot renew --cert-name dialplans.phu73l.net --dns-digitalocean --dns-digitalocean-credentials conf/certbot-creds.ini

- add expiration to calendar, "sudo certbot certificates" to show the date
- sudo cat /etc/letsencrypt/live/phu73l.net/cert.pem /etc/letsencrypt/live/phu73l.net/chain.pem /etc/letsencrypt/live/phu73l.net/fullchain.pem >/tmp/all.pem
- Reimport the certificate as in Import or reimport and deploy certificate

---

# Delete certificates

This does not normally have to be done.

- certbot certificates
- certbot delete --cert-name dev.dialplans.phu73l.net
- visit ACM web console

# List certificates

- certbot certificates
- visit AWS ACM web console
- change region to us-east-1


# Test

Run the itest tests, or POST to a smoke test URL, as described in test.md.
