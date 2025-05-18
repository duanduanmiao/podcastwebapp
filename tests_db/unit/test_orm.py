import pytest

import datetime

from sqlalchemy.exc import IntegrityError

from podcast.domainmodel.model import User, Podcast, Episode, Review, Category, Author, Playlist
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, clear_mappers
from podcast.adapters.orm import metadata, map_model_to_tables

from utils import get_project_root

TEST_DATA_PATH_DATABASE_FULL = get_project_root() / "podcast" / "adapters" / "data"
TEST_DATA_PATH_DATABASE_LIMITED = get_project_root() / "tests" / "data"

TEST_DATABASE_URI_IN_MEMORY = 'sqlite://'
TEST_DATABASE_URI_FILE = 'sqlite:///podcasts-test.db'


@pytest.fixture
def empty_session():
    clear_mappers()
    engine = create_engine(TEST_DATABASE_URI_IN_MEMORY)
    metadata.create_all(engine)
    for table in reversed(metadata.sorted_tables):
        engine.execute(table.delete())
    map_model_to_tables()
    session_factory = sessionmaker(bind=engine)
    yield session_factory()
    metadata.drop_all(engine)


article_date = datetime.date(2020, 2, 28)


def insert_user(empty_session, values=None):
    new_name = "Andrew"
    new_password = "1234"

    if values is not None:
        new_name = values[0]
        new_password = values[1]

    empty_session.execute('INSERT INTO users (username, password) VALUES (:username, :password)',
                          {'username': new_name, 'password': new_password})
    row = empty_session.execute('SELECT id from users where username = :username',
                                {'username': new_name}).fetchone()
    return row[0]


def insert_users(empty_session, values):
    for value in values:
        empty_session.execute('INSERT INTO users (user_name, password) VALUES (:user_name, :password)',
                              {'user_name': value[0], 'password': value[1]})
    rows = list(empty_session.execute('SELECT id from users'))
    keys = tuple(row[0] for row in rows)
    return keys


def insert_podcast(empty_session):
    empty_session.execute(
        'INSERT INTO podcasts (title, image, description, language, website, author_id, itunes_id) VALUES '
        '("Test Title", '
        '"Test Image", '
        '"Test Description",'
        '"Test Language",'
        '"Test Website",'
        '"Test Author",'
        '"123")'
    )
    row = empty_session.execute('SELECT id from podcasts').fetchone()
    return row[0]


def insert_episode(empty_session):
    empty_session.execute(
        'INSERT INTO episodes (title, podcast_id, link, length, description, date) VALUES ("Test Title", 1, "Test Audio", "Test Audio Length", "Test Description", "Test Date")'
    )
    rows = list(empty_session.execute('SELECT id from episodes'))
    return rows[0][0]


def insert_article_tag_associations(empty_session, article_key, tag_keys):
    stmt = 'INSERT INTO article_tags (article_id, tag_id) VALUES (:article_id, :tag_id)'
    for tag_key in tag_keys:
        empty_session.execute(stmt, {'article_id': article_key, 'tag_id': tag_key})


def make_user():
    user = User(1, "Andrew", "111")
    return user


def test_saving_of_users(empty_session):
    user = make_user()
    empty_session.add(user)
    empty_session.commit()

    rows = list(empty_session.execute('SELECT username, password FROM users'))
    assert rows == [("andrew", "111")]


def test_saving_of_users_with_common_user_name(empty_session):
    user = User(1, "Andrew", "1234")
    empty_session.add(user)
    empty_session.commit()

    with pytest.raises(IntegrityError):
        user = User(2, "Andrew", "111")
        empty_session.add(user)
        empty_session.commit()
        rows = list(empty_session.execute('SELECT username, password FROM users'))


def test_loading_of_podcasts(empty_session):
    id = insert_podcast(empty_session)
    podcast = empty_session.query(Podcast).one()

    assert podcast.id == id


def test_loading_of_episodes(empty_session):
    id = insert_episode(empty_session)
    episode = empty_session.query(Episode).one()

    assert episode.id == id


def test_loading_of_podcast_episode(empty_session):
    insert_episode(empty_session)

    rows = empty_session.query(Episode).all()
    episodes = rows[0]

    assert episodes.podcast_id == 1


def test_saving_of_review(empty_session):
    podcast_id = insert_podcast(empty_session)
    user_id = insert_user(empty_session, ("Andrew", "1234"))

    user = empty_session.query(User).filter(User._User__username == "Andrew").one()

    # Create a new Review that is bidirectionally linked with the User and Review.
    review_text = "Some review text."
    review_title = "Test Review"
    review = Review(1, podcast_id, user, review_title, 5, review_text)

    empty_session.add(review)
    empty_session.commit()

    rows = list(empty_session.execute('SELECT user_id, podcast_id, content FROM reviews'))

    assert rows == [(user_id, podcast_id, review_text)]


def test_saving_of_categories(empty_session):
    category = Category(1, "Test Category")
    empty_session.add(category)
    empty_session.commit()

    rows = list(empty_session.execute('SELECT id, name FROM categories'))
    assert rows == [(1, "Test Category")]


def test_saving_authors(empty_session):
    author = Author(1, "Test Author")
    empty_session.add(author)
    empty_session.commit()

    rows = list(empty_session.execute('SELECT id FROM authors'))
    author_id = rows[0][0]

    assert author_id == 1


def test_save_playlists(empty_session):
    user = make_user()
    empty_session.add(user)
    playlist = Playlist(1, user)
    empty_session.add(playlist)
    empty_session.commit()

    rows = list(empty_session.execute('SELECT id, user_id FROM playlists'))
    assert rows == [(1, 1)]


def test_save_episode_playlists(empty_session):
    user = make_user()
    empty_session.add(user)
    playlist = Playlist(1, user)
    id = insert_episode(empty_session)
    episode = empty_session.query(Episode).one()
    empty_session.commit()
    assert episode.id == id
    playlist.episodes.append(episode)
    empty_session.add(playlist)
    empty_session.commit()
    rows = list(empty_session.execute('SELECT episode_id, playlist_id FROM episode_playlists'))
    assert rows == [(1, 1)]


def test_save_podcast_playlists(empty_session):
    user = make_user()
    empty_session.add(user)
    playlist = Playlist(1, user)
    id = insert_podcast(empty_session)
    podcast = empty_session.query(Podcast).one()
    empty_session.commit()
    assert podcast.id == id
    playlist.podcasts.append(podcast)
    empty_session.add(playlist)
    empty_session.commit()
    rows = list(empty_session.execute('SELECT podcast_id, playlist_id FROM podcast_playlists'))
    assert rows == [(1, 1)]
