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
        if 'log' in config['handlers']:
            log(message)

        if 'slack' in config['handlers']:
            post_message_to_slack(config, message)

        if 'smtp' in config['handlers']:
            send_mail(config, message, raw_object)

        if 'telegram' in config['handlers']:
            post_message_to_telegram(config, message)
    else:
        logging.info("WARNING: No handlers configured!")


def log(message):
    logging.info(f"Handler:Log: {message}")


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
def post_message_to_slack(config, message, blocks=None):
    default_icon = "https://github.com/tonsV2/kubewatcher/raw/master/icons/icon.png"
    default_username = "KubeWatcher"

    slack = config['handlers']['slack']
    response = requests.post('https://slack.com/api/chat.postMessage', {
        'token': slack['token'],
        'channel': slack['channel'],
        'text': message,
        'icon_url': slack['icon'] if 'icon' in slack else default_icon,
        'username': slack['username'] if 'username' in slack else default_username,
        'blocks': json.dumps(blocks) if blocks else None
    }).json()

    if response['ok']:
        logging.info(f"Handler:Slack {config['handlers']['slack']['channel']}: {message}")
    else:
        logging.info(f"Handler:Slack error: {yaml.safe_dump(response)}")


# Inspiration: https://medium.com/@ManHay_Hong/how-to-create-a-telegram-bot-and-send-messages-with-python-4cf314d9fa3e
def post_message_to_telegram(config, message):
    telegram = config['handlers']['telegram']

    token = telegram['token']
    chat_id = telegram['chatId']

    url = f"https://api.telegram.org/bot{token}/sendMessage?chat_id={chat_id}&parse_mode=Markdown&text={message}"
    response = requests.get(url).json()

    if response['ok']:
        logging.info(f"Handler:Telegram: {message}")
    else:
        logging.info(f"Handler:Telegram error: {yaml.safe_dump(response)}")
