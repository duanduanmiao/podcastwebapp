from flask import Blueprint, render_template, session, redirect, url_for

from podcast.podcast import services
import podcast.adapters.repository as repo
from podcast.authentication import services as auth_services

podcast_blueprint = Blueprint(
    'podcast_bp', __name__)


@podcast_blueprint.route('/podcast/<int:page>', methods=['GET'])
def podcast(page=1):
    return redirect(url_for('podcast_bp.search', page=page, search_filter="all", condition="all"))


@podcast_blueprint.route('/podcast/<int:page>/<search_filter>/<condition>', methods=['GET'])
def search(search_filter, condition, page=1):
    podcasts, last_page = services.get_all_podcasts(repo.repo_instance, page)
    if search_filter == 'all':
        podcasts, last_page = services.get_all_podcasts(repo.repo_instance, page)
    else:
        if search_filter == 'language':
            podcasts, last_page = services.get_podcasts_by_language(repo.repo_instance, condition, page)
        elif search_filter == 'category':
            podcasts, last_page = services.get_podcasts_by_categories(repo.repo_instance, condition, page)
        elif search_filter == 'title':
            podcasts, last_page = services.get_podcasts_by_title(repo.repo_instance, condition, page)
        elif search_filter == 'author':
            podcasts, last_page = services.get_podcasts_by_author(repo.repo_instance, condition, page)
    categories = services.get_category_podcasts(repo.repo_instance, podcasts)
    username = session.get('user_name')
    user = auth_services.get_user(username, repo.repo_instance)
    return render_template(
        "podcast.html",
        podcasts=podcasts,
        categories=categories,
        zip=zip,
        page=page,
        user=user,
        search_filter=search_filter,
        condition=condition,
        last_page=last_page
    )
