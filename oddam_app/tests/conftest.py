import pytest
from django.contrib.auth.models import User


@pytest.fixture()
def user_login():
    data = {
        'username': 'testowy',
        'password': 'test'
    }
    User.objects.create_user(**data)
    return data


@pytest.fixture()
def user():
    data = {
        'username': 'testowy',
        'password': 'test'
    }
    return User.objects.create_user(**data)
