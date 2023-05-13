"""Payment settings module.
"""
from django.apps import AppConfig


class PaymentConfig(AppConfig):
    """Class to config payment.
    """
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'payment'
