from django.shortcuts import render, redirect
from django.views import View
from honey.models import HoneyOffer
from shop.models import BeeProduct, CartItem


class CartItemView(View):
    def get(self, request):
        return render()