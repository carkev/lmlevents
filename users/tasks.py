"""Celery's task: send mail notification when an order is
successfully created.
"""
from celery import shared_task
from django.conf import settings
from django.core.mail import send_mail
from .models import UserProfile


@shared_task
def account_created(account_id: int) -> int:
    """
    Task to send an e-mail notification when an account is
    successfully created.

    :param account_id: Id of the current account.
    :type account_id: int
    :return: Send an e-mail notification when an account is
             successfully created.
    :rtype: int
    """
    account: UserProfile = UserProfile.objects.get(id=account_id)
    subject: str = 'Confirmation de mail'
    message: str = \
        f'Bonjour {account.select_related("first_name").get(account.user)},' \
        f'\n\nVotre compte a été créé avec succès.\nA très vite !'
    mail_sent = send_mail(subject,
                          message,
                          settings.EMAIL_HOST_USER,
                          [account.select_related('email').get(account.user)])
    return mail_sent
