from unittest import TestCase

from kubewatcher.kubewatcher import api_version_does_not_match


class Test(TestCase):
    def test_trigger_api_version_does_not_match__return_false_if_api_versions_match(self):
        pod_filter = {
            'apiVersion': 123
        }

        raw_object = {
            "apiVersion": 123
        }

        actual_return_value = api_version_does_not_match(pod_filter, raw_object)

        self.assertFalse(actual_return_value)

    def test_trigger_api_version_does_not_match__return_true_if_api_versions_does_not_match(self):
        pod_filter = {
            'apiVersion': 123
        }

        raw_object = {
            "apiVersion": 321
        }

        actual_return_value = api_version_does_not_match(pod_filter, raw_object)

        self.assertTrue(actual_return_value)

    def test_trigger_api_version_does_not_match__return_false_if_api_versions_is_not_specified(self):
        pod_filter = {
        }

        raw_object = {
            "apiVersion": 321
        }

        actual_return_value = api_version_does_not_match(pod_filter, raw_object)

        self.assertFalse(actual_return_value)
