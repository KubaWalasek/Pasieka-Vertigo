from django.conf import settings
from django.core.validators import MinValueValidator
from django.db import models



class CartItem(models.Model):
    product = models.ForeignKey('honey.BeeProduct', on_delete=models.CASCADE, null=True, blank=True)
    honey = models.ForeignKey('honey.HoneyOffer', on_delete=models.CASCADE, null=True, blank=True)
    quantity = models.PositiveIntegerField(default=1)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, default=1)


