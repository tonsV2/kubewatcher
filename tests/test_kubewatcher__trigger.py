from unittest import TestCase

from kubewatcher.filter import Filter


class Test(TestCase):
    def test_trigger__return_false_if_api_version_does_not_match(self):
        raw_object = {
            "apiVersion": "123"
        }

        raw_filter = {
            "kind": "kind",
            "apiVersion": "321",
            "conditions": [],
            "message": {},
            "tests": []
        }

        f = Filter(raw_filter)

        actual_return_value = f.trigger(raw_object)

        self.assertFalse(actual_return_value)

    def test_trigger__return_false_if_namespace_ignored(self):
        raw_filter = {
            "kind": "kind",
            "conditions": [],
            "message": {},
            "tests": [],
            'namespaces': {
                'ignore': ['namespace']
            }
        }

        raw_object = {
            "apiVersion": "123",
            "metadata": {
                "namespace": "namespace"
            }
        }

        f = Filter(raw_filter)

        actual_return_value = f.trigger(raw_object)

        self.assertFalse(actual_return_value)

    def test_trigger__return_false_if_namespace_not_included_returns_true(self):
        raw_filter = {
            "kind": "kind",
            "conditions": [],
            "message": {},
            "tests": [],
            'namespaces': {
                'include': []
            }
        }

        raw_object = {
            "apiVersion": "123",
            "metadata": {
                "namespace": "namespace"
            }
        }

        f = Filter(raw_filter)
        actual_return_value = f.trigger(raw_object)

        self.assertFalse(actual_return_value)

    def test_trigger__true_if_all_conditions_are_met(self):
        raw_filter = {
            "kind": "kind",
            "conditions": [
                "[condition0==true]",
                "[condition1==true]"
            ],
            "message": {},
            "tests": []
        }

        raw_object = {
            "apiVersion": "123",
            "metadata": {
                "namespace": "namespace"
            },
            "condition0": "true",
            "condition1": "true"
        }

        f = Filter(raw_filter)

        actual_return_value = f.trigger(raw_object)

        self.assertTrue(actual_return_value)

    def test_trigger__false_if_a_condition_is_not_met(self):
        raw_filter = {
            "kind": "kind",
            "conditions": [
                "[condition0==true]",
                "[condition1==true]"
            ],
            "message": {},
            "tests": []
        }

        raw_object = {
            "apiVersion": "123",
            "metadata": {
                "namespace": "namespace"
            },
            "condition0": "true",
            "condition1": "false"
        }

        f = Filter(raw_filter)

        actual_return_value = f.trigger(raw_object)

        self.assertFalse(actual_return_value)
