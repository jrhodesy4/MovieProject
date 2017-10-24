from .models import User, Profile, Friend, Notification, ProPicture
from ..movieApp.models import Watchlist, UserReview, MovieReview, TVReview, EpisodeReview

def ovScoreColor(score): #gets the class we need for color == score
    color = "red"
    if score > 60:
        color = "yellow"
    if score > 80:
        color = 'green'
    return color

def subScoreColor(score):
     color = "red"
     if score > 6:
         color = "yellow"
     if score >= 8:
         color = 'green'
     return color

def subPercent(number): # this get the score and turns it to written number for class
    if number == None:
        return 5
    percent = ["one", "two", "three", "four",'five',' six', 'seven','eight', 'nine', 'ten']
    return percent[number - 1]

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

    f_name = user.first_name
    l_name = user.last_name
    fullname = str(f_name) + " " + str(l_name)
    user_id = user.id
    try :
        pic = ProPicture.objects.get(user_id=user.id)
        profile_pic = pic.picture
        is_pic = True
    except:
        profile_pic = f_name[0] + l_name[0]
        is_pic = False

    reviews = []
    a = MovieReview.objects.filter(movies__user_id=user)
    for this in a:
        entry = { #<--- this should be added too when more info is needed for template
            "title": this.title,
            "type": "movie",
            "media_code": this.api_code,
            "score": this.score,
            "content": this.content,
            "created_at": this.created_at,
            "poster_path": this.poster_path,
            'backdrop_path': this.backdrop_path,
            'story_rating': this.story_rating,
            'entertainment_rating': this.entertainment_rating,
            'acting_rating': this.acting_rating,
            'visual_rating': this.visual_rating,
            'sound_rating' : this.sound_rating,
            'reviewer_id': user_id,
            "profile_pic": profile_pic,
            "is_pic": is_pic,
            "reviewer_fullname": fullname,
            "overall_color": ovScoreColor(this.score),
            'story_percent': subPercent(this.story_rating),
            'story_color': subScoreColor(this.story_rating),
            'ent_percent': subPercent(this.entertainment_rating),
            'ent_color': subScoreColor(this.entertainment_rating),
            'act_percent': subPercent(this.acting_rating),
            'act_color': subScoreColor(this.acting_rating),
            'vis_percent': subPercent(this.visual_rating),
            'vis_color': subScoreColor(this.visual_rating),
            'sound_percent': subPercent(this.sound_rating),
            'sound_color': subScoreColor(this.sound_rating),
        }
        reviews.append(entry)
    b = TVReview.objects.filter(tvs__user_id=user)
    for this in b:
        entry = {
            "title": this.title,
            "type": "tv",
            "media_code": this.api_code,
            "score": this.score,
            "content": this.content,
            "created_at": this.created_at,
            "poster_path": this.poster_path,
            'backdrop_path': this.backdrop_path,
            'story_rating': this.story_rating,
            'entertainment_rating': this.entertainment_rating,
            'acting_rating': this.acting_rating,
            'visual_rating': this.visual_rating,
            'sound_rating' : this.sound_rating,
            'reviewer_id': user_id,
            "profile_pic": profile_pic,
            "is_pic": is_pic,
            "reviewer_fullname": fullname,
            "overall_color": ovScoreColor(this.score),
            'story_percent': subPercent(this.story_rating),
            'story_color': subScoreColor(this.story_rating),
            'ent_percent': subPercent(this.entertainment_rating),
            'ent_color': subScoreColor(this.entertainment_rating),
            'act_percent': subPercent(this.acting_rating),
            'act_color': subScoreColor(this.acting_rating),
            'vis_percent': subPercent(this.visual_rating),
            'vis_color': subScoreColor(this.visual_rating),
            'sound_percent': subPercent(this.sound_rating),
            'sound_color': subScoreColor(this.sound_rating),

        }
        reviews.append(entry)
    c = EpisodeReview.objects.filter(episodes__user_id=user)
    for this in c:
        entry = {
            "title": this.episode_title,
            "type": "tv",
            "media_code": this.api_code,
            "score": this.score,
            "content": this.content,
            "created_at": this.created_at,
            "poster_path": this.poster_path,
            'backdrop_path': this.backdrop_path,
            'story_rating': this.story_rating,
            'entertainment_rating': this.entertainment_rating,
            'acting_rating': this.acting_rating,
            'visual_rating': this.visual_rating,
            'sound_rating' : this.sound_rating,
            'reviewer_id': user_id,
            "profile_pic": profile_pic,
            "is_pic": is_pic,
            "reviewer_fullname": fullname,
            "overall_color": ovScoreColor(this.score),
            'story_percent': subPercent(this.story_rating),
            'story_color': subScoreColor(this.story_rating),
            'ent_percent': subPercent(this.entertainment_rating),
            'ent_color': subScoreColor(this.entertainment_rating),
            'act_percent': subPercent(this.acting_rating),
            'act_color': subScoreColor(this.acting_rating),
            'vis_percent': subPercent(this.visual_rating),
            'vis_color': subScoreColor(this.visual_rating),
            'sound_percent': subPercent(this.sound_rating),
            'sound_color': subScoreColor(this.sound_rating),

        }
        reviews.append(entry)
    reviews.sort(key=lambda item:item['created_at'], reverse=True)
    return reviews
