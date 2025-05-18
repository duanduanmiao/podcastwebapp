from flask import Blueprint, render_template, session

from podcast.home import services
import podcast.adapters.repository as repo
from podcast.authentication import services as auth_services

home_blueprint = Blueprint(
    'home_bp', __name__)


@home_blueprint.route('/', methods=['GET'])
def home():
    eight_podcasts = services.get_8_podcasts(repo.repo_instance)
    ten_podcasts = services.get_top_10_podcasts(repo.repo_instance)
    username = session.get('user_name')
    user = auth_services.get_user(username, repo.repo_instance)
    return render_template(
        "home.html",
        eight_podcasts=eight_podcasts,
        ten_podcasts=ten_podcasts,
        user=user
    )

