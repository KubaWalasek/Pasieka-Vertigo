import pytest
from shop.conftest import user
from django.contrib.auth.models import User
from django.urls import reverse

from shop.models import UserProfile


@pytest.mark.django_db
def test_register_view(client):
    url = reverse('register')
    response = client.get(url)
    assert response.status_code == 200
    assert '<form' in response.content.decode()


#################################   REGISTER VIEW TESTS ################################################################


@pytest.mark.django_db
def test_register_view_post_success(client):
    url = reverse('register')
    data = {'username': 'testuser',
            'password_1': 'testpassword',
            'password_2': 'testpassword',
            'email': 'email@email.com'}
    response = client.post(url, data)
    assert response.status_code == 302
    assert User.objects.filter(username='testuser').exists()
    assert UserProfile.objects.filter(user__username='testuser').exists()

@pytest.mark.django_db
def test_register_view_post_fail_username(client):
    url = reverse('register')
    user = User.objects.create_user(username='testuser', email='emial@email.com', password='testpassword')
    data = {'username': 'testuser',
            'password_1': 'testpassword',
            'password_2': 'testpassword',
            'email': 'email@email.com'
    }
    response = client.post(url, data)
    print(response.content.decode())
    assert response.status_code == 200
    assert "Użytkownik o tej nazwie już istnieje" in response.content.decode()

@pytest.mark.django_db
def test_register_view_post_fail_email(client):
    url = reverse('register')
    user = User.objects.create_user(username='testuser', email='email@email.com', password='testpassword')
    data = {'username': 'testuser1',
            'password_1': 'testpassword',
            'password_2': 'testpassword',
            'email': 'email@email.com'
    }
    response = client.post(url, data)
    print(response.content.decode())
    assert response.status_code == 200
    assert 'Użytkownik z tym adresem e-mail już istnieje' in response.content.decode()


#################################   LOGIN VIEW TESTS ################################################################


@pytest.mark.django_db
def test_loginView_get(client):
    url = reverse('login')
    response = client.get(url)
    assert response.status_code == 200
    assert '<form' in response.content.decode()

@pytest.mark.django_db
def test_login_view_post_success(client, user):
    url = reverse('login')
    data ={'username': 'testuser',
           'password': 'testpassword'}
    response = client.post(url, data)
    assert response.status_code == 302
    assert response.url == reverse('home')

@pytest.mark.django_db
def test_login_view_post_fail(client, user):
    url = reverse('login')
    data ={'username': 'testuser',
           'password': 'testpasswordd'}
    response = client.post(url, data)
    assert 'Invalid username or password' in response.content.decode()

@pytest.mark.django_db
def test_logout_view(client, user):
    client.force_login(user)
    url = reverse('logout')
    response = client.get(url)
    assert response.status_code == 302
    assert response.url == reverse('home')























