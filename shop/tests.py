import pytest
from django.urls import reverse
from shop.models import CartItem


@pytest.mark.django_db
def test_shop_product_view(client):
    url = reverse('shop_products')
    response = client.get(url)
    assert response.status_code == 200
    assert '<table' in response.content.decode()
    assert '<form' in response.content.decode()

@pytest.mark.django_db
def test_shop_honey_view_search_results(client, offer):
    url = reverse('shop_products')
    offer[0].taste.taste = 'Akacjowy'
    offer[0].taste.save()
    data = {'query': 'AKA'}
    response = client.get(url, data)
    print(response.content.decode())
    assert '<td>Aka' in response.content.decode()

@pytest.mark.django_db
def test_shop_product_view_search_results(client, product):
    url = reverse('shop_products')
    product[0].name = 'Pyłek pszczeli'
    product[0].save()
    data = {'query': 'py'}
    response = client.get(url, data)
    print(response.content.decode())
    assert '<td>Pyłek' in response.content.decode()

@pytest.mark.django_db
def test_login_required_view(client, user, product, offer):
    url = reverse('shop_products')
    client.force_login(user)
    response = client.get(url)
    print(response.content.decode())
    assert '<button>DODAJ DO KOSZYKA' in response.content.decode()
    assert 'testuser' in response.content.decode()

@pytest.mark.django_db
def test_add_to_cart_honey_view(client, offer):
    url = reverse('add_to_cart_honey', kwargs={'pk': offer[0].pk})
    response = client.get(url)
    assert response.status_code == 200

@pytest.mark.django_db
def test_add_to_cart_product_view(client, product):
    url = reverse('add_to_cart_product', kwargs={'pk': product[0].pk})
    response = client.get(url)
    assert response.status_code == 200


@pytest.mark.django_db
def test_add_to_cart_honey_view_post_success_and_check_cart(client, offer, user):
    client.force_login(user)
    add_to_cart_url = reverse('add_to_cart_honey', kwargs={'pk': offer[0].pk})
    data = {'quantity': 10}
    response = client.post(add_to_cart_url, data)
    assert response.status_code == 302
    assert CartItem.objects.get(user=user, honey=offer[0]).quantity == 10

    cart_url = reverse('cart')
    response = client.get(cart_url)
    assert response.status_code == 200
    assert 'PODSUMOWANIE' in response.content.decode()
    assert '10' in response.content.decode()
    assert offer[0].taste.taste in response.content.decode()
    assert offer[0].type.type in response.content.decode()
    assert offer[0].variant.variant in response.content.decode()
    assert 'testuser' in response.content.decode()


@pytest.mark.django_db
def test_add_to_cart_product_view_post_success_and_check_cart(client, product, user):
    client.force_login(user)
    add_to_cart_url = reverse('add_to_cart_product', kwargs={'pk': product[0].pk})
    data = {'quantity': 10}
    response = client.post(add_to_cart_url, data)
    assert response.status_code == 302
    assert CartItem.objects.get(user=user, product=product[0]).quantity == 10

    cart_url = reverse('cart')
    response = client.get(cart_url)
    assert response.status_code == 200
    assert 'PODSUMOWANIE' in response.content.decode()
    assert '10' in response.content.decode()
    assert product[0].name in response.content.decode()
    assert 'testuser' in response.content.decode()


@pytest.mark.django_db
def test_add_to_cart_honey_view_update_quantity_post_success(client, offer, user):
    client.force_login(user)
    CartItem.objects.create(user=user, honey=offer[0], quantity=10)
    url = reverse('add_to_cart_honey', kwargs={'pk': offer[0].pk})
    data = {'quantity': 10}
    response = client.post(url, data)
    print(response.content.decode())
    assert response.status_code == 200
    assert CartItem.objects.get(user=user, honey=offer[0]).quantity == 20
    assert 'Quantity updated' in response.content.decode()


