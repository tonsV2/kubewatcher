import time
from unittest import TestCase
from unittest.mock import patch

from kubewatcher.handlers import handle, post_message_to_telegram


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

    @patch("requests.get")
    def test_handle__post_message_to_telegram(self, get_mock):
        token = "token"
        chat_id = "chat-id"

        config = {
            "handlers": {
                "telegram": {
                    "token": token,
                    "chatId": chat_id
                }
            }
        }

        message = "message"

        post_message_to_telegram(config, message)

        url = f"https://api.telegram.org/bot{token}/sendMessage?chat_id={chat_id}&parse_mode=Markdown&text={message}"
        get_mock.assert_called_with(url)
