from .models import User, Profile, Friend, Notification
from ..movieApp.models import Watchlist, UserReview, MovieReview, TVReview, EpisodeReview


def get_reviews(user_id):
    user = User.objects.get(id=user_id)
    reviews = []
    a = MovieReview.objects.filter(movies__user_id=user)
    for this in a:
        entry = {
            "title": this.title,
            "score": this.score,
            "content": this.content,
            "created_at": this.created_at,
            "poster": poster_path
        }
        reviews.append(entry)
    b = TVReview.objects.filter(tvs__user_id=user)
    for this in b:
        entry = {
            "title": this.title,
            "score": this.score,
            "content": this.content,
            "created_at": this.created_at,
        }
        reviews.append(entry)
    c = EpisodeReview.objects.filter(episodes__user_id=user)
    for this in c:
        entry = {
            "title": this.episode_title,
            "score": this.score,
            "content": this.content,
            "created_at": this.created_at,
        }
        reviews.append(entry)

    return reviews
