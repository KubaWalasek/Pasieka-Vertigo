import pytest
from django.contrib.auth.models import User, Permission
from django.contrib.contenttypes.models import ContentType

from honey.models import HoneyTaste, HoneyType, HoneyVariant, HoneyOffer

@pytest.fixture
def taste():
    lst = []
    for i in range(1, 11):
        taste = HoneyTaste.objects.create(taste=f'Taste {i}')
        lst.append(taste)
    return lst

@pytest.fixture
def honey_type():
    lst = []
    for i in range(1, 11):
        honey_type = HoneyType.objects.create(type=f'Type {i}')
        lst.append(honey_type)
    return lst

@pytest.fixture
def variant():
    lst = []
    for i in range(1, 11):
        variant = HoneyVariant.objects.create(variant=f'Variant {i}')
        lst.append(variant)
    return lst

@pytest.fixture
def offer(taste, honey_type, variant):
    lst = []
    for i in range(10):
        offer = HoneyOffer.objects.create(
            taste=taste[i],
            type=honey_type[i],
            variant=variant[i],
            price=(i+1)*10,
            quantity=(i+1)*100)
        lst.append(offer)
    return lst