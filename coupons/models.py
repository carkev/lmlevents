"""Model of the coupons app.
"""
from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator


class Coupon(models.Model):
    """Model of a Coupon.
    """
    code = models.CharField(max_length=50,
                            unique=True)
    valid_from = models.DateTimeField()
    valid_to = models.DateTimeField()
    discount = models.IntegerField(
                   validators=[MinValueValidator(0),
                               MaxValueValidator(100)],
                   help_text='Pourcentage de remise (0 à 100)')
    active = models.BooleanField()

    def __str__(self):
        return str(self.code)
