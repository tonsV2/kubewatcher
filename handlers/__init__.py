import json
from pprint import pprint

import requests

from config import config


def handle(message, raw_object):
    if config['handlers']['slack']:
        response = post_message_to_slack(message)
        if not response['ok']:
            pprint(response)


# Inspiration: https://keestalkstech.com/2019/10/simple-python-code-to-send-message-to-slack-channel-without-packages/
def post_message_to_slack(text, blocks=None):
    slack = config['handlers']['slack']
    return requests.post('https://slack.com/api/chat.postMessage', {
        'token': slack['token'],
        'channel': slack['channel'],
        'text': text,
        #        'icon_url': slack_icon_url,
        'username': "slack_user_name",
        'blocks': json.dumps(blocks) if blocks else None
    }).json()
