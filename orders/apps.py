"""Order application management.
"""
from django.apps import AppConfig


class OrdersConfig(AppConfig):
    """Class to config orders.
    """
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'orders'
