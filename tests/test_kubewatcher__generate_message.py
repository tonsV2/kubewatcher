from unittest import TestCase

from kubewatcher.kubewatcher import generate_message


class Test(TestCase):
    def test_generate_message(self):
        message_data = {
            "template": "Pod: {NAME} in {NAMESPACE} has restarted {RESTART_COUNT} times",
            "attributes": {
                "NAME": "metadata.name",
                "NAMESPACE": "metadata.namespace",
                "RESTART_COUNT": "status.containerStatuses[*].restartCount"
            }
        }

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

        actual_message = generate_message(message_data, raw_object)

        expected_message = "Pod: test-name in test-namespace has restarted 123 times"
        self.assertEqual(actual_message, expected_message)
