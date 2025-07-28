import pytest
from django.contrib.auth.models import Permission
from django.test import Client
from django.urls import reverse
from honey.models import HoneyTaste, HoneyType, HoneyVariant, HoneyOffer
from shop.conftest import user

# Funkcja przyjmuje parametr client jako argument fixture, którą dostarcza pytest-django automatycznie.
# Nie wymaga żadnych dekoratorów ani tworzenia instancji klienta.
# Dla modeli nie obslugujacych zadnych zapytan do baz danych.

@pytest.mark.django_db
def test_honey_view(client):
    response = client.get('/')
    assert response.status_code == 200

@pytest.mark.django_db
def test_honeys_view(client):
    url = reverse('honeys')
    response = client.get(url)
    assert response.status_code == 200

#################################TASTE################################################################
@pytest.mark.django_db
def test_honey_taste_view(client, user):
    permission = Permission.objects.get(codename='add_honeytaste')
    user.user_permissions.add(permission)
    client.force_login(user)
    url = reverse('honey_taste')
    response = client.get(url)
    assert response.status_code == 200
    assert '<form' in response.content.decode()

@pytest.mark.django_db
def test_add_honey_taste_view_post_success(client, user):
    permission = Permission.objects.get(codename='add_honeytaste')
    user.user_permissions.add(permission)
    client.force_login(user)
    url = reverse('honey_taste')
    data = {'taste': 'Akacja'}
    response = client.post(url, data)
    assert response.status_code == 200
    assert HoneyTaste.objects.filter(taste='Akacja').exists()

@pytest.mark.django_db
def test_add_honey_taste_view_duplicate(client, user):
    permission = Permission.objects.get(codename='add_honeytaste')
    user.user_permissions.add(permission)
    client.force_login(user)
    url = reverse('honey_taste')
    HoneyTaste.objects.create(taste='Akacja')  # tworzymy smak Akacja w testowej bazie danych
    data = {'taste': 'Akacja'}
    response = client.post(url, data)  # próbujemy dodać drugi raz Akację przez formularz
    assert response.status_code == 200
    assert 'Taste already exists ' in response.content.decode()
    assert HoneyTaste.objects.filter(taste='Akacja').count() == 1

#########################TYPE##########################################################################
@pytest.mark.django_db
def test_honey_type_view(client, user):
    permission = Permission.objects.get(codename='add_honeytype')
    user.user_permissions.add(permission)
    client.force_login(user)
    url = reverse('honey_type')
    response = client.get(url)
    assert response.status_code == 200
    assert '<form' in response.content.decode()

@pytest.mark.django_db
def test_add_honey_type_view_post_success(client, user):
    permission = Permission.objects.get(codename='add_honeytype')
    user.user_permissions.add(permission)
    client.force_login(user)
    url = reverse('honey_type')
    data = {'type': 'kremowany'}
    response = client.post(url, data)
    assert response.status_code == 200
    assert HoneyType.objects.filter(type='kremowany').exists()

@pytest.mark.django_db
def test_add_honey_type_view_duplicate(client, user):
    permission = Permission.objects.get(codename='add_honeytype')
    user.user_permissions.add(permission)
    client.force_login(user)
    url = reverse('honey_type')
    HoneyType.objects.create(type='kremowany')
    data = {'type': 'kremowany'}
    response = client.post(url, data)
    assert response.status_code == 200
    assert 'Type already exists' in response.content.decode()
    assert HoneyType.objects.filter(type='kremowany').count() == 1


###############################VARIANT###########################################################
@pytest.mark.django_db
def test_honey_variant_view(client, user):
    permission = Permission.objects.get(codename='add_honeyvariant')
    user.user_permissions.add(permission)
    client.force_login(user)
    url = reverse('honey_variant')
    response = client.get(url)
    assert response.status_code == 200
    assert '<form' in response.content.decode()

