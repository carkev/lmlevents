"""App config module.
"""
from django.apps import AppConfig


class CartConfig(AppConfig):
    """Class to add Cart to admin panel.
    """
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'cart'
