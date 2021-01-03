from unittest import TestCase
from unittest.mock import patch

from kubewatcher.handlers import post_message_to_telegram


class Test(TestCase):
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
