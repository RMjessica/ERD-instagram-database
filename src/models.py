import os
import sys
from sqlalchemy import Column, ForeignKey, Integer, String, PrimaryKeyConstraint
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine
from eralchemy import render_er


def get_current_date():
    return datetime.now().strftime("%d-%m-%Y")


Base = declarative_base()


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    full_name = Column(String(20), nullable=False)
    username = Column(String(20), unique=True, nullable=False)
    email = Column(String(40), unique=True, nullable=False)
    password = Column(Integer, nullable=False)
    creation_date = Column(
        String(10), default=get_current_date, nullable=False)

    post = relationship('Post', back_populates='user')
    comment = relationship('Comment', back_populates='user')
    favorite = relationship('Favorite', back_populates='user')


class Post(Base):
    __tablename__ = 'posts'

    id = Column(Integer, primary_key=True)
    creation_date = Column(
        String(10), default=get_current_date, nullable=False)

    user_id = Column(Integer, ForeignKey('users.id'))
    user = relationship('User', back_populates='post')

    media = relationship('Media', back_populates='post')
    favorite = relationship('Favorite', back_populates='post')
    comment = relationship('Comment', back_populates='post')


class Media(Base):
    __tablename__ = 'media'
    id = Column(Integer, primary_key=True)
    media_type = Column(String(50), nullable=False)
    media_url = Column(String(200), unique=True, nullable=False)

    post_id = Column(Integer, ForeignKey('posts.id'))
    post = relationship('Post', back_populates='media')


class Follower(Base):
    __tablename__ = 'followers'

    follower_id = Column(Integer, ForeignKey('users.id'), primary_key=True)
    following_id = Column(Integer, ForeignKey('users.id,'), primary_key=True)

    __table_args__ = (
        PrimaryKeyConstraint(following_id, follower_id),
        {},
    )

    follower = relationship("User", foreign_keys=[follower_id])
    following = relationship("User", foreign_keys=[following_id])


class Comment(Base):
    __tablename__ = 'comments'
    id = Column(Integer, primary_key=True)
    comment = Column(String(400), nullable=False)

    user_id = Column(Integer, ForeignKey('users.id'))
    user = relationship('User', back_populates='comment')

    post_id = Column(Integer, ForeignKey('posts.id'))
    post = relationship('Post', back_populates='comment')


class Favorite(Base):
    __tablename__ = 'favorites'
    id = Column(Integer, primary_key=True)

    user_id = Column(Integer, ForeignKey('users.id'))
    user = relationship('User', back_populates='favorite')

    post_id = Column(Integer, ForeignKey('posts.id'))
    post = relationship('Post', back_populates='favorite')

    def to_dict(self):
        return {}


# Draw from SQLAlchemy base
try:
    result = render_er(Base, 'diagram.png')
    print("Success! Check the diagram.png file")
except Exception as e:
    print("There was a problem genering the diagram")
    raise e
