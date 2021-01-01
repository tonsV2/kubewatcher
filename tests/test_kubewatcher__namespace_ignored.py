from unittest import TestCase

from kubewatcher.kubewatcher import namespace_ignored


class Test(TestCase):
    def test_namespace_ignored__return_true_if_namespace_is_ignored(self):
        namespace = "namespace"

        namespaces = {
            "ignore": ["namespace"]
        }

        actual_return_value = namespace_ignored(namespace, namespaces)

        self.assertTrue(actual_return_value)

    def test_namespace_ignored__return_false_if_namespace_is_not_ignored(self):
        namespace = "namespace"

        namespaces = {
            "ignore": []
        }

        actual_return_value = namespace_ignored(namespace, namespaces)

        self.assertFalse(actual_return_value)

    def test_namespace_ignored__return_false_if_ignored_is_not_specified(self):
        namespace = "namespace"

        namespaces = {}

        actual_return_value = namespace_ignored(namespace, namespaces)

        self.assertFalse(actual_return_value)
