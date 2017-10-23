from django.shortcuts import render, redirect, HttpResponse
from . import services
from ..User_app import user_services
from ..User_app.models import User, Profile, Friend
from ..movieApp.models import Watchlist
# from ..movieApp.models import
from ..User_app import views
from django.views.generic.edit import FormView
from datetime import datetime, timedelta
import math
from django.core import serializers
from django.http import JsonResponse
import json
import requests



# Create your views here.
"""
api key = 286abf6056d0a1338f772d1b7202e728
"""
# local fucntions here ===============================================
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

def createReviewFormat(review):
    now = datetime.now()
    new_timestamp = review['created_at'].replace(tzinfo=None)
    difference = now - new_timestamp
    minute_difference = int(difference.total_seconds() / 60)
    hour_difference = int(difference.total_seconds() / 3600)
    day_difference = int(difference.days)
    week_difference = int(difference.days / 7)
    month_difference = int(difference.days / 30)
    year_difference = int(month_difference / 12)
    data = {
        "poster_path": review['poster_path'],
        "backdrop_path": review['backdrop_path'],
        "title": review['title'],
        "overall_score": review['score'],
        "overall_color": ovScoreColor(review['score']),
        "story_rating": review['story_rating'],
        'story_percent': subPercent(review['story_rating']),
        'story_color': subScoreColor(review['story_rating']),
        'ent_percent': subPercent(review['entertainment_rating']),
        'ent_color': subScoreColor(review['entertainment_rating']),
        "entertainment_rating": review['entertainment_rating'],
        'act_percent': subPercent(review['acting_rating']),
        'act_color': subScoreColor(review['acting_rating']),
        "acting_rating": review['acting_rating'],
        'vis_percent': subPercent(review['visual_rating']),
        'vis_color': subScoreColor(review['visual_rating']),
        "visual_rating": review['visual_rating'],
        'sound_percent': subPercent(review['sound_rating']),
        'sound_color': subScoreColor(review['sound_rating']),
        "sound_rating": review['sound_rating'],
        'minute_difference': minute_difference,
        'hour_difference': hour_difference,
        'day_difference': day_difference,
        'week_difference': week_difference,
        'month_difference' : month_difference,
        'year_difference': year_difference,
    }

    return data



def search(request):
    search = request.GET.get('search-info')
    result = services.search_database(search)
    return JsonResponse(result, safe=False)
    # return HttpResponse(serializers.serialize("json", final), content_type='application/json')


def index(request):
    if "user" not in request.session:
        return redirect('/login')
    if "user" in request.session :
        status = 'You are logged in'
    user_id = request.session['user']

    #this is for the reviews
    try:
        reviews = user_services.get_feed_reviews(user_id)
    except:
        reviews = "none";

    final_form_reviews =[] # <-- this returns the reviews and makes them formated correctly
    for review in reviews:
        data = createReviewFormat(review);
        final_form_reviews.append(data)

    #this is for the watchlist
    user = User.objects.get(id=user_id)
    my_watchlist = Watchlist.objects.filter(user=user)


    url = "https://api.themoviedb.org/3/discover/movie?api_key=286abf6056d0a1338f772d1b7202e728&language=en-US&sort_by=popularity.desc&include_adult=false&include_video=false&page=1"
    json_data = requests.get(url).json()


    slideshow = []
    movies = json_data['results']
    for x in range(0,10):
        if x == 0:
            current_status = "active"
        else:
            current_status = "non-active"

        placement = "index-" + str(x)

        current_data = {
            "title": movies[x]['title'],
            "backdrop_path":  movies[x]['backdrop_path'],
            "poster_path":  movies[x]['poster_path'],
            "id":  movies[x]['id'],
            "status":  current_status,
            "placement":  placement,
        }
        slideshow.append(current_data)



    data = {
        "reviews": final_form_reviews,
        "watchlist": my_watchlist,
        "slideshow": slideshow
    }

    return render(request, 'homeApp/index.html', data)




def get_places(request):
    if request.is_ajax():
        q = request.GET.get('term', '')
        users = User.objects.filter(first_name__icontains = q )|User.objects.filter(last_name__icontains = q)
        users = users[:20]
        results = []
        for user in users:
            user_json = {}
            user_json['id'] = user.id
            user_json['label'] = user.first_name + " " + user.last_name
            user_json['value'] = user.first_name
            results.append(user_json)
        data = json.dumps(results)
    else:
        data = 'fail'
    mimetype = 'application/json'
    print data
    print "here"
    return HttpResponse(data, mimetype)

def searchUsers(request):
    if request.method == 'POST':
        count = User.objects.filter(first_name__icontains=request.POST['person']).count()
        users = User.objects.filter(first_name__icontains=request.POST['person'])
        print users
        return render(request, 'homeApp/search.html', {'users' : users, 'count' : count})

# def get_places(request):
#   if request.is_ajax():
#     q = request.GET.get('term', '')
#     users = User.objects.filter(first_name__icontains=q)
#     results = []
#     for user in users:
#       user_json = {}
#       user_json['id'] = user.id
#       user_json['label'] = user.first_name
#       user_json['value'] = user.first_name
#       results.append(user_json)
#     data = json.dumps(results)
#   else:
#     data = 'fail'
#   mimetype = 'application/json'
#   return HttpResponse(data, mimetype)


# class AutoCompleteView(FormView):
#     def get(self,request,*args,**kwargs):
#         data = request.GET
#         username = data.get("term")
#         if username:
#             users = User.objects.get(username__icontains = username)
#         else:
#             users = User.objects.all()
#         results = []
#         for user in users:
#             user_json = {}
            # user_json['id'] = user.id
            # user_json['label'] = user.first_name
            # user_json['value'] = user.first_name
#             results.append(user_json)
#             data = json.dumps(results)
#             mimetype = 'application/json'
#             return HttpResponse(data, mimetype)
