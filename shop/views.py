from django.shortcuts import render, redirect
from django.views import View

import honey
from honey.forms import HoneySearchForm
from honey.models import HoneyOffer, BeeProduct
from shop.forms import AddToCartHoneyForm, AddToCartBeeProductForm
from shop.models import CartItem




class ShopProductView(View):
    def get(self, request):
        form = HoneySearchForm(request.GET)
        honeys = HoneyOffer.objects.all().order_by('taste__taste')
        products = BeeProduct.objects.all()
        if form.is_valid():
            query = form.cleaned_data['query']
            if query:
                query_lower = query.lower()
                honeys = [
                    honey for honey in honeys if any(
                        query_lower in value.lower()
                        for value in [
                            honey.taste.taste,
                            honey.taste.get_taste_display(),
                            honey.type.type,
                            honey.type.get_type_display(),
                            honey.variant.variant,
                            honey.variant.get_variant_display(),
                        ]
                    )
                ]
                products = products.filter(name__icontains=query)


        return render(request, 'shop_products.html', {
            'honeys': honeys,
            'products': products,
            'form': form,
        })

class AddToCartHoneyView(View):
    def get(self, request, pk):
        honey = HoneyOffer.objects.get(pk=pk)
        form = AddToCartHoneyForm(initial={'quantity': 1}, available_quantity=honey.quantity)
        return render(request, 'add_to_cart_honey.html', {
            'honey': honey,
            'form': form
        })

    def post(self, request, pk):
        honey = HoneyOffer.objects.get(pk=pk)
        form = AddToCartHoneyForm(request.POST, available_quantity=honey.quantity)

        if form.is_valid():
            added_quantity = form.cleaned_data['quantity']
            cart_item = CartItem.objects.filter(
                user=request.user,
                honey__taste=honey.taste,
                honey__type=honey.type,
                honey__variant=honey.variant
            ).first()
            if cart_item:
                cart_item.quantity += added_quantity
                cart_item.save()
                honey.quantity -= added_quantity
                honey.save()
                return render(request, 'add_to_cart_honey.html', {
                    'honey': honey,
                    'form': form,
                    'message': 'Quantity updated!'
                })

            honey.quantity -= added_quantity
            honey.save()
            CartItem.objects.create(
                user=request.user,
                honey=honey,
                quantity=added_quantity,
                product=None
            )
            return redirect('cart')


class AddToCartProductView(View):
    def get(self, request, pk):
        product = BeeProduct.objects.get(pk=pk)
        form = AddToCartBeeProductForm(initial={'quantity': 1}, available_quantity=product.quantity)
        return render(request, 'add_to_cart_product.html', {
            'product': product,
            'form': form
        })

    def post(self, request, pk):
        product = BeeProduct.objects.get(pk=pk)
        form = AddToCartBeeProductForm(request.POST, available_quantity=product.quantity)
        if form.is_valid():
            added_quantity = form.cleaned_data['quantity']
            item = CartItem.objects.filter(user=request.user, product__name=product.name).first()
            if item:
                item.quantity += added_quantity
                item.save()
                product.quantity -= added_quantity
                product.save()
                return render(request, 'add_to_cart_honey.html', {
                    'product': product,
                    'form': form,
                    'message': 'Quantity updated!'
                })

            added_quantity = form.cleaned_data['quantity']
            product.quantity -= added_quantity
            product.save()
            CartItem.objects.create(
                user=request.user,
                product=product,
                quantity=added_quantity,
                honey=None
            )
            return redirect('cart')


class CartItemView(View):
    def get(self, request):
        return render(request, 'cart_item.html')



class UpdateCartItemQuantityView(View):
    def post(self, request, pk):
        item_in_cart = CartItem.objects.get(pk=pk, user=request.user)
        old_quantity = item_in_cart.quantity
        new_quantity = int(request.POST.get('quantity', 1))
        diff = new_quantity - old_quantity

        if new_quantity > 0:
            if item_in_cart.honey:
                available_quantity = item_in_cart.honey.quantity + old_quantity
                message = f'Not enough quantity in stock! You can add only  {available_quantity-old_quantity} more product(s) to cart!'
                if available_quantity - new_quantity < 0:
                    return render(request, 'cart_item.html', {
                        'item': item_in_cart,
                        'message': message
                    })
                item_in_cart.honey.quantity -= diff
                item_in_cart.honey.save()
            if item_in_cart.product:
                available_quantity = item_in_cart.product.quantity + old_quantity
                message = f'Not enough quantity in stock! You can add only  {available_quantity - old_quantity} more product(s) to cart!'
                if available_quantity - new_quantity < 0:
                    return render(request, 'cart_item.html', {
                        'item': item_in_cart,
                        'message': message
                    })
                item_in_cart.product.quantity -= diff
                item_in_cart.product.save()
            item_in_cart.quantity = new_quantity
            item_in_cart.save()
        else:
            if item_in_cart.honey:
                item_in_cart.honey.quantity += item_in_cart.quantity
                item_in_cart.honey.save()
            if item_in_cart.product:
                item_in_cart.product.quantity += item_in_cart.quantity
                item_in_cart.product.save()
            item_in_cart.delete()
        return redirect('cart')


class OrderSummaryView(View):
    def get(self, request):
        return render(request, 'order_summary.html')
















