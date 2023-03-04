"""Celery's task: send mail notification when an order 
is successfully created.
"""
from celery import shared_task
from django.conf import settings
from django.core.mail import send_mail
from .models import Order


@shared_task
def order_created(order_id: int) -> int:
    """
    Task to send an e-mail notification when an order is
    successfully created.

    :param order_id: Id of the current order.
    :type order_id: int
    :return: Send an e-mail notification when an order is
             successfully created.
    :rtype: int
    """
    order: Order = Order.objects.get(id=order_id)
    subject: str = f'Commande n°. {order.id}'
    message: str = f'Bonjour {order.first_name},\n\n' \
                   f'Votre commande a été réalisée avec succès.' \
                   f'Votre numéro de commande est {order.id}.'
    mail_sent = send_mail(subject,
                          message,
                          settings.EMAIL_HOST_USER,
                          [order.email])
    return mail_sent
