from unittest import mock, TestCase

from chalicelib import env_util

env = env_util.get_env()


class TestFoo(TestCase):

    def test_exercise(self):
        assert(True)
