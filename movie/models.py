from movie.extensions import db, login_manager
from sqlalchemy import Integer, Text, String, DateTime, ForeignKey, Column, Table, func
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import List
from flask_login import UserMixin
from datetime import datetime

@login_manager.user_loader
def load_user(user_id):
  return db.session.get(User, int(user_id))

class User(db.Model, UserMixin):
  __tablename__ = 'user'
  id: Mapped[int] = mapped_column(Integer, primary_key=True)
  username: Mapped[str] = mapped_column(String(25), unique=True, nullable=False)
  email: Mapped[str] = mapped_column(String(50), unique=True, nullable=False)
  password: Mapped[str] = mapped_column(String(255), nullable=False)
  firstname: Mapped[str] = mapped_column(String(25), nullable=True)
  lastname: Mapped[str] = mapped_column(String(25), nullable=True)
  avatar: Mapped[str] = mapped_column(String(25), nullable=True, default='avatar.png')
  created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
  updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

  movies: Mapped[List['Movie']] = relationship(back_populates='user')
  def __repr__(self):
    return f'<User: {self.username}>'

movie_genre = Table(
    'movie_genre',    
    db.metadata,
    Column('movie_id', Integer, ForeignKey('movie.id'), primary_key=True),
    Column('genre_id', Integer, ForeignKey('type.id'), primary_key=True)
)

class Type(db.Model):
  __tablename__ = 'type'
  id: Mapped[int] = mapped_column(Integer, primary_key=True)
  name: Mapped[str] = mapped_column(String(25), unique=True, nullable=False)

  movies: Mapped[List['Movie']] = relationship(back_populates='types', secondary=movie_genre)
  def __repr__(self):
    return f'<Type: {self.name}>'
  
class Movie(db.Model):
  __tablename__ = 'movie'
  id: Mapped[int] = mapped_column(Integer, primary_key=True)
  name: Mapped[str] = mapped_column(String(30), unique=True, nullable=False)
  description: Mapped[str] = mapped_column(Text, nullable=False)
  release_year: Mapped[int] = mapped_column(Integer, nullable=True)
  director: Mapped[str] = mapped_column(String(50), nullable=True)
  img_url: Mapped[str] = mapped_column(String(255), nullable=False)
  user_id: Mapped[int] = mapped_column(Integer, ForeignKey(User.id))
  created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())

  user: Mapped[User] = relationship(back_populates='movies')
  types: Mapped[List[Type]] = relationship(back_populates='movies', secondary=movie_genre)

  def __repr__(self):
    return f'<Movie: {self.name}>'