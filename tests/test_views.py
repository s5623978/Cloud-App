import pytest
from unittest.mock import patch, MagicMock
from django.http import HttpRequest
from django.contrib import messages
from gamestore.frontend.views import landing, store, checkout


@patch('gamestore.frontend.views.auth.verify_id_token')
@patch('gamestore.frontend.views.login_user')
@patch('gamestore.frontend.views.render')
def test_landing_get_with_user(mock_render, mock_login, mock_verify):
    request = HttpRequest()
    request.session = {'user': 'data'}

    with patch('gamestore.frontend.views.redirect') as mock_redirect:
        landing(request)
        mock_redirect.assert_called_once_with('/store/')


@patch('gamestore.frontend.views.auth.verify_id_token')
@patch('gamestore.frontend.views.login_user')
@patch('gamestore.frontend.views.render')
def test_landing_login_success(mock_render, mock_login, mock_verify):
    request = HttpRequest()
    request.method = 'POST'
    request.session = MagicMock()
    request.POST = {'email': 'test@example.com', 'password': 'pass', 'action': 'login'}

    mock_login.return_value = {"idToken": "token"}
    mock_verify.return_value = {"uid": "123", "email": "test@example.com"}

    with patch('gamestore.frontend.views.redirect') as mock_redirect:
        landing(request)
        mock_redirect.assert_called_once_with('/store/')
        assert request.session.__setitem__.called  # or check the call


@patch('gamestore.frontend.views.messages.error')
@patch('gamestore.frontend.views.auth.verify_id_token')
@patch('gamestore.frontend.views.login_user')
@patch('gamestore.frontend.views.render')
def test_landing_login_failure(mock_render, mock_login, mock_verify, mock_messages_error):
    request = HttpRequest()
    request.method = 'POST'
    request.session = {}
    request.POST = {'email': 'test@example.com', 'password': 'pass', 'action': 'login'}

    mock_login.return_value = None

    landing(request)
    mock_render.assert_called_once_with(request, 'frontend/landing.html')


@patch('gamestore.frontend.views.messages.success')
@patch('gamestore.frontend.views.create_user')
@patch('gamestore.frontend.views.render')
def test_landing_signup_success(mock_render, mock_create, mock_messages_success):
    request = HttpRequest()
    request.method = 'POST'
    request.session = {}
    request.POST = {'email': 'test@example.com', 'password': 'pass', 'action': 'signup'}

    mock_create.return_value = MagicMock()

    landing(request)
    mock_render.assert_called_once_with(request, 'frontend/landing.html')


@patch('gamestore.frontend.views.messages.error')
@patch('gamestore.frontend.views.create_user')
@patch('gamestore.frontend.views.render')
def test_landing_signup_failure(mock_render, mock_create, mock_messages_error):
    request = HttpRequest()
    request.method = 'POST'
    request.session = {}
    request.POST = {'email': 'test@example.com', 'password': 'pass', 'action': 'signup'}

    mock_create.side_effect = Exception("Error")

    landing(request)
    mock_render.assert_called_once_with(request, 'frontend/landing.html')


@patch('gamestore.frontend.views.db.collection')
@patch('gamestore.frontend.views.render')
def test_store_get(mock_render, mock_collection):
    request = HttpRequest()
    request.method = 'GET'
    request.session = {'user': 'data'}

    mock_game1 = MagicMock()
    mock_game1.to_dict.return_value = {'title': 'Game1'}
    mock_game1.id = 'id1'
    mock_collection.return_value.stream.return_value = [mock_game1]

    store(request)
    mock_render.assert_called_once_with(request, "frontend/store.html", {"games": [{'title': 'Game1', 'id': 'id1'}]})


@patch('gamestore.frontend.views.messages.success')
@patch('gamestore.frontend.views.db.collection')
@patch('gamestore.frontend.views.render')
def test_store_add_to_basket(mock_render, mock_collection, mock_messages_success):
    request = HttpRequest()
    request.method = 'POST'
    request.POST = {'action': 'add_to_basket', 'game_id': '1', 'title': 'Game1', 'price': '10.0'}
    request.session = {'user': 'data', 'basket': {}}

    mock_collection.return_value.stream.return_value = []

    store(request)
    assert request.session['basket']['1'] == {'title': 'Game1', 'price': 10.0, 'qty': 1}


@patch('gamestore.frontend.views.logout')
@patch('gamestore.frontend.views.redirect')
@patch('gamestore.frontend.views.db.collection')
@patch('gamestore.frontend.views.render')
def test_store_logout(mock_render, mock_collection, mock_redirect, mock_logout):
    request = HttpRequest()
    request.method = 'POST'
    request.POST = {'action': 'logout'}
    request.session = {'user': 'data'}

    mock_collection.return_value.stream.return_value = []

    store(request)
    mock_logout.assert_called_once_with(request)
    mock_redirect.assert_called_once_with('/')


@patch('gamestore.frontend.views.render')
def test_checkout_get(mock_render):
    request = HttpRequest()
    request.method = 'GET'
    request.session = {'user': 'data', 'basket': {'1': {'price': 10.0, 'qty': 2}}}

    checkout(request)
    mock_render.assert_called_once_with(request, 'frontend/checkout.html', {'basket': {'1': {'price': 10.0, 'qty': 2}}, 'total': 20.0})


@patch('gamestore.frontend.views.redirect')
def test_checkout_remove_from_basket(mock_redirect):
    request = HttpRequest()
    request.method = 'POST'
    request.POST = {'action': 'remove_from_basket', 'game_id': '1'}
    request.session = {'user': 'data', 'basket': {'1': {'price': 10.0, 'qty': 2}}}

    checkout(request)
    assert request.session['basket']['1']['qty'] == 1
    mock_redirect.assert_called_once_with('/checkout/')

@patch('gamestore.frontend.views.messages.error')
@patch('gamestore.frontend.views.redirect')
def test_checkout_place_order_empty_basket(mock_redirect, mock_messages_error):
    request = HttpRequest()
    request.method = 'POST'
    request.POST = {'action': 'place_order'}
    request.session = {'user': 'data', 'basket': {}}

    checkout(request)
    mock_redirect.assert_called_once_with('/checkout/')