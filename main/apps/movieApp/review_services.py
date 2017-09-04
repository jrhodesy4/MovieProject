from ..User_app.models import User
from .models import MovieReview, TVReview, EpisodeReview, UserReview
from . import movie_services


def all_movie_reviews(id):
    reviews = []
    movie = movie_services.get_movie(id)
    start_reviews = MovieReview.objects.filter(api_code=id)
    for review in start_reviews:
        user_id = review.user_id
        user = User.objects.get(id=user_id)
        fullname = User.Fullname_toString(user)
        data = {
            "user_name": fullname,
            "score": review.score,
            "content": review.content,
            "date": review.created_at,
        }
        reviews.append(data)
    reviews.sort(key=lambda item:item['date'], reverse=True)
    return reviews
