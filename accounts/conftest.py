import pytest
from django.contrib.auth.models import User

from shop.models import UserProfile
from shop.conftest import user

@pytest.fixture
def userprofile(user):
    return UserProfile.objects.create(
        user=user,
        first_name='testname',
        last_name='testlastname',
        post_code='12345',
        city='testcity',
        street='teststreet',
        street_number='123',
        door_number='456',
        phone_number='1234567890'
    )
