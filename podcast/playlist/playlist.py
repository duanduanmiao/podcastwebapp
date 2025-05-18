from flask import Blueprint, render_template, session, redirect, url_for, Response

import podcast.adapters.repository as repo
from podcast.authentication import services as auth_services
from podcast.playlist import services
from podcast.podcast import services as podcast_services

playlist_blueprint = Blueprint(
    'playlist_bp', __name__, url_prefix='/playlist')


@playlist_blueprint.route('/', methods=['GET'])
def playlist():
    username = session.get('user_name')
    user = auth_services.get_user(username, repo.repo_instance)
    if user:
        playlist = services.get_playlist_by_username(repo.repo_instance, user.username)
        podcasts = playlist.podcasts
        episodes = playlist.episodes
        categories = podcast_services.get_category_podcasts(repo.repo_instance, podcasts)
        return render_template(
            "playlist.html",
            playlist=playlist,
            podcasts=podcasts,
            categories=categories,
            episodes=episodes,
            zip=zip,
            user=user,
            len=len
        )
    return redirect(url_for('home_bp.home'))


@playlist_blueprint.route('/add/<int:podcast_id>', methods=['GET'])
def add_podcast(podcast_id):
    username = session.get('user_name')
    user = auth_services.get_user(username, repo.repo_instance)
    if user:
        services.add_podcast(repo.repo_instance, podcast_id, username)
    return Response(status=204)


@playlist_blueprint.route('/del/<int:podcast_id>', methods=['GET'])
def delete_podcast(podcast_id):
    username = session.get('user_name')
    user = auth_services.get_user(username, repo.repo_instance)
    if user:
        services.delete_podcast(repo.repo_instance, podcast_id, username)
        return redirect(url_for('playlist_bp.playlist'))
    return redirect(url_for('home_bp.home'))


@playlist_blueprint.route('/add/episode/<int:episode_id>', methods=['GET'])
def add_episode(episode_id):
    username = session.get('user_name')
    user = auth_services.get_user(username, repo.repo_instance)
    if user:
        services.add_episode(repo.repo_instance, episode_id, username)
    return Response(status=204)


@playlist_blueprint.route('/del/episode/<int:episode_id>', methods=['GET'])
def delete_episode(episode_id):
    username = session.get('user_name')
    user = auth_services.get_user(username, repo.repo_instance)
    if user:
        services.delete_episode(repo.repo_instance, episode_id, username)
        return redirect(url_for('playlist_bp.playlist'))
    return redirect(url_for('home_bp.home'))

