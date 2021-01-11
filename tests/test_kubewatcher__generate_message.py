from unittest import TestCase

from kubewatcher.filter import Filter


class Test(TestCase):
    def test_generate_message(self):
        message_data = {
            "template": "Pod: {NAME} in {NAMESPACE} has restarted {RESTART_COUNT} times",
            "attributes": {
                "NAME": "metadata.name",
                "NAMESPACE": "metadata.namespace",
                "RESTART_COUNT": "status.containerStatuses.*.restartCount"
            }
        }

        f = Filter({"kind": "kind", "conditions": [], "message": message_data, "tests": []})

        raw_object = {
            "metadata": {
                "name": "test-name",
                "namespace": "test-namespace",
            },
            "status": {
                "containerStatuses": [
                    {
                        "restartCount": "123"
                    }
                ]
            }
        }

        actual_message = f.generate_message(raw_object)

        expected_message = "Pod: test-name in test-namespace has restarted 123 times"
        self.assertEqual(expected_message, actual_message)
