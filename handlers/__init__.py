import json
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from pprint import pprint

import requests
from ruamel import yaml

from config import config


def handle(message, raw_object):
    if config['handlers']['slack']:
        response = post_message_to_slack(message)
        if not response['ok']:
            pprint(response)

    if config['handlers']['smtp']:
        send_mail(message, raw_object)


# Inspiration: https://www.tutorialspoint.com/send-mail-from-your-gmail-account-using-python
def send_mail(message, raw_object):
    smtp_config = config['handlers']['smtp']
    mail_message = MIMEMultipart()
    mail_message['From'] = smtp_config['from']
    mail_message['To'] = smtp_config['to']
    mail_message['Subject'] = message

    body = yaml.safe_dump(raw_object)

    mail_message.attach(MIMEText(body, 'plain'))

    session = smtplib.SMTP(smtp_config['host'], smtp_config['port'])
    if smtp_config['tls']:
        session.starttls()
    session.login(smtp_config['from'], smtp_config['password'])
    text = mail_message.as_string()
    try:
        session.sendmail(smtp_config['from'], smtp_config['to'], text)
    except smtplib.SMTPAuthenticationError as exc:
        print(exc)
    session.quit()


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
