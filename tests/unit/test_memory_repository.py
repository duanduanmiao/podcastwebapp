from datetime import date, datetime
from typing import List

import pytest

from podcast.domainmodel.model import Episode, Podcast, Author, Category, User, Review
from tests.conftest import in_memory_repo


def test_repository_can_add_a_episode(in_memory_repo):
    episode = Episode(4, 1, "title", "link", 10, "description", "2017-12-01")
    in_memory_repo.add_episode(episode)

    assert in_memory_repo.get_episode_by_id(4) is episode


def test_repository_can_add_a_podcast(in_memory_repo):
    episode = Podcast(4, Author(1, "author_name"), "title", "image", "description", "website", 1000, "Language")
    in_memory_repo.add_episode(episode)

    assert in_memory_repo.get_episode_by_id(4) is episode


def test_repository_can_add_a_category(in_memory_repo):
    category = Category(8, "category")
    in_memory_repo.add_category(category)

    assert list(in_memory_repo.get_categories())[-1] is category


def test_repository_can_get_podcasts(in_memory_repo):
    assert len(in_memory_repo.get_podcasts()) == 3


def test_repository_can_get_episodes(in_memory_repo):
    assert len(in_memory_repo.get_episodes()) == 3


def test_repository_can_get_categories(in_memory_repo):
    assert len(in_memory_repo.get_categories()) == 7


def test_repository_can_get_episode_by_id(in_memory_repo):
    episode = Episode(4, 1, "title", "link", 10, "description", "2017-12-01")
    in_memory_repo.add_episode(episode)

    assert in_memory_repo.get_episode_by_id(4) is episode


def test_repository_can_get_podcast_by_id(in_memory_repo):
    episode = Podcast(4, Author(1, "author_name"), "title", "image", "description", "website", 1000, "Language")
    in_memory_repo.add_episode(episode)

    assert in_memory_repo.get_episode_by_id(4) is episode


def test_repository_can_add_user(in_memory_repo):
    user = User(1, "username", "password")
    in_memory_repo.add_user(user)
    assert in_memory_repo.get_user("username") == user


def test_repository_can_get_number_users(in_memory_repo):
    user = User(1, "username", "password")
    in_memory_repo.add_user(user)
    assert in_memory_repo.get_number_users() == 1


def test_repository_can_get_user(in_memory_repo):
    user = User(1, "username", "password")
    in_memory_repo.add_user(user)
    assert in_memory_repo.get_user("username") == user


def test_repository_can_get_reviews(in_memory_repo):
    user = User(1, "username", "password")
    in_memory_repo.add_user(user)
    review = Review(1, 1, user, "link", 5, "test")
    in_memory_repo.add_review(review)
    assert in_memory_repo.get_reviews()[0] == review


def test_repository_can_add_review(in_memory_repo):
    user = User(1, "username", "password")
    in_memory_repo.add_user(user)
    review = Review(1, 1, user, "link", 5, "test")
    in_memory_repo.add_review(review)
    assert in_memory_repo.get_reviews()[0] == review


def test_repository_can_get_playlists(in_memory_repo):
    user = User(1, "username", "password")
    in_memory_repo.add_user(user)
    assert in_memory_repo.get_playlists()[0].user == user


def test_repository_can_add_podcast_to_playlist(in_memory_repo):
    user = User(1, "username", "password")
    in_memory_repo.add_user(user)
    podcast = in_memory_repo.get_podcasts()[0]
    playlist = in_memory_repo.get_playlists()[0]
    playlist.podcasts.append(podcast)
    assert len(playlist.podcasts) == 1


def test_repository_can_add_episode_to_playlist(in_memory_repo):
    user = User(1, "username", "password")
    in_memory_repo.add_user(user)
    episode = in_memory_repo.get_episodes()[0]
    playlist = in_memory_repo.get_playlists()[0]
    playlist.episodes.append(episode)
    assert len(playlist.episodes) == 1