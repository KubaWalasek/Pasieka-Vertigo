from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.mail import send_mail
from django.shortcuts import render, redirect
import stripe
from django.conf import settings
from django.http import JsonResponse, HttpResponse
from django.views import View
from django.views.decorators.csrf import csrf_exempt

from honey.forms import HoneySearchForm
from honey.models import HoneyOffer, BeeProduct
from shop.forms import AddToCartHoneyForm, AddToCartBeeProductForm, OrderDataForm
from shop.models import CartItem, Order, OrderItem






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



class DeleteCartItemView(View):
    def post(selfself, request, pk):
        item_in_cart = CartItem.objects.get(pk=pk, user=request.user)
        old_quantity = item_in_cart.quantity
        if item_in_cart.honey:
            item_in_cart.honey.quantity += old_quantity
            item_in_cart.honey.save()
        if item_in_cart.product:
            item_in_cart.product.quantity += old_quantity
            item_in_cart.product.save()
        item_in_cart.delete()
        return redirect('cart')


class OrderSummaryView(View):
    def get(self, request):
        return render(request, 'order_summary.html')

class SendOrderView(View):
    def get(self, request):
        user = request.user
        user_profile = user.userprofile
        initial_data = {
            'first_name': user_profile.first_name or '',
            'last_name': user_profile.last_name or '',
            'email': user.email,
            'post_code': user_profile.post_code or '',
            'city': user_profile.city or '',
            'street': user_profile.street or '',
            'street_number': user_profile.street_number or '',
            'door_number': user_profile.door_number or '',
            'phone_number': user_profile.phone_number or '',
        }
        form = OrderDataForm(initial=initial_data)

        return render(request, 'order_data.html', {
            'form': form,
            'user_profile': user_profile,
            'user': user,
        })

    def post(self, request):
        user = request.user
        form = OrderDataForm(request.POST)
        items_queryset = CartItem.objects.select_related('product', 'honey').filter(user=user)
        items_in_cart = list(items_queryset)
        total_in_cart_price = 0
        total_line_price = 0

        for cart_item in items_in_cart:
            if cart_item.honey:
                price = cart_item.honey.price
                total_line_price = price * cart_item.quantity
                total_in_cart_price += cart_item.honey.price * cart_item.quantity
            elif cart_item.product:
                price = cart_item.product.price
                total_line_price = price * cart_item.quantity
                total_in_cart_price += cart_item.product.price * cart_item.quantity
            cart_item.total_price = total_line_price

        if form.is_valid():
            order = Order.objects.create(
                user = user,
                email = form.cleaned_data['email'],
                first_name = form.cleaned_data['first_name'],
                last_name = form.cleaned_data['last_name'],
                post_code = form.cleaned_data['post_code'],
                city = form.cleaned_data['city'],
                street = form.cleaned_data['street'],
                street_number = form.cleaned_data['street_number'],
                door_number = form.cleaned_data['door_number'],
                phone_number = form.cleaned_data['phone_number']         ,
                paid = False,
                total_price = total_in_cart_price,
            )

            for cart_item in items_in_cart:
                product = cart_item.product
                honey = cart_item.honey
                if cart_item.honey:
                    product_name = honey.taste.taste
                    price = honey.price
                elif cart_item.product:
                    product_name = product.name
                    price = product.price
                else:
                    continue
                quantity = cart_item.quantity
                OrderItem.objects.create(
                    order = order,
                    product_name = product_name,
                    price = price,
                    quantity = quantity
                )
            CartItem.objects.filter(user=user).delete()

            return redirect( 'order_finished', pk=order.id)


stripe.api_key = settings.STRIPE_SECRET_KEY

class OrderFinishedView(LoginRequiredMixin, View):
    def get(self, request, pk):
        order = Order.objects.get(pk=pk)
        order_items = OrderItem.objects.filter(order=order)

        return render(request, 'order_finished.html', {
            'order': order,
            'order_items': order_items,
            'STRIPE_PUBLISHABLE_KEY': settings.STRIPE_PUBLISHABLE_KEY
        })



class StripeCheckoutSessionView(View):
    def post(self, request, pk):
        order = Order.objects.get(pk=pk)
        line_items = []
        line_items.append({
            'price_data': {
                'currency': 'pln',
                'product_data': {
                    'name': 'Zamówienie z pasieki VERTIGO',
                },
                'unit_amount': int(order.total_price * 100),  # zamiana zł na grosze
            },
            'quantity': 1,
        })
        checkout_session = stripe.checkout.Session.create(
            payment_method_types=['blik'],
            line_items=line_items,
            mode='payment',
            success_url=request.build_absolute_uri(f'/shop/order_finished/{order.id}/'),
            cancel_url=request.build_absolute_uri(f'/shop/order_finished/{order.id}/'),
            customer_email=order.email
        )
        # Zapisz sobie session_id do zamówienia (może się przydać):
        order.stripe_session_id = checkout_session.id
        order.save()
        return redirect(checkout_session.url)





@csrf_exempt
def stripe_webhook_view(request):
    endpoint_secret = settings.STRIPE_WEBHOOK_SECRET

    payload = request.body
    sig_header = request.META.get('HTTP_STRIPE_SIGNATURE', '')

    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, endpoint_secret
        )
    except ValueError:
        return HttpResponse(status=400)
    except stripe.error.SignatureVerificationError:
        return HttpResponse(status=400)

    if event['type'] == 'checkout.session.completed':
        session = event['data']['object']
        session_id = session.get('id')
        from shop.models import Order
        try:
            order = Order.objects.get(stripe_session_id=session_id)
            order.paid = True
            order.save()

            # Wysyłka maila do klienta po opłaceniu zamówienia
            subject = "Potwierdzenie opłacenia zamówienia"
            message = (
                f"Cześć {order.first_name},\n\n"
                f"Twoje zamówienie nr {order.id} zostało opłacone.\n"
                "Dziękujemy za zakupy w Pasiece Vertigo!"
            )
            recipient = [order.email]
            send_mail(subject, message, None, recipient)

        except Order.DoesNotExist:
            pass

    return HttpResponse(status=200)
























