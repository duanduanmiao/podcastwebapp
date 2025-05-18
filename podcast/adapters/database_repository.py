from datetime import date
from typing import List

from sqlalchemy import desc, asc
from sqlalchemy.orm.exc import NoResultFound

from sqlalchemy.orm import scoped_session

from podcast.domainmodel.model import User, Podcast, Episode, Review, Playlist, Category
from podcast.adapters.repository import AbstractRepository


class SessionContextManager:
    def __init__(self, session_factory):
        self.__session_factory = session_factory
        self.__session = scoped_session(self.__session_factory)

    def __enter__(self):
        return self

    def __exit__(self, *args):
        self.rollback()

    @property
    def session(self):
        return self.__session

    def commit(self):
        self.__session.commit()

    def rollback(self):
        self.__session.rollback()

    def reset_session(self):
        # this method can be used e.g. to allow Flask to start a new session for each http request,
        # via the 'before_request' callback
        self.close_current_session()
        self.__session = scoped_session(self.__session_factory)

    def close_current_session(self):
        if not self.__session is None:
            self.__session.close()


class SqlAlchemyRepository(AbstractRepository):

    def __init__(self, session_factory):
        self._session_cm = SessionContextManager(session_factory)

    def close_session(self):
        self._session_cm.close_current_session()

    def reset_session(self):
        self._session_cm.reset_session()

    def add_user(self, user: User):
        with self._session_cm as scm:
            scm.session.add(user)
            scm.session.add(Playlist(None, user))
            scm.commit()

    def get_user(self, user_name: str) -> User:
        user = None
        try:
            user = self._session_cm.session.query(User).filter(User._User__username == user_name).one()
        except NoResultFound:
            pass
        return user

    def add_episode(self, episode):
        with self._session_cm as scm:
            scm.session.add(episode)
            scm.commit()

    def add_podcast(self, podcast):
        with self._session_cm as scm:
            scm.session.add(podcast)
            scm.commit()

    def get_episodes(self):
        return self._session_cm.session.query(Episode).all()

    def get_podcasts(self):
        return self._session_cm.session.query(Podcast).all()

    def get_podcast_by_id(self, podcast_id):
        return self._session_cm.session.query(Podcast).filter(Podcast._Podcast__id==podcast_id).first()

    def get_episode_by_id(self, episode_id):
        return self._session_cm.session.query(Episode).filter_by(id=episode_id).first()

    def add_category(self, category):
        with self._session_cm as scm:
            scm.session.add(category)
            scm.commit()

    def get_categories(self):
        return self._session_cm.session.query(Category).all()

    def get_number_users(self):
        return len(self._session_cm.session.query(User).all())

    def get_reviews(self):
        return self._session_cm.session.query(Review).all()

    def add_review(self, review):
        with self._session_cm as scm:
            scm.session.add(review)
            scm.commit()

    def get_playlists(self):
        return self._session_cm.session.query(Playlist).all()

    def add_podcast_to_playlist(self, playlist_id, podcast):
        with self._session_cm as scm:
            scm.session.query(Playlist).filter_by(id=playlist_id).first().podcasts.append(podcast)
            scm.commit()

    def remove_podcast_from_playlist(self, playlist_id, podcast):
        with self._session_cm as scm:
            scm.session.query(Playlist).filter_by(id=playlist_id).first().podcasts.remove(podcast)
            scm.commit()

    def add_episode_to_playlist(self, playlist_id, episode):
        with self._session_cm as scm:
            scm.session.query(Playlist).filter_by(id=playlist_id).first().episodes.append(episode)
            scm.commit()

    def remove_episode_from_playlist(self, playlist_id, episode):
        with self._session_cm as scm:
            scm.session.query(Playlist).filter_by(id=playlist_id).first().episodes.remove(episode)
            scm.commit()
