from celery import shared_task
from django.conf import settings
from django.core.mail import send_mail
from .models import Order


@shared_task
def order_created(order_id):
    """
    Task to send an e-mail notification when an order is
    successfully created.
    """
    order = Order.objects.get(id=order_id)
    print("order", order.email)
    subject = f'Commande n°. {order.id}'
    message = f'Bonjour {order.first_name},\n\n' \
              f'Votre commande a été réalisée avec succès.' \
              f'Votre numéro de commande est {order.id}.'
    mail_sent = send_mail(subject,
                          message,
                          settings.EMAIL_HOST_USER,
                          [order.email])
    return mail_sent
