import asyncio
import functools
import json
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

import requests
from ruamel import yaml

from kubewatcher.config import config


# Inspiration: https://stackoverflow.com/questions/41063331/how-to-use-asyncio-with-existing-blocking-library
def run_in_executor(f):
    @functools.wraps(f)
    def inner(*args, **kwargs):
        loop = asyncio.new_event_loop()
        return loop.run_in_executor(None, functools.partial(f, *args, **kwargs))

    return inner


@run_in_executor
def handle(message, raw_object):
    if 'handlers' in config:
        if config['handlers']['slack']:
            response = post_message_to_slack(message)
            if response['ok']:
                print(f"Slack {config['handlers']['slack']['channel']}: {message}")
            else:
                print(f"Slack error: {yaml.safe_dump(response)}")

        if config['handlers']['smtp']:
            send_mail(message, raw_object)
    else:
        print("WARNING: No handlers configured!")


# Inspiration: https://www.tutorialspoint.com/send-mail-from-your-gmail-account-using-python
def send_mail(message, raw_object):
    smtp_config = config['handlers']['smtp']

    session = smtplib.SMTP(smtp_config['host'], smtp_config['port'])
    if smtp_config['tls']:
        session.starttls()
    session.login(smtp_config['from'], smtp_config['password'])

    for to in smtp_config['to']:
        mail = MIMEMultipart()
        mail['From'] = smtp_config['from']
        mail['To'] = to
        mail['Subject'] = message

        body = yaml.safe_dump(raw_object)

        mail.attach(MIMEText(body, 'plain'))

        try:
            session.sendmail(smtp_config['from'], to, mail.as_string())
            print(f"SMTP {to}: {message}")
        except smtplib.SMTPException as exc:
            print("SMTPException:")
            print(exc)

        session.quit()


# Inspiration: https://keestalkstech.com/2019/10/simple-python-code-to-send-message-to-slack-channel-without-packages/
def post_message_to_slack(text, blocks=None):
    slack = config['handlers']['slack']
    return requests.post('https://slack.com/api/chat.postMessage', {
        'token': slack['token'],
        'channel': slack['channel'],
        'text': text,
        'icon_url': slack['icon'],
        'username': slack['username'],
        'blocks': json.dumps(blocks) if blocks else None
    }).json()
