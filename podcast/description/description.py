from flask import Blueprint, render_template, session

import podcast.adapters.repository as repo
from podcast.review import services as review_services
from podcast.description import services
from podcast.authentication import services as auth_services

description_blueprint = Blueprint(
    'description_bp', __name__)


@description_blueprint.route('/description/<int:podcast_id>', methods=['GET'])
def description(podcast_id):
    reviews = review_services.get_reviews_by_podcast_id(repo.repo_instance, podcast_id)
    avg_rating = sum([int(review.rating) for review in reviews]) / len(reviews) if reviews else 0
    username = session.get('user_name')
    podcast = services.get_podcast_by_id(repo.repo_instance, podcast_id)
    user = auth_services.get_user(username, repo.repo_instance)
    return render_template("description.html",
                           podcast=podcast,
                           user=user,
                           reviews=reviews,
                           avg_rating=avg_rating)