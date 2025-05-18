import csv
from pathlib import Path
from datetime import date, datetime
from typing import List

from bisect import bisect, bisect_left, insort_left

from podcast.adapters.repository import AbstractRepository
from podcast.domainmodel.model import Episode, Playlist


class MemoryRepository(AbstractRepository):

    def __init__(self):
        self.episodes = []
        self.podcasts = []
        self.categories = set()
        self.users = []
        self.reviews = []
        self.playlists = []

    def add_episode(self, episode):
        self.episodes.append(episode)

    def add_podcast(self, podcast):
        self.podcasts.append(podcast)

    def add_category(self, category):
        self.categories.add(category)

    def get_podcasts(self):
        return self.podcasts

    def get_episodes(self):
        return self.episodes

    def get_categories(self):
        return self.categories

    def get_episode_by_id(self, episode_id):
        return self.episodes[episode_id - 1]

    def get_podcast_by_id(self, podcast_id):
        return self.podcasts[podcast_id - 1]

    def add_user(self, user):
        self.playlists.append(Playlist(len(self.playlists), user))
        return self.users.append(user)

    def get_number_users(self):
        return len(self.users)

    def get_user(self, username):
        for user1 in self.users:
            if username == user1.username:
                return user1

    def get_reviews(self):
        return self.reviews

    def add_review(self, review):
        self.reviews.append(review)

    def get_playlists(self):
        return self.playlists

    def add_podcast_to_playlist(self, playlist_id, podcast):
        self.playlists[playlist_id].podcasts.append(podcast)

    def remove_podcast_from_playlist(self, playlist_id, podcast):
        self.playlists[playlist_id].podcasts.remove(podcast)

    def add_episode_to_playlist(self, playlist_id, episode):
        self.playlists[playlist_id].episodes.append(episode)

    def remove_episode_from_playlist(self, playlist_id, episode):
        self.playlists[playlist_id].episodes.remove(episode)