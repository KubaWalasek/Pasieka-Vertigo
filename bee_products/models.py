from django.db import models

class BeeProduct(models.Model):
    BEE_PRODUCTS_CHOICES = [
        ('Wosk', 'Wosk pszczeli - 100g'),
        ('Propolis', 'Propolis 60% - 50ml'),
        ('Pierzga', 'Pierzga - 300g'),
        ('Pyłek', 'Pyłek pszczeli - 500g')
    ]
    name = models.CharField(max_length=20, choices=BEE_PRODUCTS_CHOICES)
    price = models.DecimalField(max_digits=3, decimal_places=2)
    quantity = models.IntegerField(default=1)

# Create your models here.
