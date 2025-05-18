from flask import Blueprint, render_template, session, redirect, url_for, request

from podcast.review import services
import podcast.adapters.repository as repo

review_blueprint = Blueprint(
    'review_bp', __name__, url_prefix='/review')


@review_blueprint.route('/<podcast_id>/<title>/<ratio>/<content>', methods=['GET'])
def add_review(podcast_id, title, ratio, content):
    username = session.get('user_name')
    services.add_review(repo.repo_instance, podcast_id, username, title, ratio, content)
    return redirect(url_for("description_bp.description", podcast_id=podcast_id))