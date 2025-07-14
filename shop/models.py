import honey
from django.db import models



class CartItem(models.Model):
    product = models.ForeignKey('honey.BeeProduct', on_delete=models.CASCADE)
    honey = models.ForeignKey('honey.HoneyOffer', on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)