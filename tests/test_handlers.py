import time
from unittest import TestCase
from unittest.mock import patch

from kubewatcher.handlers import handle, post_message_to_telegram, post_message_to_slack


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

    @patch("requests.post")
    def test_handle__post_message_to_slack_using_defaults(self, post_mock):
        default_icon = "https://github.com/tonsV2/kubewatcher/raw/master/icons/icon.png"
        default_username = "KubeWatcher"

        token = "token"
        channel = "channel"
        config = {
            "handlers": {
                "slack": {
                    "token": token,
                    "channel": channel
                }
            }
        }

        message = "message"

        post_message_to_slack(config, message)

        url = 'https://slack.com/api/chat.postMessage'
        parameters = {
            'token': config['handlers']['slack']['token'],
            'channel': config['handlers']['slack']['channel'],
            'text': message,
            'icon_url': default_icon,
            'username': default_username,
            'blocks': None
        }

        post_mock.assert_called_with(url, parameters)

    @patch("requests.post")
    def test_handle__post_message_to_slack(self, post_mock):
        custom_icon = "icon"
        custom_username = "username"

        token = "token"
        channel = "channel"
        config = {
            "handlers": {
                "slack": {
                    "token": token,
                    "channel": channel,
                    "icon": custom_icon,
                    "username": custom_username
                }
            }
        }

        message = "message"

        post_message_to_slack(config, message)

        url = 'https://slack.com/api/chat.postMessage'
        parameters = {
            'token': config['handlers']['slack']['token'],
            'channel': config['handlers']['slack']['channel'],
            'text': message,
            'icon_url': custom_icon,
            'username': custom_username,
            'blocks': None
        }

        post_mock.assert_called_with(url, parameters)
