import pytest
from pytest_django.asserts import assertTemplateUsed, assertContains
from django.urls import reverse
from django.contrib.auth.models import User

"""
base
"""


@pytest.mark.django_db
def test_base(client):
    url = reverse('base')
    response = client.get(url)
    assert response.status_code == 200


@pytest.mark.django_db
def test_base_template(client):
    url = reverse('base')
    response = client.get(url)
    assertTemplateUsed(response, 'index.html')
    assertContains(response, 'Fundacji')


"""
login view
"""


def test_login_view_get(client):
    url = reverse('login')
    response = client.get(url)
    assert response.status_code == 200


@pytest.mark.django_db
def test_login_view_post(client, user_login):
    url = reverse('login')
    response = client.post(url, user_login)
    assert response.status_code == 302
    assert response.url == reverse('base')


@pytest.mark.django_db
def test_login_view_post_next(client, user_login):
    url = reverse('login')
    url += "?next=" + reverse('form')
    response = client.post(url, user_login)
    assert response.status_code == 302
    assert response.url == reverse('base')


"""
logout
"""


@pytest.mark.django_db
def test_logout_view_get(client, user):
    url = reverse('logout')
    client.force_login(user)
    response = client.get(url)
    client.logout()
    assert response.status_code == 302
    assert response.url.startswith(reverse('base'))


"""
register view
"""


def test_register_view_get(client):
    url = reverse('register')
    response = client.get(url)
    assert response.status_code == 200


@pytest.mark.django_db
def test_register_view_post(client):
    url = reverse('register')
    new_user = {
        'username': 'testu',
        'password': 'testp',
        're_password': 'testp'
    }
    response = client.post(url, new_user)
    assert response.status_code == 302
    assert response.url.startswith(reverse('login'))
    assert User.objects.get(username=new_user['username'])
