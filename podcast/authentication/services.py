from werkzeug.security import generate_password_hash, check_password_hash

from podcast.adapters.repository import AbstractRepository
from podcast.domainmodel.model import User


class NameNotUniqueException(Exception):
    pass


class UnknownUserException(Exception):
    pass


class AuthenticationException(Exception):
    pass


def add_user(user_name: str, password: str, repo: AbstractRepository):
    if not repo.get_user(user_name):
        password_hash = generate_password_hash(password)
        user = User(repo.get_number_users(), user_name, password_hash)
        repo.add_user(user)
        return user
    raise NameNotUniqueException


def authenticate_user(user_name: str, password: str, repo: AbstractRepository):
    authenticated = False
    user = repo.get_user(user_name)
    if user is not None:
        authenticated = check_password_hash(user.password, password)
    return authenticated


def get_user(user_name: str, repo: AbstractRepository) -> User:
    return repo.get_user(user_name)
