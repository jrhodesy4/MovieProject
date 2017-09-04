from .models import User, Profile, Friend, Notification
from ..movieApp.models import Watchlist, UserReview, MovieReview, TVReview, EpisodeReview



def get_reviews():
    reviews = []
    user = User.objects.get(id = request.session['user'])
    return 
