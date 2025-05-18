from datetime import date, datetime

import pytest

import podcast.adapters.repository as repo
from podcast.adapters.database_repository import SqlAlchemyRepository
from podcast.domainmodel.model import User, Podcast, Author, Episode, Category, Review
from podcast.adapters.repository import RepositoryException

import pytest

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, clear_mappers

from podcast import CSVDataReader
from podcast.adapters import database_repository
from podcast.adapters.datareader import csvdatareader
from podcast.adapters.orm import metadata, map_model_to_tables

from utils import get_project_root

TEST_DATA_PATH_DATABASE_FULL = get_project_root() / "podcast" / "adapters" / "data"
TEST_DATA_PATH_DATABASE_LIMITED = get_project_root() / "tests" / "data"

TEST_DATABASE_URI_IN_MEMORY = 'sqlite://'
TEST_DATABASE_URI_FILE = 'sqlite:///podcasts-test.db'


@pytest.fixture
def session_factory():
    clear_mappers()
    engine = create_engine(TEST_DATABASE_URI_IN_MEMORY)
    metadata.create_all(engine)
    for table in reversed(metadata.sorted_tables):
        engine.execute(table.delete())
    map_model_to_tables()
    # Create the database session factory using sessionmaker (this has to be done once, in a global manner)
    session_factory = sessionmaker(autocommit=False, autoflush=True, bind=engine)
    # Create the SQLAlchemy DatabaseRepository instance for an sqlite3-based repository.
    repo_instance = database_repository.SqlAlchemyRepository(session_factory)
    CSVDataReader().populate(TEST_DATA_PATH_DATABASE_LIMITED, repo_instance)
    yield session_factory
    metadata.drop_all(engine)


def test_repository_can_add_a_user(session_factory):
    repo = SqlAlchemyRepository(session_factory)

    user = User(1, 'Dave', '123456789')
    repo.add_user(user)

    repo.add_user(User(2, 'Martin', '123456789'))

    user2 = repo.get_user('dave')

    assert user2 == user and user2 is user


def test_repository_can_retrieve_a_user(session_factory):
    repo = SqlAlchemyRepository(session_factory)

    user = User(1, 'fmercury', '123456789')
    repo.add_user(user)

    user = repo.get_user('fmercury')
    assert user.username == "fmercury"


def test_repository_does_not_retrieve_a_non_existent_user(session_factory):
    repo = SqlAlchemyRepository(session_factory)

    user = repo.get_user('prince')
    assert user is None


def test_repository_can_retrieve_users_count(session_factory):
    repo = SqlAlchemyRepository(session_factory)

    user = User(1, 'fmercury', '123456789')
    repo.add_user(user)

    number_of_users = repo.get_number_users()

    assert number_of_users == 1


def test_repository_can_add_podcast(session_factory):
    repo = SqlAlchemyRepository(session_factory)

    podcast1 = Podcast(4, Author(4, 'Test Author'), 'Test Title', "Test Image", "Test Description", "Test Website", 123,
                       "Test Language")

    repo.add_podcast(podcast1)

    podcast2 = repo.get_podcast_by_id(4)

    assert podcast1 == podcast2


def test_repository_can_add_episode(session_factory):
    repo = SqlAlchemyRepository(session_factory)

    episode1 = Episode(4, 1, 'Test Title', 'Test Link', 1, 'Test Description', 'Test Date')

    repo.add_episode(episode1)

    episode2 = repo.get_episode_by_id(4)

    assert episode1 == episode2


def test_repository_can_get_all_episodes(session_factory):
    repo = SqlAlchemyRepository(session_factory)

    episodes = repo.get_episodes()
    assert len(episodes) == 3


def test_repository_can_get_all_podcasts(session_factory):
    repo = SqlAlchemyRepository(session_factory)

    podcasts = repo.get_podcasts()
    assert len(podcasts) == 3


def test_repository_can_get_podcast_by_id(session_factory):
    repo = SqlAlchemyRepository(session_factory)

    podcast1 = Podcast(4, Author(4, 'Test Author'), 'Test Title', "Test Image", "Test Description", "Test Website", 123,
                       "Test Language")

    repo.add_podcast(podcast1)

    podcast2 = repo.get_podcast_by_id(4)
    assert podcast1 == podcast2


def test_repository_can_get_episode_by_id(session_factory):
    repo = SqlAlchemyRepository(session_factory)

    episode1 = Episode(4, 1, 'Test Title', 'Test Link', 1, 'Test Description', 'Test Date')

    repo.add_episode(episode1)

    episode2 = repo.get_episode_by_id(4)

    assert episode1 == episode2


def test_repository_can_get_number_users(session_factory):
    repo = SqlAlchemyRepository(session_factory)

    user = User(1, 'Dave', '123456789')
    repo.add_user(user)

    number_users = repo.get_number_users()
    assert number_users == 1


def test_repository_can_add_category(session_factory):
    repo = SqlAlchemyRepository(session_factory)

    category1 = Category(8, 'Test Category')

    repo.add_category(category1)
    categories = repo.get_categories()
    assert categories[-1] == category1


def test_repository_can_get_categories(session_factory):
    repo = SqlAlchemyRepository(session_factory)

    category1 = Category(8, 'Test Category')

    repo.add_category(category1)
    categories = repo.get_categories()
    assert categories[-1] == category1


def test_repository_can_add_podcast_to_playlist(session_factory):
    repo = SqlAlchemyRepository(session_factory)

    user = User(1, 'Dave', '123456789')
    repo.add_user(user)
    playlist = repo.get_playlists()[-1]
    podcast = Podcast(4, Author(4, 'Test Author'), 'Test Title', "Test Image", "Test Description", "Test Website", 123,
                      "Test Language")
    repo.add_podcast_to_playlist(playlist.id, podcast)
    assert playlist.podcasts[0] == podcast


def test_repository_can_add_episode_to_playlist(session_factory):
    repo = SqlAlchemyRepository(session_factory)

    user = User(1, 'Dave', '123456789')
    repo.add_user(user)
    playlist = repo.get_playlists()[-1]
    episode = Episode(4, 1, 'Test Title', 'Test Link', 1, 'Test Description', 'Test Date')
    repo.add_episode_to_playlist(playlist.id, episode)
    assert playlist.episodes[0] == episode


def test_repository_add_review(session_factory):
    repo = SqlAlchemyRepository(session_factory)

    user = User(1, 'Dave', '123456789')
    repo.add_user(user)
    review = Review(1, 1, user, 'Test Title', 5, 'Test Content')
    repo.add_review(review)

    assert repo.get_reviews()[-1] == review


def test_repository_can_get_reviews(session_factory):
    repo = SqlAlchemyRepository(session_factory)

    user = User(1, 'Dave', '123456789')
    repo.add_user(user)
    review = Review(1, 1, user, 'Test Title', 5, 'Test Content')
    repo.add_review(review)

    assert repo.get_reviews()[-1] == review