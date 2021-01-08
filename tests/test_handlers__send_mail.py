from unittest import TestCase
from unittest.mock import patch, Mock

from kubewatcher.handlers import send_mail


class Test(TestCase):
    @patch("smtplib.SMTP")
    def test_handle__send_mail(self, smtp):
        mock_session = Mock()
        smtp.return_value = mock_session

        from_ = "from"
        password = "password"
        host = "host"
        port = 587
        tls = True
        to = ["to"]

        config = {
            "handlers": {
                "smtp": {
                    "from": from_,
                    "password": password,
                    "host": host,
                    "port": port,
                    "tls": tls,
                    "to": to
                }
            }
        }

        message = "message"

        raw_object = {}

        send_mail(config, message, raw_object)

        smtp.assert_called_once_with(host, port)
        mock_session.starttls.assert_called_once()
        mock_session.login.assert_called_once_with(from_, password)
        mock_session.sendmail.assert_called()
        mock_session.quit.assert_called_once()

    @patch("smtplib.SMTP")
    def test_handle__send_mail_multiple_recipients(self, smtp):
        mock_session = Mock()
        smtp.return_value = mock_session

        from_ = "from"
        password = "password"
        host = "host"
        port = 587
        tls = True
        tos = ["to0", "to1"]

        config = {
            "handlers": {
                "smtp": {
                    "from": from_,
                    "password": password,
                    "host": host,
                    "port": port,
                    "tls": tls,
                    "to": tos
                }
            }
        }

        message = "message"

        raw_object = {}

        send_mail(config, message, raw_object)

        smtp.assert_called_once_with(host, port)
        mock_session.starttls.assert_called_once()
        mock_session.login.assert_called_once_with(from_, password)
        mock_session.sendmail.assert_called()
        self.assertEqual(2, mock_session.sendmail.call_count)
        mock_session.quit.assert_called_once()

    @patch("smtplib.SMTP")
    def test_handle__send_mail_no_tls(self, smtp):
        mock_session = Mock()
        smtp.return_value = mock_session

        from_ = "from"
        password = "password"
        host = "host"
        port = 587
        tls = False
        to = ["to"]

        config = {
            "handlers": {
                "smtp": {
                    "from": from_,
                    "password": password,
                    "host": host,
                    "port": port,
                    "tls": tls,
                    "to": to
                }
            }
        }

        message = "message"

        raw_object = {}

        send_mail(config, message, raw_object)

        smtp.assert_called_once_with(host, port)
        mock_session.starttls.assert_not_called()
        mock_session.login.assert_called_once_with(from_, password)
        mock_session.sendmail.assert_called()
        mock_session.quit.assert_called_once()
