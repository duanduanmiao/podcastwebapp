import abc
from typing import List
from datetime import date

from podcast.domainmodel.model import Episode

repo_instance = None


class RepositoryException(Exception):

    def __init__(self, message=None):
        pass


class AbstractRepository(abc.ABC):

    @abc.abstractmethod
    def add_category(self, category):
        raise NotImplementedError

    @abc.abstractmethod
    def get_categories(self):
        raise NotImplementedError

    @abc.abstractmethod
    def add_episode(self, episode):
        raise NotImplementedError

    @abc.abstractmethod
    def add_podcast(self, podcast):
        raise NotImplementedError

    @abc.abstractmethod
    def get_episodes(self):
        raise NotImplementedError

    @abc.abstractmethod
    def get_podcasts(self):
        raise NotImplementedError

    @abc.abstractmethod
    def get_podcast_by_id(self, podcast_id):
        raise NotImplementedError

    @abc.abstractmethod
    def get_episode_by_id(self, episode_id):
        raise NotImplementedError

    @abc.abstractmethod
    def add_user(self, user):
        raise NotImplementedError

    @abc.abstractmethod
    def get_number_users(self):
        raise NotImplementedError

    @abc.abstractmethod
    def get_user(self, username):
        raise NotImplementedError

    @abc.abstractmethod
    def get_reviews(self):
        raise NotImplementedError

    @abc.abstractmethod
    def add_review(self, review):
        raise NotImplementedError

    @abc.abstractmethod
    def get_playlists(self):
        raise NotImplementedError

    @abc.abstractmethod
    def add_podcast_to_playlist(self, playlist_id, podcast):
        raise NotImplementedError

    @abc.abstractmethod
    def remove_podcast_from_playlist(self, playlist_id, podcast):
        raise NotImplementedError

    @abc.abstractmethod
    def add_episode_to_playlist(self, playlist_id, episode):
        raise NotImplementedError

    @abc.abstractmethod
    def remove_episode_from_playlist(self, playlist_id, episode):
        raise NotImplementedError







