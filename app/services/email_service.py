import smtplib
from email.message import EmailMessage

from app.config import settings


class EmailService:
    def __init__(
        self,
        SMTP_HOST: str = settings.SMTP_HOST,
        SMTP_PORT: int = settings.SMTP_PORT,
    ) -> None:
        self.SMTP_HOST = SMTP_HOST
        self.SMTP_PORT = SMTP_PORT

    def create_message(
        self, content: str, to: str, subject: str, from_: str = settings.SMTP_USER
    ) -> EmailMessage:
        message = EmailMessage()
        message.set_content(content)
        message["Subject"] = subject
        message["From"] = from_
        message["To"] = to

        return message

    def send_email(self, message: EmailMessage):
        with smtplib.SMTP_SSL(self.SMTP_HOST, self.SMTP_PORT) as server:
            server.login(settings.SMTP_USER, settings.SMTP_PASSWORD)
            server.send_message(message)
