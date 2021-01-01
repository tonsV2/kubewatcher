import asyncio
import functools
import json
import logging
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

import requests
from ruamel import yaml


# Inspiration: https://stackoverflow.com/questions/41063331/how-to-use-asyncio-with-existing-blocking-library
def run_in_executor(f):
    @functools.wraps(f)
    def inner(*args, **kwargs):
        loop = asyncio.new_event_loop()
        return loop.run_in_executor(None, functools.partial(f, *args, **kwargs))

    return inner


@run_in_executor
def handle(config, message, raw_object):
    if 'handlers' in config:
        if 'slack' in config['handlers']:
            post_message_to_slack(config, message)

        if 'smtp' in config['handlers']:
            send_mail(config, message, raw_object)
    else:
        logging.info("WARNING: No handlers configured!")


# Inspiration: https://www.tutorialspoint.com/send-mail-from-your-gmail-account-using-python
def send_mail(config, message, raw_object):
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
            logging.info(f"Handler:SMTP {to}: {message}")
        except smtplib.SMTPException as exc:
            logging.error("SMTPException:")
            logging.error(exc)

        session.quit()


# Inspiration: https://keestalkstech.com/2019/10/simple-python-code-to-send-message-to-slack-channel-without-packages/
def post_message_to_slack(config, text, blocks=None):
    default_icon = "https://github.com/tonsV2/kubewatcher/raw/master/icons/icon.png"
    default_username = "KubeWatcher"

    slack = config['handlers']['slack']
    response = requests.post('https://slack.com/api/chat.postMessage', {
        'token': slack['token'],
        'channel': slack['channel'],
        'text': text,
        'icon_url': slack['icon'] if 'icon' in slack else default_icon,
        'username': slack['username'] if 'username' in slack else default_username,
        'blocks': json.dumps(blocks) if blocks else None
    }).json()

    if response['ok']:
        logging.info(f"Handler:Slack {config['handlers']['slack']['channel']}: {text}")
    else:
        logging.info(f"Handler:Slack error: {yaml.safe_dump(response)}")
