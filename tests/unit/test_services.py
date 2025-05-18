from datetime import date

import pytest

from podcast.description import services as description_services
from podcast.domainmodel.model import User, Review
from podcast.home import services as home_services
from podcast.podcast import services as podcast_services
from podcast.authentication import services as auth_services
from podcast.playlist import services as playlist_services
from podcast.review import services as review_services
from tests.conftest import in_memory_repo


def test_can_get_podcast_by_id(in_memory_repo):
    podcast = description_services.get_podcast_by_id(in_memory_repo, 1)

    assert podcast.title == "D-Hour Radio Network"
    assert podcast.language == "English"
    assert podcast.itunes_id == 538283940


def test_can_get_8_podcasts(in_memory_repo):
    podcasts = home_services.get_8_podcasts(in_memory_repo)

    assert len(podcasts) == 3  # if length < 8, it would return the original list


def test_can_get_top_10_podcasts(in_memory_repo):
    podcasts = home_services.get_top_10_podcasts(in_memory_repo)

    assert len(podcasts) == 3  # if length < 10, it would return the original list


def test_can_get_all_podcasts(in_memory_repo):
    podcasts, last_page = podcast_services.get_all_podcasts(in_memory_repo, 1)

    assert len(podcasts) == 3  # if length < 10, it would return the original list
    assert last_page


def test_can_get_category_podcasts(in_memory_repo):
    podcasts, last_page = podcast_services.get_all_podcasts(in_memory_repo, 1)
    category_podcasts = podcast_services.get_category_podcasts(in_memory_repo, podcasts)
    print(category_podcasts)

    assert len(category_podcasts) == 3
    assert last_page
    assert category_podcasts[0] == 'Professional | News & Politics | Sports & Recreation | Comedy'


def test_can_add_user(in_memory_repo):
    auth_services.add_user("username", "password", in_memory_repo)
    assert auth_services.get_user("username", in_memory_repo) == User(0, "username", "password")


def test_can_authenticate_user(in_memory_repo):
    auth_services.add_user("username", "password", in_memory_repo)
    b = auth_services.authenticate_user("username", "password", in_memory_repo)
    assert b


def test_can_get_user(in_memory_repo):
    auth_services.add_user("username", "password", in_memory_repo)
    assert auth_services.get_user("username", in_memory_repo) == User(0, "username", "password")


def test_can_get_playlist_by_username(in_memory_repo):
    user = auth_services.add_user("username", "password", in_memory_repo)
    playlist = playlist_services.get_playlist_by_username(in_memory_repo, "username")
    assert playlist.user == user


def test_can_add_podcast_to_playlist(in_memory_repo):
    auth_services.add_user("username", "password", in_memory_repo)
    playlist_services.add_podcast(in_memory_repo, 1, "username")
    playlist = playlist_services.get_playlist_by_username(in_memory_repo, "username")
    assert len(playlist.podcasts) == 1


def test_can_add_episode_to_playlist(in_memory_repo):
    auth_services.add_user("username", "password", in_memory_repo)
    playlist_services.add_episode(in_memory_repo, 1, "username")
    playlist = playlist_services.get_playlist_by_username(in_memory_repo, "username")
    assert len(playlist.episodes) == 1


def test_can_delete_podcast_from_playlist(in_memory_repo):
    auth_services.add_user("username", "password", in_memory_repo)
    playlist_services.add_podcast(in_memory_repo, 1, "username")
    playlist = playlist_services.get_playlist_by_username(in_memory_repo, "username")
    assert len(playlist.podcasts) == 1
    playlist_services.delete_podcast(in_memory_repo, 1, "username")
    assert len(playlist.podcasts) == 0


def test_can_delete_episode_from_playlist(in_memory_repo):
    auth_services.add_user("username", "password", in_memory_repo)
    playlist_services.add_episode(in_memory_repo, 1, "username")
    playlist = playlist_services.get_playlist_by_username(in_memory_repo, "username")
    assert len(playlist.episodes) == 1
    playlist_services.delete_episode(in_memory_repo, 1, "username")
    assert len(playlist.episodes) == 0


def test_can_get_podcasts_by_title(in_memory_repo):
    auth_services.add_user("username", "password", in_memory_repo)
    podcasts, last_page = podcast_services.get_podcasts_by_title(in_memory_repo, "D-Hour Radio Network", 1)
    assert len(podcasts) == 1
    assert last_page


def test_can_get_podcasts_by_language(in_memory_repo):
    auth_services.add_user("username", "password", in_memory_repo)
    podcasts, last_page = podcast_services.get_podcasts_by_language(in_memory_repo, "English", 1)
    assert len(podcasts) == 2
    assert last_page


def test_can_get_podcasts_by_author(in_memory_repo):
    auth_services.add_user("username", "password", in_memory_repo)
    podcasts, last_page = podcast_services.get_podcasts_by_author(in_memory_repo, "D Hour Radio Network", 1)
    assert len(podcasts) == 1
    assert last_page


def test_can_get_podcasts_by_category(in_memory_repo):
    auth_services.add_user("username", "password", in_memory_repo)
    podcasts, last_page = podcast_services.get_podcasts_by_categories(in_memory_repo, "Professional", 1)
    assert len(podcasts) == 1
    assert last_page


def test_can_add_review(in_memory_repo):
    auth_services.add_user("username", "password", in_memory_repo)
    review_services.add_review(in_memory_repo, 1, "username", "title", 5, "content")
    reviews = review_services.get_reviews_by_podcast_id(in_memory_repo, 1)
    assert len(reviews) == 1


def test_can_get_reviews_by_podcast_id(in_memory_repo):
    auth_services.add_user("username", "password", in_memory_repo)
    review_services.add_review(in_memory_repo, 1, "username", "title", 5, "content")
    reviews = review_services.get_reviews_by_podcast_id(in_memory_repo, 1)
    assert len(reviews) == 1