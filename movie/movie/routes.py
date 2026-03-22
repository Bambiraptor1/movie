from flask import Blueprint, render_template, url_for, redirect, flash, request
from movie.extensions import db
from movie.models import User, Movie, Type
from flask_login import current_user, login_required

movie_bp = Blueprint('movie', __name__, template_folder='templates')

@movie_bp.route('/')
def index():
  query = db.select(Movie).where(Movie.user == current_user)
  movies = db.session.scalars(query).all()
  return render_template('movie/index.html', 
                         title='Movie Page',
                         movies=movies)

@movie_bp.route('/new', methods=['GET', 'POST'])
def new_movie():
  query = db.select(Type)
  movie_types = db.session.scalars(query).all()
  if request.method == 'POST':
    name = request.form.get('name')
    reslease_year = request.form.get('release_year')
    director = request.form.get('director')
    description = request.form.get('description')
    img_url = request.form.get('img_url')
    types = request.form.getlist('movie_types')
    user_id = current_user.id

    p_types = []
    for id in types:
      p_types.append(db.session.get(Type, id))

    movie = Movie(
      name=name,
      release_year=reslease_year,
      director=director,
      description=description,
      img_url=img_url,
      user_id=user_id,
      types=p_types
    )
    db.session.add(movie)
    db.session.commit()
    flash('Add new movie successful!', 'success')
    return redirect(url_for('movie.index'))

  return render_template('movie/new_movie.html', 
                         title='New Movie Page',
                         movie_types=movie_types)

@movie_bp.route('/<int:id>/edit', methods=['GET', 'POST'])
@login_required
def edit_movie(id):
    movie = Movie.query.get_or_404(id)

    if movie.user_id != current_user.id:
        flash("You don't have permission to edit this movie.", "danger")
        return redirect(url_for('movie.index'))

    all_types = Type.query.all()

    if request.method == 'POST':
        movie.name = request.form['name']
        movie.description = request.form['description']
        movie.release_year = request.form.get('release_year', type=int)
        movie.director = request.form['director']
        movie.img_url = request.form['img_url']

        type_ids = request.form.getlist('movie_types') 
        movie.types = Type.query.filter(Type.id.in_(type_ids)).all()

        db.session.commit()
        flash("Movie updated successfully!", "success")
        return redirect(url_for('movie.index'))

    return render_template('movie/edit_movie.html', movie=movie, movie_types=all_types)

@movie_bp.route('/<int:id>/delete', methods=['POST'])
def delete_movie(id):
  movie = db.session.get(Movie, id)
  if movie:
    db.session.delete(movie)
    db.session.commit()
    flash('Delete movie successful!', 'success')
  else:
    flash('Movie not found!', 'warning')
  return redirect(url_for('movie.index'))

@movie_bp.route('/search')
def search_movie():
    q = request.args.get('q', '')  
    movies = []

    if q:
        query = db.select(Movie).where(Movie.name.ilike(f'%{q}%'))
        movies = db.session.scalars(query).all()

    return render_template(
        'movie/search_results.html',
        title='ผลการค้นหา',
        movies=movies,
        q=q
    )

@movie_bp.route('/search-live')
def search_live_movie():
    q = request.args.get('q', '')
    movies = []

    if q and len(q) >= 1:
        query = db.select(Movie).where(Movie.name.ilike(f'%{q}%')).limit(5)
        movies = db.session.scalars(query).all()

    return render_template(
        'movie/search_dropdown.html',
        movies=movies,
        q=q
    )
