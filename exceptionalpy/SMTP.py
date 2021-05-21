from smtplib import SMTP_SSL as SMTP
from email.mime.text import MIMEText

from exceptionalpy import BaseNotifier, Handler


class SMTPNotifier(BaseNotifier):
    def __init__(self, host: str, port: int, sender: str, username: str, password: str, destinations: list[str],
                 subject: str):
        BaseNotifier.__init__(self)
        self.sender = sender
        self.username = username
        self.password = password
        self.destinations = destinations
        self.subject = subject

        self._client = SMTP(host, port)
        self._client.login(self.username, self.password)

    def send(self, message: list[str]):
        msg = '\n'.join(message)
        msg = MIMEText(msg, "plain")
        msg["Subject"] = self.subject
        msg["From"] = self.sender
        self._client.sendmail(self.sender, self.destinations, msg.as_string())


class SMTPHandler(Handler):
    def __init__(self, address: tuple, credentials: tuple, sender: str, destinations: list[str], subject: str,
                 init: bool = True):
        Handler.__init__(self, init)
        self._notifier = SMTPNotifier(address[0], address[1], sender, credentials[0], credentials[1], destinations,
                                      subject)
