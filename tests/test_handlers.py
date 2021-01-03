import time
from unittest import TestCase
from unittest.mock import patch

from kubewatcher.handlers import handle


class Test(TestCase):
    @patch("kubewatcher.handlers.post_message_to_slack")
    @patch("kubewatcher.handlers.send_mail")
    @patch("kubewatcher.handlers.post_message_to_telegram")
    def test_handle__ensure_handlers_are_called(self, post_message_to_slack_mock, send_mail_mock,
                                                post_message_to_telegram_mock):
        config = {
            "handlers": {
                "slack": {},
                "smtp": {},
                "telegram": {},
            }
        }

        handle(config, "", {})
        time.sleep(1)

        post_message_to_slack_mock.assert_called()
        send_mail_mock.assert_called()
        post_message_to_telegram_mock.assert_called()

    @patch("kubewatcher.handlers.post_message_to_slack")
    @patch("kubewatcher.handlers.send_mail")
    @patch("kubewatcher.handlers.post_message_to_telegram")
    def test_handle__ensure_handlers_are_not_called(self, post_message_to_slack_mock, send_mail_mock,
                                                    post_message_to_telegram_mock):
        config = {
        }

        handle(config, "", {})
        time.sleep(1)

        post_message_to_slack_mock.assert_not_called()
        send_mail_mock.assert_not_called()
        post_message_to_telegram_mock.assert_not_called()
