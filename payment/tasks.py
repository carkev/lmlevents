from io import BytesIO
from celery import shared_task
import weasyprint
from django.conf import settings
from django.template.loader import render_to_string
from django.core.mail import EmailMessage
from orders.models import Order


@shared_task
def payment_completed(order_id):
    """
    Task to send an e-mail notification when an order is
    successfully paid.
    """
    order = Order.objects.get(id=order_id)
    # create invoice e-mail
    subject = f'LML Events - Facture n°. {order.id}'
    message = 'Veuillez trouver ci-joint la facture de votre achat.'
    email = EmailMessage(subject,
                         message,
                         settings.EMAIL_HOST_USER,
                         [order.email])
    # generate PDF
    html = render_to_string('order_pdf.html', {'order': order})
    out = BytesIO()
    stylesheets=[weasyprint.CSS(settings.STATIC_ROOT / 'css/pdf.css')]
    weasyprint.HTML(string=html).write_pdf(out,
                                          stylesheets=stylesheets)
    # attach PDF file
    email.attach(f'order_{order.id}.pdf',
                 out.getvalue(),
                 'application/pdf')
    # send e-mail
    email.send()
