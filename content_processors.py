import datetime
from django.utils import timezone
from shop.models import CartItem


def current_date(request):
    return {'current_date': timezone.now().date()}

def cart_items(request):
    if request.user.is_authenticated:
        items = CartItem.objects.filter(user=request.user)
    else:
        items = CartItem.objects.none()

    total_cart = 0

    for item in items:
        if item.product:
            item.total = item.product.price * item.quantity
        elif item.honey:
            item.total = item.honey.price * item.quantity
        else:
            item.total = 0
        total_cart += item.total

    return {'items': items,
            'total_cart': total_cart
            }

