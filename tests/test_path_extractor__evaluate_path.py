from unittest import TestCase

from kubewatcher.path_extractor import evaluate_path


class Test(TestCase):
    def test_evaluate_path__simple_property_less_than(self):
        data = {
            "property": "1"
        }

        path = "[property < 2]"

        actual_value = evaluate_path(data, path)

        self.assertTrue(actual_value)

    def test_evaluate_path__simple_property_grater_than(self):
        data = {
            "property": "1"
        }

        path = "[property > 0]"

        actual_value = evaluate_path(data, path)

        self.assertTrue(actual_value)

    def test_evaluate_path__simple_property_equals(self):
        data = {
            "property": "value"
        }

        path = "[property == value]"

        actual_value = evaluate_path(data, path)

        self.assertTrue(actual_value)

    def test_evaluate_path__simple_property_not_equals(self):
        data = {
            "property": "value"
        }

        path = "[property != nope]"

        actual_value = evaluate_path(data, path)

        self.assertTrue(actual_value)

    def test_evaluate_path__simple_property_no_match(self):
        data = {
            "property": "value"
        }

        path = "[property == nope]"

        actual_value = evaluate_path(data, path)

        self.assertFalse(actual_value)

    def test_evaluate_path__nested_property(self):
        data = {
            "property": {
                "property": "value"
            }
        }

        path = "property[property == value]"

        actual_value = evaluate_path(data, path)

        self.assertTrue(actual_value)

    def test_evaluate_path__multiple_values_first_match(self):
        data = {
            "property": [
                {"state": "value0"},
                {"state": "value1"}
            ]
        }

        path = "property[state == value0]"

        actual_value = evaluate_path(data, path)

        self.assertTrue(actual_value)

    def test_evaluate_path__multiple_values_second_match(self):
        data = {
            "property": [
                {"state": "value0"},
                {"state": "value1"}
            ]
        }

        path = "property[state == value1]"

        actual_value = evaluate_path(data, path)

        self.assertTrue(actual_value)

    def test_evaluate_path__multiple_nested_values_first_match(self):
        data = {
            "property": [
                {
                    "property": {
                        "state": "value0"
                    }
                },
                {
                    "property": {
                        "state": "value1"
                    }
                },
            ]
        }

        path = "property.*.property[state == value0]"

        actual_value = evaluate_path(data, path)

        self.assertTrue(actual_value)

    def test_evaluate_path__multiple_nested_values_second_match(self):
        data = {
            "property": [
                {
                    "property": {
                        "state": "value0"
                    }
                },
                {
                    "property": {
                        "state": "value1"
                    }
                },
            ]
        }

        path = "property.*.property[state == value1]"

        actual_value = evaluate_path(data, path)

        self.assertTrue(actual_value)
