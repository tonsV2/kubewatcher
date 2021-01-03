from unittest import TestCase
from unittest.mock import patch

from kubewatcher.handlers import post_message_to_slack


class Test(TestCase):
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
