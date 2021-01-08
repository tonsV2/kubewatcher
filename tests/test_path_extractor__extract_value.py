from unittest import TestCase

from kubewatcher.path_extractor import extract_value, MultipleValuesException


class Test(TestCase):
    def test_extract_value__simple_property(self):
        data = {
            "property": "value"
        }

        path = "property"

        actual_value = extract_value(data, path)

        self.assertEqual("value", actual_value)

    def test_extract_value__nested_property(self):
        data = {
            "property": {
                "property": "value"
            }
        }

        path = "property.property"

        actual_value = extract_value(data, path)

        self.assertEqual("value", actual_value)

    def test_extract_value__multiple_values_exception(self):
        data = {
            "property": [
                {"state": "value0"},
                {"state": "value1"}
            ]
        }

        path = "property.*.state"

        self.assertRaises(MultipleValuesException, extract_value, data, path)
