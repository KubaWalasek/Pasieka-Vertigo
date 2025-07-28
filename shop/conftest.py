import pytest
from django.contrib.auth.models import User

from honey.conftest import offer, taste, honey_type, variant
from honey.models import BeeProduct

@pytest.fixture
def product():
    lst = []
    for i in range(1,11):
        bee_product = BeeProduct.objects.create(
            name=f'Product {i}',
            price=i*10,
            quantity=i*100)
        lst.append(bee_product)
    return lst


@pytest.fixture
def user():
    return User.objects.create_user(username='testuser', password='testpassword')



