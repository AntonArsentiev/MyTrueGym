import os
from constants import *
from celery import shared_task
from twilio.rest import Client
from smtplib import SMTPException
from mytruegym.settings import DEBUG
from django.core.mail import EmailMessage
from django.utils.translation import ugettext_lazy
from twilio.base.exceptions import TwilioException

@shared_task
def send_celery_mail(email_to):
    try:
        email = EmailMessage(
            ugettext_lazy("Подтверждение почтового адреса"),
            ugettext_lazy("<p>Для подтверждения почтового адреса перейдите по ссылке "
            "<a href=\"{}://{}/account/settings/email\">Перейдите тут</a></p>").format(
                "http" if DEBUG else "https",
                "127.0.0.1:8000" if DEBUG else "www.mytruegym.ru"
            ),
            os.environ.get(EMAIL_HOST_USER_VALUE),
            [email_to]
        )
        email.content_subtype = "html"
        email.send(fail_silently=False)
    except SMTPException as exp:
        print(exp)


@shared_task
def send_code_to_activate_phone_number(phone_number):
    if DEBUG:
        return
    account_sid = os.environ.get(TWILIO_ACCOUNT_SID)
    auth_token = os.environ.get(TWILIO_AUTH_TOKEN)
    service_token = os.environ.get(TWILIO_SERVICE_TOKEN)
    client = Client(account_sid, auth_token)
    try:
        client.verify.services(service_token).verifications.create(to=phone_number, channel="sms")
    except TwilioException as exp:
        print(exp)


def send_code_to_verify_phone_number(phone_number, code):
    if DEBUG:
        return True if code == "123456" else False
    else:
        account_sid = os.environ.get(TWILIO_ACCOUNT_SID)
        auth_token = os.environ.get(TWILIO_AUTH_TOKEN)
        service_token = os.environ.get(TWILIO_SERVICE_TOKEN)
        client = Client(account_sid, auth_token)
        verified = client.verify.services(service_token).verification_checks.create(to=phone_number, code=code)
        return verified.valid
