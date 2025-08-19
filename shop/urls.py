from django.urls import path

from shop.views import CartItemView, ShopProductView, AddToCartHoneyView, AddToCartProductView, \
    UpdateCartItemQuantityView, OrderSummaryView, SendOrderView

urlpatterns = [
    path('cart/', CartItemView.as_view(), name='cart'),
    path('shop_products/', ShopProductView.as_view(), name='shop_products' ),
    path('add_to_cart_honey/<int:pk>/', AddToCartHoneyView.as_view(), name='add_to_cart_honey'),
    path('add_to_cart_product/<int:pk>/', AddToCartProductView.as_view(), name='add_to_cart_product'),

    path('cart/update_quantity/<int:pk>/', UpdateCartItemQuantityView.as_view(), name='update_cart_item_quantity'),
    path('order_summary/', OrderSummaryView.as_view(),name='order_summary'),
    path('send_order/', SendOrderView.as_view(), name='send_order')
]