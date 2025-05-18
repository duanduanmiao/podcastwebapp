from sqlalchemy import select, inspect

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
def database_engine():
    clear_mappers()
    engine = create_engine(TEST_DATABASE_URI_FILE)
    metadata.create_all(engine)  # Conditionally create database tables.
    for table in reversed(metadata.sorted_tables):  # Remove any data from the tables.
        engine.execute(table.delete())
    map_model_to_tables()
    # Create the database session factory using sessionmaker (this has to be done once, in a global manner)
    session_factory = sessionmaker(autocommit=False, autoflush=True, bind=engine)
    # Create the SQLAlchemy DatabaseRepository instance for an sqlite3-based repository.
    repo_instance = database_repository.SqlAlchemyRepository(session_factory)
    CSVDataReader().populate(TEST_DATA_PATH_DATABASE_LIMITED, repo_instance)
    yield engine
    metadata.drop_all(engine)


def test_database_populate_inspect_table_names(database_engine):
    # Get table information
    inspector = inspect(database_engine)
    assert inspector.get_table_names() == ['authors', 'categories', 'episode_playlists', 'episodes',
                                           'playlists', 'podcast_categories', 'podcast_playlists', 'podcasts',
                                           'reviews', 'users']


def test_database_populate_all_podcasts(database_engine):
    # Get table information
    inspector = inspect(database_engine)
    name_of_podcasts_table = inspector.get_table_names()[7]

    with database_engine.connect() as connection:
        select_statement = select([metadata.tables[name_of_podcasts_table]])
        result = connection.execute(select_statement)

        all_podcast_names = []
        for row in result:
            all_podcast_names.append(row['title'])

        assert all_podcast_names == ['D-Hour Radio Network', 'Brian Denny Radio', 'Onde Road - Radio Popolare']


def test_database_populate_all_episodes(database_engine):
    # Get table information
    inspector = inspect(database_engine)
    name_of_users_table = inspector.get_table_names()[3]

    with database_engine.connect() as connection:
        select_statement = select([metadata.tables[name_of_users_table]])
        result = connection.execute(select_statement)

        all_episodes = []
        for row in result:
            all_episodes.append(row['title'])

        assert all_episodes == [
            'The Mandarian Orange Show Episode 74- Bad Hammer Time, or: 30 Day MoviePass Challenge Part 3',
            'Finding yourself in the character by justifying your actions', 'Episode 182 - Lyrically Weak']


def test_database_populate_all_authors(database_engine):
    # Get table information
    inspector = inspect(database_engine)
    name_of_comments_table = inspector.get_table_names()[0]

    with database_engine.connect() as connection:
        select_statement = select([metadata.tables[name_of_comments_table]])
        result = connection.execute(select_statement)

        all_authors = []
        for row in result:
            all_authors.append(row['name'])

        assert all_authors == ['D Hour Radio Network', 'Brian Denny', 'Radio Popolare']


def test_database_populate_all_categories(database_engine):
    # Get table information
    inspector = inspect(database_engine)
    name_of_articles_table = inspector.get_table_names()[1]

    with database_engine.connect() as connection:
        select_statement = select([metadata.tables[name_of_articles_table]])
        result = connection.execute(select_statement)

        all_categories = []
        for row in result:
            all_categories.append((row['name']))

        nr_articles = len(all_categories)
        assert nr_articles == 7

        assert all_categories == [
            'Society & Culture', 'Personal Journals', 'Professional', 'News & Politics', 'Sports & Recreation',
            'Comedy', 'Society & Culture']
