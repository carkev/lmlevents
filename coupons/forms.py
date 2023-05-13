"""Coupons forms module.
"""
from django import forms


class CouponApplyForm(forms.Form):
    """Form class to apply coupon.
    """
    code = forms.CharField()
