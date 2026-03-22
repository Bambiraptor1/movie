import os
from flask import Flask
from movie.extensions import db, login_manager, bcrypt
from movie.models import User, Movie, Type
from movie.core.routes import core_bp
from movie.users.routes import user_bp
from movie.movie.routes import movie_bp

def create_app():
  app = Flask(__name__)
  app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL')
  app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY')

  db.init_app(app)
  bcrypt.init_app(app)
  login_manager.init_app(app)
  login_manager.login_view = 'user.login'
  login_manager.login_message = 'Please log in to access this page.'
  login_manager.login_message_category = 'warning'

  app.register_blueprint(core_bp, url_prefix='/')
  app.register_blueprint(user_bp, url_prefix='/users')
  app.register_blueprint(movie_bp, url_prefix='/movies')

  return app