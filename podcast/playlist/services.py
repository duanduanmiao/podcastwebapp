from podcast.adapters.repository import AbstractRepository
from podcast.domainmodel.model import Playlist, Podcast


def get_playlist_by_username(repo: AbstractRepository, username):
    playlists = repo.get_playlists()
    for playlist in playlists:
        if playlist.user.username == username:
            return playlist


def add_podcast(repo: AbstractRepository, podcast_id, username):
    playlist = get_playlist_by_username(repo, username)
    podcast = repo.get_podcast_by_id(podcast_id)
    repo.add_podcast_to_playlist(playlist.id, podcast)


def add_episode(repo: AbstractRepository, episode_id, username):
    playlist = get_playlist_by_username(repo, username)
    episode = repo.get_episode_by_id(episode_id)
    repo.add_episode_to_playlist(playlist.id, episode)


def delete_podcast(repo: AbstractRepository, podcast_id, username):
    playlist = get_playlist_by_username(repo, username)
    podcast = repo.get_podcast_by_id(podcast_id)
    repo.remove_podcast_from_playlist(playlist.id, podcast)


def delete_episode(repo: AbstractRepository, episode_id, username):
    playlist = get_playlist_by_username(repo, username)
    episode = repo.get_episode_by_id(episode_id)
    repo.remove_episode_from_playlist(playlist.id, episode)
