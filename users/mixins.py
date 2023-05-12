"""Mixins module.
"""
import string
import random
from urllib.parse import urlencode
from django.conf import settings
from django.shortcuts import redirect
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.core.mail import EmailMultiAlternatives, get_connection
from django.template.loader import render_to_string
from django.utils.html import strip_tags

import six
import phonenumbers
import pycountry
from twilio.rest import Client as TwilioClient
from users.models import UserToken


def form_errors(*args):
    '''Handles form error that are passed back to AJAX calls
    '''
    message = ""
    for form in args:

        if form.errors:
            message = form.errors.as_text()

    return message


def redirect_params(**kwargs):
    '''Used to append url parameters when redirecting users
    '''
    url = kwargs.get("url")
    params = kwargs.get("params")
    response = redirect(url)

    if params:
        query_string = urlencode(params)
        response['Location'] += '?' + query_string + "/"

    return response


# DOCS - https://docs.djangoproject.com/en/3.1/topics/auth/default/
class TokenGenerator(PasswordResetTokenGenerator):
    '''Creates a token that is used for email and password verification
    emails.
    '''

    def _make_hash_value(self, user, timestamp):
        return (
            six.text_type(user.pk)
            + six.text_type(timestamp)
            + six.text_type(user.is_active))


# DOCS - https://docs.djangoproject.com/en/3.1/topics/email/
class CreateEmail:
    '''Used to send emails from a Gmail account with an app password.
    '''

    def __init__(self, request, *args, **kwargs):
        self.email_account = kwargs.get("email_account")
        self.subject = kwargs.get("subject", "")
        self.email = kwargs.get("email")
        self.template = kwargs.get("template")
        self.context = kwargs.get("context")
        self.cc_email = kwargs.get("cc_email")
        self.token = kwargs.get("token")
        self.url_safe = kwargs.get("url_safe")
        domain = settings.CURRENT_SITE
        context = {
            "user": request.user,
            "domain": domain,
            }

        if self.token:
            context["token"] = self.token

        if self.url_safe:
            context["url_safe"] = self.url_safe

        email_accounts = {
            "donotreply": {
                'name': settings.EMAIL_HOST_USER,
                'password': settings.DONOT_REPLY_EMAIL_PASSWORD,
                'from': settings.EMAIL_HOST_USER,
                'display_name': settings.DISPLAY_NAME},
            }
        # render with dynamic value
        html_content = render_to_string(self.template, context)
        # Strip the html tag. So people can see the pure text at least.
        text_content = strip_tags(html_content)

        with get_connection(
                host=settings.EMAIL_HOST,
                port=settings.EMAIL_PORT,
                username=email_accounts[self.email_account]["name"],
                password=email_accounts[self.email_account]["password"],
                use_tls=settings.EMAIL_USE_TLS
                ) as connection:
            msg = EmailMultiAlternatives(
                    self.subject,
                    text_content,
                    f'{email_accounts[self.email_account]["display_name"]} '
                    f'<{email_accounts[self.email_account]["from"]}>',
                    [self.email],
                    cc=[self.cc_email],
                    connection=connection)
            msg.attach_alternative(html_content, "text/html")
            msg.send()


class CreateSMS:
    '''Used to send sms from a Twilio account
    '''

    def __init__(self, **kwargs):
        self.number = kwargs.get("number")
        self.message = kwargs.get("message")
        # Get API variables
        sid = settings.TWILIO_SID
        token = settings.TWILIO_TOKEN
        twilio_number = settings.TWILIIO_TEL
        # Create client
        client = TwilioClient(sid, token)
        # Create message
        client.messages.create(
            body=self.message,
            from_=twilio_number,
            to=self.number)


class ActivateTwoStep:
    '''Creates and sends a 6 digit code that is used for sms verification
    '''

    def __init__(self, **kwargs):
        self.user = kwargs.get("user")
        self.token = kwargs.get("token")
        # Create two step code
        size = 6
        chars = string.digits
        code = ''.join(random.choice(chars) for _ in range(size))
        # Create a usertoken object to store code
        user_token = UserToken.objects.create(
            user=self.user,
            token=self.token,
            two_step_code=code,
            is_sms=True)
        # User phonenumbers & pycountry libaries to convert telephone
        # number into a useable format for Twilio
        country_code = pycountry.countries.get(
            name=self.user.userprofile.country).alpha_2
        number_object = phonenumbers.parse(self.user.userprofile.telephone,
                                           country_code)
        telephone = (f'+{number_object.country_code}'
                     f'{number_object.national_number}')
        send_sms = CreateSMS(
            number=telephone,
            message=f'Votre code d\'authentification est : {code}')
