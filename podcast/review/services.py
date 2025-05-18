from podcast.adapters.repository import AbstractRepository
from podcast.domainmodel.model import Review


def get_reviews_by_podcast_id(repo: AbstractRepository, podcast_id):
    res = []
    reviews = repo.get_reviews()
    for review in reviews:
        if int(review.podcast_id) == podcast_id:
            res.append(review)
    return res[::-1]


def add_review(repo: AbstractRepository, podcast_id, username, title, rating, content):
    user = repo.get_user(username)
    number_reviews = len(repo.get_reviews())
    review = Review(number_reviews, podcast_id, user, title, rating, content)
    repo.add_review(review)