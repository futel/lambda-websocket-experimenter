from unittest import mock, TestCase

from chalicelib import util

env = {
    #'AWS_LOGS_TOPIC_ARN': 'AWS_LOGS_TOPIC_ARN',
    #'AWS_METRICS_TOPIC_ARN': 'AWS_METRICS_TOPIC_ARN',
    #'TWILIO_ACCOUNT_SID': 'TWILIO_ACCOUNT_SID',
    #'TWILIO_AUTH_TOKEN': 'TWILIO_AUTH_TOKEN',
    'table': mock.MagicMock()
}

class TestUtil(TestCase):

    def test_log(self):
        util.log('foo')

    def test_announce_connection(self):
        util.announce_connection('foo', env)

    def test_remove_connection(self):
        util.remove_connection('foo', env)