@pytest.mark.django_db
def test_add_honey_variant_view_post_success(client, user):
    permission = Permission.objects.get(codename='add_honeyvariant')
    user.user_permissions.add(permission)
    client.force_login(user)
    url = reverse('honey_variant')
    data = {'variant': '50'}
    response = client.post(url, data)
    assert response.status_code == 200
    assert HoneyVariant.objects.filter(variant='50').exists()

@pytest.mark.django_db
def test_add_honey_variant_view_duplicate(client, user):
    permission = Permission.objects.get(codename='add_honeyvariant')
    user.user_permissions.add(permission)
    client.force_login(user)
    url = reverse('honey_variant')
    HoneyVariant.objects.create(variant='50')
    data = {'variant': '50'}
    response = client.post(url, data)
    assert response.status_code == 200
    assert 'Variant already exists' in response.content.decode()
    assert HoneyVariant.objects.filter(variant='50').count() == 1

###################################OFFER############################################################

@pytest.mark.django_db
def test_honey_offer_view(client, user):
    permission = Permission.objects.get(codename='add_honeyoffer')
    user.user_permissions.add(permission)
    client.force_login(user)
    url = reverse('honey_offer')
    response = client.get(url)
    assert response.status_code == 200
    assert '<form' in response.content.decode()

@pytest.mark.django_db
def test_honey_offer_view_post_success(client, user, taste, honey_type, variant):
    permission = Permission.objects.get(codename='add_honeyoffer')
    user.user_permissions.add(permission)
    client.force_login(user)
    url = reverse('honey_offer')
    data = {
        'taste': taste[0].pk,
        'type': honey_type[0].pk,
        'variant': variant[0].pk,
        'price': 100,
        'quantity': 100
    }
    response = client.post(url, data)
    assert response.status_code == 200
    assert HoneyOffer.objects.filter(
        taste=taste[0].pk,
        type=honey_type[0].pk,
        variant=variant[0].pk).exists()

@pytest.mark.django_db
def test_add_honey_offer_view_duplicate(client, taste, honey_type, variant, user):
    permission = Permission.objects.get(codename='add_honeyoffer')
    user.user_permissions.add(permission)
    client.force_login(user)
    url = reverse('honey_offer')
    HoneyOffer.objects.create(taste=taste[0], type=honey_type[0],variant=variant[0])
    data = {
        'taste': taste[0].pk,
        'type': honey_type[0].pk,
        'variant': variant[0].pk,
        'price': 100,
        'quantity': 100
    }
    response = client.post(url, data)
    assert response.status_code == 200
    assert 'Offer already exists' in response.content.decode()
    assert HoneyOffer.objects.filter(taste=taste[0].pk, type=honey_type[0].pk, variant=variant[0].pk).count() == 1


####################################LIST###############################################################

@pytest.mark.django_db
def test_honey_list_view_status_code(client):
    url = reverse('honey_list')
    response = client.get(url)
    assert response.status_code == 200

@pytest.mark.django_db
def test_honey_list_view_contains_table(client):
    url = reverse('honey_list')
    response = client.get(url)
    assert '<table' in response.content.decode()

@pytest.mark.django_db
def test_honey_list_view_contains_form(client):
    url = reverse('honey_list')
    response = client.get(url)
    assert '<form' in response.content.decode()

@pytest.mark.django_db
def test_honey_list_view_search_results(client, offer):
    url = reverse('honey_list')
    offer[0].taste.taste = 'Akacja'
    offer[0].taste.save()
    data = {'query': 'AKA'}
    response = client.get(url, data)
    print(response.content.decode())

    assert '<td>Akacjowy</td>' in response.content.decode()

@pytest.mark.django_db
def test_honey_list_view_empty_message(client):
    url = reverse('honey_list')
    data = {'query': 'czekolada'}
    response = client.get(url, data)
    assert 'Brak miodów w bazie' in response.content.decode()




##############################UPDATE#######################################################################

