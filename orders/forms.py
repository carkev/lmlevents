"""Order forms module.
"""
from django import forms
from .models import Order


class OrderCreateForm(forms.ModelForm):
    """Class to create order form creation.
    """
    class Meta:
        """Change the class behaviour.
        """
        model = Order
        fields = ['first_name', 'last_name', 'email', 'address',
                  'postal_code', 'city']
