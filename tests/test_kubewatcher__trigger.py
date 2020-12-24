from unittest import TestCase, mock

from kubewatcher.kubewatcher import trigger


class Test(TestCase):
    def test_trigger__return_false_if_api_version_does_not_match_returns_true(self):
        with mock.patch("kubewatcher.kubewatcher.api_version_does_not_match") as api_version_does_not_match:
            api_version_does_not_match.return_value = True

            actual_return_value = trigger({}, {})

            self.assertFalse(actual_return_value)

    def test_trigger__return_false_if_namespace_ignored_returns_true(self):
        pod_filter = {
            'namespaces': {}
        }

        raw_object = {
            "metadata": {
                "namespace": "namespace"
            }
        }

        with mock.patch("kubewatcher.kubewatcher.namespace_ignored") as namespace_ignored:
            namespace_ignored.return_value = True

            actual_return_value = trigger(pod_filter, raw_object)

            self.assertFalse(actual_return_value)

    def test_trigger__return_false_if_namespace_not_included_returns_true(self):
        pod_filter = {
            'namespaces': {}
        }

        raw_object = {
            "metadata": {
                "namespace": "namespace"
            }
        }

        with mock.patch("kubewatcher.kubewatcher.namespace_not_included") as namespace_not_included:
            namespace_not_included.return_value = True

            actual_return_value = trigger(pod_filter, raw_object)

            self.assertFalse(actual_return_value)

    def test_trigger__true_if_all_conditions_are_met(self):
        pod_filter = {
            "conditions": [
                "condition0",
                "condition1"
            ]
        }

        raw_object = {
            "metadata": {
                "namespace": "namespace"
            }
        }

        with mock.patch("kubewatcher.kubewatcher.evaluate_path", new=custom_evaluate_path):
            actual_return_value = trigger(pod_filter, raw_object)

            self.assertTrue(actual_return_value)

    def test_trigger__false_if_a_condition_is_not_met(self):
        pod_filter = {
            "conditions": [
                "condition0",
                "condition2"
            ]
        }

        raw_object = {
            "metadata": {
                "namespace": "namespace"
            }
        }

        with mock.patch("kubewatcher.kubewatcher.evaluate_path", new=custom_evaluate_path):
            actual_return_value = trigger(pod_filter, raw_object)

            self.assertFalse(actual_return_value)


def custom_evaluate_path(raw_object, condition):
    if condition == "condition0":
        return True
    if condition == "condition1":
        return True
    if condition == "condition2":
        return False
