from podcast.adapters.repository import AbstractRepository


def get_podcast_by_id(repo: AbstractRepository, podcast_id):
    podcast = repo.get_podcast_by_id(podcast_id)
    podcast.episodes.sort(key=lambda episode: episode.title)
    return podcast