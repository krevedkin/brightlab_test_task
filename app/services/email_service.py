import smtplib
from email.message import EmailMessage

from app.config import settings


class EmailService:
    def __init__(
        self,
        SMTP_HOST: str = settings.SMTP_HOST,
        SMTP_PORT: int = settings.SMTP_PORT,
        SMTP_USER: str = settings.SMTP_USER,
        SMTP_PASSWORD: str = settings.SMTP_PASSWORD,
    ) -> None:
        self.SMTP_HOST = SMTP_HOST
        self.SMTP_PORT = SMTP_PORT
        self.SMTP_USER = SMTP_USER
        self.SMTP_PASSWORD = SMTP_PASSWORD

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
            server.login(self.SMTP_USER, self.SMTP_PASSWORD)
            server.send_message(message)
