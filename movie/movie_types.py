types = [
    'Drama', 'Adventure', 'Thriller', 'Crime', 'Action',
    'Comedy', 'Mystery', 'War', 'Fantasy', 'Sci-Fi', 'Family',
    'Romance', 'Animation', 'Biography', 'History', 'Horror',
    'Sport', 'Western', 'Music', 'Musical', 'Film-Noir'
]
from movie.models import Type
movie_types = [Type(name=mg) for mg in types]