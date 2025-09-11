from django.conf import settings
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator
from django.db import models



class CartItem(models.Model):
    product = models.ForeignKey('honey.BeeProduct', on_delete=models.CASCADE, null=True, blank=True)
    honey = models.ForeignKey('honey.HoneyOffer', on_delete=models.CASCADE, null=True, blank=True)
    quantity = models.PositiveIntegerField(default=1)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, default=1)


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=20, blank=True, null=True)
    last_name = models.CharField(max_length=20, blank=True, null=True)
    post_code = models.CharField(max_length=10, blank=True, null=True)
    city = models.CharField(max_length=30, blank=True, null=True)
    street = models.CharField(max_length=30, blank=True, null=True)
    street_number = models.CharField(max_length=10, blank=True, null=True)
    door_number = models.CharField(max_length=10, blank=True, null=True)
    phone_number = models.CharField(max_length=15, blank=True, null=True)

    def __str__(self):
        return self.user.username

class Order(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True)
    first_name = models.CharField(max_length=20)
    last_name = models.CharField(max_length=20)
    email = models.EmailField()
    post_code = models.CharField(max_length=10)
    city = models.CharField(max_length=30)
    street = models.CharField(max_length=30)
    street_number = models.CharField(max_length=10)
    door_number = models.CharField(max_length=10, blank=True, null=True)
    phone_number = models.CharField(max_length=15)
    created = models.DateTimeField(auto_now_add=True)
    paid = models.BooleanField(default=False)
    stripe_session_id = models.CharField(max_length=255, blank=True, null=True)  # ID sesji Stripe
    total_price = models.DecimalField(max_digits=8, decimal_places=2, default=0.00)

class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE)
    product_name = models.CharField(max_length=128)
    quantity = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=7, decimal_places=2)

    @property
    def total_line_price(self):
        return self.price * self.quantity



