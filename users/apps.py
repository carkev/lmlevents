"""App config module.
"""
from django.apps import AppConfig


class UsersConfig(AppConfig):
    """Class to set this app.
    """
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'users'
