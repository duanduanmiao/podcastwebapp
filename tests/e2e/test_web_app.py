import pytest

from flask import session

from podcast import MemoryRepository, create_app, CSVDataReader
from tests.conftest import TEST_DATA_PATH


@pytest.fixture
def client():
    my_app = create_app({
        'TESTING': True,  # Set to True during testing.
        'TEST_DATA_PATH': TEST_DATA_PATH,  # Path for loading test data into the repository.
        'WTF_CSRF_ENABLED': False,  # test_client will not send a CSRF token, so disable validation.
        'REPOSITORY': 'memory',
    })

    return my_app.test_client()


@pytest.fixture
def in_memory_repo():
    repo = MemoryRepository()
    CSVDataReader().populate(TEST_DATA_PATH, repo)
    return repo


def test_register(client):
    # Check that we retrieve the register page.
    response_code = client.get('/authentication/register').status_code
    assert response_code == 200

    # Check that we can register a user successfully, supplying a valid user name and password.
    response = client.post(
        '/authentication/register',
        data={'user_name': 'gmichael', 'password': 'CarelessWhisper1984'}
    )
    assert response.headers['Location'] == '/authentication/login'


def test_register_with_invalid_input(in_memory_repo, client):
    client.post(
        '/authentication/register',
        data={'user_name': "test1", 'password': "123456"}
    )

    assert len(in_memory_repo.users) == 0


def test_login(client):
    # Check that we can retrieve the login page.
    status_code = client.get('/authentication/login').status_code
    assert status_code == 200

    response = client.post(
        '/authentication/register',
        data={'user_name': 'gmichael', 'password': 'CarelessWhisper1984'}
    )
    assert response.headers['Location'] == '/authentication/login'

    # Check that a successful login generates a redirect to the homepage.
    response = client.post(
        '/authentication/login',
        data={'user_name': 'gmichael', 'password': 'CarelessWhisper1984'}
    )
    assert response.headers['Location'] == '/'

    # Check that a session has been created for the logged-in user.
    with client:
        client.get('/')
        assert session['user_name'] == 'gmichael'


def test_logout(client):
    client.post(
        '/authentication/register',
        data={'user_name': 'gmichael', 'password': 'CarelessWhisper1984'}
    )
    client.post(
        '/authentication/login',
        data={'user_name': 'gmichael', 'password': 'CarelessWhisper1984'}
    )
    client.get(
        '/authentication/logout',
    )
    with client.session_transaction() as session:
        assert "user_name" not in session


def test_index(client):
    # Check that we can retrieve the home page.
    response = client.get('/')
    assert response.status_code == 200
    assert b"CS235 Podcast Library - Home" in response.data


def test_searching_podcasts(client):
    response = client.get('/podcast/1/title/D-Hour Radio Network')
    assert b'D-Hour Radio Network' in response.data
    response = client.get('/podcast/1/category/Society & Culture')
    assert b'D-Hour Radio Network' in response.data
    assert b'Onde Road - Radio Popolare' in response.data
    response = client.get('/podcast/1/author/D Hour Radio Network')
    assert b'D-Hour Radio Network' in response.data
    response = client.get('/podcast/1/language/English')
    assert b'D-Hour Radio Network' in response.data
    assert b'Brian Denny Radio' in response.data


def test_reviewing_podcasts(client):
    client.post(
        '/authentication/register',
        data={'user_name': 'gmichael', 'password': 'CarelessWhisper1984'}
    )
    client.post(
        '/authentication/login',
        data={'user_name': 'gmichael', 'password': 'CarelessWhisper1984'}
    )
    response = client.get('/review/1/title/5/content')
    assert response.status_code == 302
    response = client.get('/description/1')
    assert b"title" in response.data


def test_adding_podcasts_to_playlist(client):
    client.post(
        '/authentication/register',
        data={'user_name': 'gmichael', 'password': 'CarelessWhisper1984'}
    )
    client.post(
        '/authentication/login',
        data={'user_name': 'gmichael', 'password': 'CarelessWhisper1984'}
    )
    response = client.get('/playlist/add/1')
    assert response.status_code == 204


def test_adding_episodes_to_playlist(client):
    client.post(
        '/authentication/register',
        data={'user_name': 'gmichael', 'password': 'CarelessWhisper1984'}
    )
    client.post(
        '/authentication/login',
        data={'user_name': 'gmichael', 'password': 'CarelessWhisper1984'}
    )
    response = client.get('/playlist/add/episode/1')
    assert response.status_code == 204
