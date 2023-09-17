from email.message import EmailMessage

import pytest
from pytest_mock import MockerFixture

from app.services.email_service import EmailService


@pytest.fixture(scope="function")
def service() -> EmailService:
    return EmailService("stmp.fake.host", 465)


@pytest.mark.email
def test_email_create_message(service: EmailService, mocker: MockerFixture):
    msg = service.create_message(
        "Test Content", "fakeuser@email.com", "Test Subject", "fakeuser@email.com"
    )
    expected_msg = EmailMessage()
    expected_msg.set_content("Test Content")
    expected_msg["Subject"] = "Test Subject"
    expected_msg["From"] = "fakeuser@email.com"
    expected_msg["To"] = "fakeuser@email.com"

    assert isinstance(msg, EmailMessage)
    assert expected_msg["Subject"] == msg["Subject"]
    assert expected_msg["From"] == msg["From"]
    assert expected_msg["To"] == msg["To"]
    assert expected_msg.get_content() == msg.get_content()


@pytest.mark.email
def test_send_email(service: EmailService, mocker: MockerFixture) -> None:
    mocked_ssl = mocker.patch("smtplib.SMTP_SSL")
    msg = EmailMessage()
    service.send_email(msg)
    mocked_ssl.assert_called_once_with(service.SMTP_HOST, service.SMTP_PORT)
    mocked_ssl.return_value.__enter__.return_value.login.assert_called_with(
        service.SMTP_USER, service.SMTP_PASSWORD
    )
    mocked_ssl.return_value.__enter__.return_value.send_message.assert_called_with(msg)
