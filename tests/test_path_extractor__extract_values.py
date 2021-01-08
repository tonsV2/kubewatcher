from unittest import TestCase

from kubewatcher.path_extractor import extract_values


class Test(TestCase):
    def test_extract_values__simple_property(self):
        data = {
            "property": "value"
        }

        path = "property"

        actual_value = extract_values(data, path)
        self.assertEqual(["value"], actual_value)

    def test_extract_values__nested_property(self):
        data = {
            "property": {
                "property": "value"
            }
        }

        path = "property.property"

        actual_value = extract_values(data, path)

        self.assertEqual(["value"], actual_value)

    def test_extract_values__multiple_values(self):
        data = {
            "property": [
                {"state": "value0"},
                {"state": "value1"}
            ]
        }

        path = "property.*.state"

        actual_value = extract_values(data, path)

        self.assertEqual(["value0", "value1"], actual_value)

    def test_extract_values__multiple_nested_values(self):
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

        path = "property.*.property.state"

        actual_value = extract_values(data, path)

        self.assertEqual(["value0", "value1"], actual_value)
