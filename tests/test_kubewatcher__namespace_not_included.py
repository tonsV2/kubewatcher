from unittest import TestCase

from kubewatcher.kubewatcher import namespace_not_included


class Test(TestCase):
    def test_namespace_not_included__return_false_if_namespace_is_included(self):
        namespace = "namespace"

        namespaces = {
            "include": ["namespace"]
        }

        actual_return_value = namespace_not_included(namespace, namespaces)

        self.assertFalse(actual_return_value)

    def test_namespace_not_included__return_true_if_namespace_is_not_included(self):
        namespace = "namespace"

        namespaces = {
            "include": []
        }

        actual_return_value = namespace_not_included(namespace, namespaces)

        self.assertTrue(actual_return_value)

    def test_namespace_not_included__return_false_if_include_is_not_specified(self):
        namespace = "namespace"

        namespaces = {}

        actual_return_value = namespace_not_included(namespace, namespaces)

        self.assertFalse(actual_return_value)
