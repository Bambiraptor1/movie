from flask import Blueprint, render_template, request
from movie.extensions import db
from movie.models import Movie, Type

core_bp = Blueprint('core', __name__, template_folder='templates')

@core_bp.route('/')
def index():
  page = request.args.get('page', type=int)
  movies = db.paginate(db.select(Movie), per_page=4, page=page)
  return render_template('core/index.html',
                         title='Home Page',
                         movies=movies)


@core_bp.route('/<int:id>/detail')
def detail(id):
  query = db.select(Movie).where(Movie.id==id)
  movie = db.session.scalar(query)
  return render_template('core/movie_detail.html',
                         title='Movie Detail Page',
                         movie=movie)