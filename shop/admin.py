from django.contrib import admin

from shop.models import CartItem, OrderItem, Order, UserProfile

admin.site.register(CartItem)
admin.site.register(UserProfile)
admin.site.register(Order)
admin.site.register(OrderItem)
