"""Users model.
"""
from django.db import models
from django.contrib.auth.models import User
from .choices import COUNTRIES


class UserProfile(models.Model):
    '''Our UserProfile model extends the built-in Django User Model.
    '''
    updated = models.DateTimeField(auto_now=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    telephone = models.CharField(max_length=15, null=True, blank=True)
    address = models.CharField(verbose_name="Addresse", max_length=100,
                               null=True, blank=True)
    town = models.CharField(verbose_name="Ville", max_length=100,
                            null=True, blank=True)
    county = models.CharField(verbose_name="Région", max_length=100,
                              null=True, blank=True)
    post_code = models.CharField(verbose_name="Code Postale", max_length=8,
                                 null=True, blank=True)
    country = models.CharField(verbose_name="Pays", max_length=100,
                               null=True, blank=True, choices=COUNTRIES)
    is_active = models.BooleanField(default=True)

    email_verified = models.BooleanField(default=False)
    two_step_active = models.BooleanField(default=True)

    def __str__(self):
        return f'{self.user}'


class UserToken(models.Model):
    '''Our UserToken model is used to store verification tokens generated
    by users.
    '''
    updated = models.DateTimeField(auto_now=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    token = models.CharField(max_length=100, null=True, blank=True)
    two_step_code = models.CharField(max_length=6, null=True, blank=True)
    # Used to change the object type
    is_email = models.BooleanField(default=False)
    is_password = models.BooleanField(default=False)
    is_sms = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f'{self.user}'
