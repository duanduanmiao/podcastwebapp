from sqlalchemy import (
    Table, MetaData, Column, Integer, String, Date, DateTime,
    ForeignKey
)
from sqlalchemy.orm import mapper, relationship, synonym

from podcast import Author
from podcast.domainmodel import model
from podcast.domainmodel.model import Episode, Podcast

# global variable giving access to the MetaData (schema) information of the database
metadata = MetaData()

users_table = Table(
    'users', metadata,
    Column('id', Integer, primary_key=True, autoincrement=True),
    Column('username', String(255), unique=True, nullable=False),
    Column('password', String(255), nullable=False)
)

podcasts_table = Table(
    'podcasts', metadata,
    Column('id', Integer, primary_key=True, autoincrement=True),
    Column('author_id', ForeignKey('authors.id')),
    Column('title', String(255), nullable=False),
    Column('image', String(255), nullable=False),
    Column('description', String(1024), nullable=False),
    Column('language', String(255), nullable=False),
    Column('website', String(255), nullable=False),
    Column('itunes_id', Integer, nullable=False),
)

episodes_table = Table(
    'episodes', metadata,
    Column('id', Integer, primary_key=True, autoincrement=True),
    Column('podcast_id', ForeignKey('podcasts.id')),
    Column('title', String(255), nullable=False),
    Column('link', String(255), nullable=False),
    Column('length', Integer, nullable=False),
    Column('date', String(255), nullable=False),
    Column('description', String(1024), nullable=False),
)

playlists_table = Table(
    'playlists', metadata,
    Column('id', Integer, primary_key=True, autoincrement=True),
    Column('user_id', ForeignKey('users.id')),
)

authors_table = Table(
    'authors', metadata,
    Column('id', Integer, primary_key=True, autoincrement=True),
    Column('name', String(64), nullable=False)
)

reviews_table = Table(
    'reviews', metadata,
    Column('id', Integer, primary_key=True, autoincrement=True),
    Column('user_id', ForeignKey('users.id'), nullable=False),
    Column('podcast_id', ForeignKey('podcasts.id'), nullable=False),
    Column('content', String(1024), nullable=False),
    Column('rating', Integer, nullable=False)
)

categories_table = Table(
    'categories', metadata,
    Column('id', Integer, primary_key=True, autoincrement=True),
    Column('name', String(64), nullable=False),
)

podcast_categories_table = Table(
    'podcast_categories', metadata,
    Column('id', Integer, primary_key=True, autoincrement=True),
    Column('podcast_id', ForeignKey('podcasts.id')),
    Column('category_id', ForeignKey('categories.id'))
)

podcast_playlists_table = Table(
    'podcast_playlists', metadata,
    Column('id', Integer, primary_key=True, autoincrement=True),
    Column('podcast_id', ForeignKey('podcasts.id')),
    Column('playlist_id', ForeignKey('playlists.id'))
)

episode_playlists_table = Table(
    'episode_playlists', metadata,
    Column('id', Integer, primary_key=True, autoincrement=True),
    Column('episode_id', ForeignKey('episodes.id')),
    Column('playlist_id', ForeignKey('playlists.id'))
)

def map_model_to_tables():
    mapper(model.Podcast, podcasts_table, properties={
        '_Podcast__id': podcasts_table.c.id,
        '_Podcast__author': relationship(model.Author, backref='Author.id'),
        '_Podcast__title': podcasts_table.c.title,
        '_Podcast__image': podcasts_table.c.image,
        '_Podcast__description': podcasts_table.c.description,
        '_Podcast__language': podcasts_table.c.language,
        '_Podcast__website': podcasts_table.c.website,
        '_Podcast__itunes_id': podcasts_table.c.itunes_id,
        'episodes': relationship(model.Episode, backref='Episode.id'),
        'categories': relationship(model.Category, secondary=podcast_categories_table,
                                   back_populates='_Category__podcast'),
        '_Podcast__playlists': relationship(model.Playlist, secondary=podcast_playlists_table,
                                            back_populates='podcasts')
    })
    mapper(model.Episode, episodes_table, properties={
        'id': episodes_table.c.id,
        'title': episodes_table.c.title,
        'link': episodes_table.c.link,
        'length': episodes_table.c.length,
        'description': episodes_table.c.description,
        'date': episodes_table.c.date,
        '_Episode__playlists': relationship(model.Playlist, secondary=episode_playlists_table,
                                            back_populates='episodes')
    })

    mapper(model.User, users_table, properties={
        '_User__id': users_table.c.id,
        '_User__username': users_table.c.username,
        '_User__password': users_table.c.password,
    })
    mapper(model.Review, reviews_table, properties={
        'id': reviews_table.c.id,
        'content': reviews_table.c.content,
        'user': relationship(model.User, backref='user_review'),
        'podcast_id': reviews_table.c.podcast_id,
        'rating': reviews_table.c.rating,
    })
    mapper(model.Author, authors_table, properties={
        '_Author__id': authors_table.c.id,
        '_Author__name': authors_table.c.name,
    })

    mapper(model.Playlist, playlists_table, properties={
        'id': playlists_table.c.id,
        'user': relationship(model.User, backref='user_playlist'),
        'podcasts': relationship(model.Podcast, secondary=podcast_playlists_table,
                                 back_populates='_Podcast__playlists'),
        'episodes': relationship(model.Episode, secondary=episode_playlists_table,
                                 back_populates='_Episode__playlists')
    })
    mapper(model.Category, categories_table, properties={
        '_Category__id': categories_table.c.id,
        'name': categories_table.c.name,
        '_Category__podcast': relationship(model.Podcast, secondary=podcast_categories_table,
                                           back_populates='categories')
    })