@pytest.mark.django_db
def test_honey_update_offer_view(client, offer, user):
    permission = Permission.objects.get(codename='add_honeyoffer')
    user.user_permissions.add(permission)
    client.force_login(user)
    url = reverse('update_offer', kwargs={'pk': offer[0].pk})
    response = client.get(url)
    assert response.status_code == 200

@pytest.mark.django_db
def test_honey_update_offer_form_contains_view(client, offer):
    url = reverse('update_offer', kwargs={'pk': offer[0].pk})
    response = client.get(url)
    assert '<form' in response.content.decode()

@pytest.mark.django_db
def test_honey_update_offer_view_correct_offer(client, offer, user):
    permission = Permission.objects.get(codename='change_honeyoffer')
    user.user_permissions.add(permission)
    client.force_login(user)
    selected_offer = offer[0]
    url = reverse('update_offer', kwargs={'pk': selected_offer.pk})
    response = client.get(url)
    assert selected_offer.taste.taste in response.content.decode()
    assert selected_offer.type.type in response.content.decode()
    assert selected_offer.variant.variant in response.content.decode()


@pytest.mark.django_db
def test_honey_update_offer_view_post_success(client, offer, user):
    permission = Permission.objects.get(codename='change_honeyoffer')
    user.user_permissions.add(permission)
    client.force_login(user)
    url = reverse('update_offer', kwargs={'pk': offer[0].pk})
    data = {
        'price': 200,
        'quantity': 200
    }
    response = client.post(url, data)
    assert response.status_code == 200
    assert HoneyOffer.objects.filter(pk=offer[0].pk, price=200, quantity=200).exists()

@pytest.mark.django_db
def test_honey_update_offer_view_form_validation(client, offer, user):
    permission = Permission.objects.get(codename='change_honeyoffer')
    user.user_permissions.add(permission)
    client.force_login(user)
    url = reverse('update_offer', kwargs={'pk': offer[0].pk})
    data = {
        'price': '',
        'quantity':''
    }
    response = client.post(url, data)
    print(response.content.decode())
    assert response.status_code == 200
    assert 'class="error' in response.content.decode()



##########################DELETE################################################################################

@pytest.mark.django_db
def test_honey_delete_offer_view(client, offer, user):
    permission = Permission.objects.get(codename='delete_honeyoffer')
    user.user_permissions.add(permission)
    client.force_login(user)
    url = reverse('delete_offer', kwargs={'pk': offer[0].pk})
    response = client.get(url)
    assert response.status_code == 200

@pytest.mark.django_db
def test_honey_delete_offer_view_correct_offer(client, offer, user):
    permission = Permission.objects.get(codename='delete_honeyoffer')
    user.user_permissions.add(permission)
    client.force_login(user)
    selected_offer = offer[0]
    url = reverse('delete_offer', kwargs={'pk': selected_offer.pk})
    response = client.get(url)
    print(response.content.decode())
    assert selected_offer.taste.taste in response.content.decode()
    assert selected_offer.type.type in response.content.decode()
    assert selected_offer.variant.variant in response.content.decode()

@pytest.mark.django_db
def test_honey_delete_offer_view_post_success(client, offer, user):
    permission = Permission.objects.get(codename='delete_honeyoffer')
    user.user_permissions.add(permission)
    client.force_login(user)
    selected_offer = offer[0]
    url = reverse('delete_offer', kwargs={'pk': selected_offer.pk})
    response = client.post(url)
    assert response.status_code == 302
    assert not HoneyOffer.objects.filter(pk=selected_offer.pk).exists()

@pytest.mark.django_db
def test_honey_delete_offer_view_message_contains(client, offer, user):
    permission = Permission.objects.get(codename='delete_honeyoffer')
    user.user_permissions.add(permission)
    client.force_login(user)
    url = reverse('delete_offer', kwargs={'pk': offer[0].pk})
    response = client.get(url)
    assert 'Be careful, you are going to delete this offer !' in response.content.decode()












