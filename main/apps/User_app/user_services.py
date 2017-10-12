from .models import User, Profile, Friend, Notification
from ..movieApp.models import Watchlist, UserReview, MovieReview, TVReview, EpisodeReview



def get_feed_reviews(user_id): #<--- this gets reviews for all friends in list and sort them acordingly
    final_list = []
    user = User.objects.get(id=user_id)
    friends = Friend.objects.get(current_user=user)
    feed_list = []
    for friend in friends.users.all():

        f_reviews = get_reviews(friend.id)
        for rev in f_reviews:
            feed_list.append(rev)
    feed_list.sort(key=lambda item:item['created_at'], reverse=True) #<--puts into int order created by
    return feed_list




def get_reviews(user_id): #<--- this function should get all reviews with a account and put them into uniform
    user = User.objects.get(id=user_id)
    reviews = []
    a = MovieReview.objects.filter(movies__user_id=user)
    for this in a:
        entry = { #<--- this should be added too when more info is needed for template
            "title": this.title,
            "score": this.score,
            "content": this.content,
            "created_at": this.created_at,
            "poster_path": this.poster_path,
            'story_rating': this.story_rating,
            'entertainment_rating': this.entertainment_rating,
            'acting_rating': this.acting_rating,
            'visual_rating': this.visual_rating,
            'sound_rating' : this.sound_rating
        }
        reviews.append(entry)
    b = TVReview.objects.filter(tvs__user_id=user)
    for this in b:
        entry = {
            "title": this.title,
            "score": this.score,
            "content": this.content,
            "created_at": this.created_at,
            "poster_path": this.poster_path,
            'story_rating': this.story_rating,
            'entertainment_rating': this.entertainment_rating,
            'acting_rating': this.acting_rating,
            'visual_rating': this.visual_rating,
            'sound_rating' : this.sound_rating
        }
        reviews.append(entry)
    c = EpisodeReview.objects.filter(episodes__user_id=user)
    for this in c:
        entry = {
            "title": this.episode_title,
            "score": this.score,
            "content": this.content,
            "created_at": this.created_at,
            "poster_path": this.poster_path,
            'story_rating': this.story_rating,
            'entertainment_rating': this.entertainment_rating,
            'acting_rating': this.acting_rating,
            'visual_rating': this.visual_rating,
            'sound_rating' : this.sound_rating
        }
        reviews.append(entry)
    reviews.sort(key=lambda item:item['created_at'], reverse=True)
    return reviews
