"""Allows cart to be calling in templates.
"""
from .cart import Cart


def cart(request):
    """Return the cart.
    """
    return {'cart': Cart(request)}
