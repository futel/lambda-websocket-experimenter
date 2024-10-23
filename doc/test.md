# Testing and monitoring

# Unit test

These test against the local source.

- source venv/bin/activate
- pytest test

# Smoke API integration test

These test against the current stage deployment. Note that these will cause side effects like log generation.

- source venv/bin/activate
- pytest itest

# Acceptance test

XXX

# View logs

- chalice logs --stage stage --since 10m --follow

# View components in AWS console

- region us-west-2
- AWS Lambda dashboard