@pytest.mark.django_db
def test_add_to_cart_product_view_update_quantity_post_success(client, product, user):
    client.force_login(user)
    CartItem.objects.create(user=user, product=product[0], quantity=10)
    url = reverse('add_to_cart_product', kwargs={'pk': product[0].pk})
    data = {'quantity': 10}
    response = client.post(url, data)
    print(response.content.decode())
    assert response.status_code == 200
    assert CartItem.objects.get(user=user, product=product[0]).quantity == 20
    assert 'Quantity updated' in response.content.decode()


@pytest.mark.django_db
def test_cart_item_view(client):
    url = reverse('cart')
    response = client.get(url)
    assert response.status_code == 200
    assert '<strong>Zaloguj się' in response.content.decode()


@pytest.mark.django_db
def test_cart_item_view_login_empty(client, user):
    client.force_login(user)
    url = reverse('cart')
    response = client.get(url)
    assert response.status_code ==200
    assert 'Brak produktów w koszyku' in response.content.decode()

@pytest.mark.django_db
def test_cart_item_view_login_not_empty(client, user, offer):
    client.force_login(user)
    CartItem.objects.create(user=user, honey=offer[0], quantity=10)
    url = reverse('cart')
    response = client.get(url)
    print(response.content.decode())
    assert response.status_code ==200
    assert 'value="10"' in response.content.decode()


@pytest.mark.django_db
def test_cart_item_view_update_quantity_post_success_honey(client, user, offer):
    client.force_login(user)
    cart_item = CartItem.objects.create(user=user, honey=offer[0], quantity=10)
    url = reverse('update_cart_item_quantity', kwargs={'pk': cart_item.pk})
    data = {'quantity': 20}
    response = client.post(url, data)
    assert response.status_code == 302
    assert CartItem.objects.get(user=user, honey=offer[0]).quantity == 20


@pytest.mark.django_db
def test_cart_item_view_update_quantity_post_delete_honey(client, user, offer):
    client.force_login(user)
    cart_item = CartItem.objects.create(user=user, honey=offer[0], quantity=10)
    url = reverse('update_cart_item_quantity', kwargs={'pk': cart_item.pk})
    data = {'quantity': 0}
    response = client.post(url, data)
    assert response.status_code == 302
    assert not CartItem.objects.filter(user=user, honey=offer[0]).exists()


@pytest.mark.django_db
def test_cart_item_view_update_quantity_post_success_product(client, user, product):
    client.force_login(user)
    cart_item = CartItem.objects.create(user=user, product=product[0], quantity=10)
    url = reverse('update_cart_item_quantity', kwargs={'pk': cart_item.pk})
    data = {'quantity': 20}
    response = client.post(url, data)
    assert response.status_code == 302
    assert CartItem.objects.get(user=user, product=product[0]).quantity == 20


@pytest.mark.django_db
def test_cart_item_view_update_quantity_post_delete_product(client, user, product):
    client.force_login(user)
    cart_item = CartItem.objects.create(user=user, product=product[0], quantity=10)
    url = reverse('update_cart_item_quantity', kwargs={'pk': cart_item.pk})
    data = {'quantity': 0}
    response = client.post(url, data)
    assert response.status_code == 302
    assert not CartItem.objects.filter(user=user, product=product[0]).exists()


@pytest.mark.django_db
def test_cart_item_view_update_quantity_too_many_honeys(client, user, offer):
    client.force_login(user)
    offer[0].quantity = 100
    offer[0].save()
    cart_item = CartItem.objects.create(user=user, honey=offer[0], quantity=20)
    url = reverse('update_cart_item_quantity', kwargs={'pk': cart_item.pk})
    data = {'quantity': 210}
    response = client.post(url, data)
    print(response.content.decode())
    assert 'Not enough quantity' in response.content.decode()


@pytest.mark.django_db
def test_cart_item_view_update_quantity_too_many_products(client, user, product):
    client.force_login(user)
    product[0].quantity = 100
    product[0].save()
    cart_item = CartItem.objects.create(user=user, product=product[0], quantity=20)
    url = reverse('update_cart_item_quantity', kwargs={'pk': cart_item.pk})
    data = {'quantity': 210}
    response = client.post(url, data)
    print(response.content.decode())
    assert 'Not enough quantity' in response.content.decode()

























