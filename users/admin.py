"""App add to admin panel.
"""
from django.contrib import admin
from . models import UserProfile, UserToken


# DOCS - https://docs.djangoproject.com/en/3.1/ref/contrib/admin/
class UserProfileAdmin(admin.ModelAdmin):
    """Class to add UserProfile to admin panel.
    """
    list_display = ('id', 'user', 'timestamp')


class UserTokenAdmin(admin.ModelAdmin):
    """Class to add TokenAdmin to admin panel.
    """
    list_display = ('id', 'user', 'timestamp')


admin.site.register(UserToken, UserTokenAdmin)
admin.site.register(UserProfile, UserProfileAdmin)
