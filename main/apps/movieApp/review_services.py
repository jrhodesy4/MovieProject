from ..User_app.models import User, Friend, ProPicture
from .models import MovieReview, TVReview, EpisodeReview, UserReview

from . import movie_services

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


def all_media_reviews(id, _type): #<-- this functions gets all the reviews for the movie page just enter the id of the movie
    if _type == "movie":

        reviews = []
        movie = movie_services.get_movie(id)
        start_reviews = MovieReview.objects.filter(api_code=id)
        for review in start_reviews:
            user_id = review.user_id
            user = User.objects.get(id=user_id)
            fullname = User.Fullname_toString(user)
            f_name = user.first_name
            l_name = user.last_name
            user_id = user.id
            try :
                pic = ProPicture.objects.get(user_id=user.id)
                profile_pic = pic.picture
                is_pic = True
            except:
                profile_pic = f_name[0] + l_name[0]
                is_pic = False
            data = {
                "user_name": fullname,
                "title": review.title,
                "type": "movie",
                "media_code": review.api_code,
                "score": review.score,
                "content": review.content,
                "created_at": review.created_at,
                "poster_path": review.poster_path,
                'story_rating':review.story_rating,
                'entertainment_rating': review.entertainment_rating,
                'acting_rating': review.acting_rating,
                'visual_rating': review.visual_rating,
                'sound_rating' : review.sound_rating,
                'reviewer_id': user_id,
                "profile_pic": profile_pic,
                "is_pic": is_pic,
                "overall_color": ovScoreColor(review.score),
                'story_percent': subPercent(review.story_rating),
                'story_color': subScoreColor(review.story_rating),
                'ent-percent': subPercent(review.entertainment_rating),
                'ent_color': subScoreColor(review.entertainment_rating),
                'act_percent': subPercent(review.acting_rating),
                'act_color': subScoreColor(review.acting_rating),
                'vis_percent': subPercent(review.visual_rating),
                'vis_color': subScoreColor(review.visual_rating),
                'sound_percent': subPercent(review.sound_rating),
                'sound_color': subScoreColor(review.sound_rating),
            }
            reviews.append(data)
        reviews.sort(key=lambda item:item['created_at'], reverse=True)
        return reviews
    else:
        reviews = []
        movie = movie_services.get_show(id)
        start_reviews = TVReview.objects.filter(api_code=id)
        for review in start_reviews:
            user_id = review.user_id
            user = User.objects.get(id=user_id)
            fullname = User.Fullname_toString(user)
            f_name = user.first_name
            l_name = user.last_name
            user_id = user.id
            try :
                pic = ProPicture.objects.get(user_id=user.id)
                profile_pic = pic.picture
                is_pic = True
            except:
                profile_pic = f_name[0] + l_name[0]
                is_pic = False
            data = {
                "user_name": fullname,
                "title": review.title,
                "type": "tv",
                "media_code": review.api_code,
                "score": review.score,
                "content": review.content,
                "created_at": review.created_at,
                "poster_path": review.poster_path,
                'story_rating':review.story_rating,
                'entertainment_rating': review.entertainment_rating,
                'acting_rating': review.acting_rating,
                'visual_rating': review.visual_rating,
                'sound_rating' : review.sound_rating,
                'reviewer_id': user_id,
                "profile_pic": profile_pic,
                "is_pic": is_pic,
                "overall_color": ovScoreColor(review.score),
                'story_percent': subPercent(review.story_rating),
                'story_color': subScoreColor(review.story_rating),
                'ent-percent': subPercent(review.entertainment_rating),
                'ent_color': subScoreColor(review.entertainment_rating),
                'act_percent': subPercent(review.acting_rating),
                'act_color': subScoreColor(review.acting_rating),
                'vis_percent': subPercent(review.visual_rating),
                'vis_color': subScoreColor(review.visual_rating),
                'sound_percent': subPercent(review.sound_rating),
                'sound_color': subScoreColor(review.sound_rating),
            }
            reviews.append(data)
        reviews.sort(key=lambda item:item['created_at'], reverse=True)
        return reviews




def sort_reviews_media(user_id, id, _type):
    user = User.objects.get(id=user_id)

    friends = Friend.objects.get(current_user=user)


    full_reviews = all_media_reviews(id, _type)
    friend_reviews = []
    other_reviews = []
    total_score = 0
    total_reviews = len(full_reviews)

    if friends == '[]':

        other_reviews = full_reviews
    else:
        for review in full_reviews:
            total_score = total_score + int(review['score'])

            try:
                this = Friend.objects.filter(users__id=review['reviewer_id'])
                print "succed to get friend"
                friend_reviews.append(review)
            except:
                other_reviews.append(review)
                print "failed to get friend"


    if total_reviews == 0:
        avg_color = 'grey'
        avg = 'n/a'
    else:
        avg = total_score/total_reviews
        avg_color = ovScoreColor(avg)
    data = {
        "friend_reviews": friend_reviews,
        "reviews": other_reviews,
        "avg_score": avg,
        "avg_color": avg_color
    }

    return data
