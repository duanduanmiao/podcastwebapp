import random

from podcast.adapters.repository import AbstractRepository
from podcast.domainmodel.model import Review


def get_8_podcasts(repo: AbstractRepository):
    podcasts = repo.get_podcasts()
    podcast_list = []
    if len(podcasts) >= 8:
        number_list = random.sample(range(0, len(podcasts)), 8)
        for num in number_list:
            if num < len(podcasts):
                podcast = podcasts[num]
                podcast_list.append(podcast)
        return podcast_list
    else:
        return podcasts


def get_top_10_podcasts(repo: AbstractRepository):
    return repo.get_podcasts()[:10]


def get_podcast_by_id(repo: AbstractRepository, podcast_id):
    return repo.get_podcast_by_id(podcast_id)



