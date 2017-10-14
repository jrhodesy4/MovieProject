from django.shortcuts import render, redirect
from . import movie_services, review_services
from ..homeApp import services
from .models import Watchlist
from ..User_app.models import User
from ..movieApp.models import MovieReview, TVReview, EpisodeReview, UserReview

from django.core import serializers
from django.http import JsonResponse
import json
import requests
from datetime import datetime
import math

# from ..homeApp import services

# custom defintions here =======================
def authenticate(request): #<----- this is to tell whether the user is logged in or not
    if 'user' in request.session:
        return "in"
    else:
        return "out"

def in_watchlist(user_id, id): #<----- if media is in the user watchlist returns boolean
    user = User.objects.get(id=user_id)
    try:
        Watchlist.objects.get(user__id=user.id, api_code=id)
        return True
    except:
        return False

def review_completed(user_id, id, _type): #<----- if the user has completed a review for item returns boolean
    if _type == "movie":
        try:
            review = MovieReview.objects.get(api_code=id, user_id=user_id)
            print "user has already written a review"
            return review.score
        except:
            return "no score"
    if _type == "tv":
        try:
            review = TVReview.objects.get(api_code=id, user_id=user_id)
            print "user has already written a review"
            return review.score
        except:
            return "no score"
    if _type == "episode":
        try:
            review = EpisodeReview.objects.get(api_code=id, user_id=user_id)
            print "user has already written a review"
            return review.score
        except:
            return "no score"

# Create your views here.=======================
# =====================================================================
# =====================================================================


def movie_page(request, id): # this renders the selected individual movie page
    in_list = False
    status = authenticate(request)
    try:
        trailers = movie_services.get_videos(id, 'movie')
    except:
        trailers = 'none'
    review_c = False
    if status == "in":
        user_id = request.session['user']
        in_list = in_watchlist(user_id, id)
        score = review_completed(user_id, id, "movie")
    else:
        score = "not logged"
    user = request.session['user']

    review_data = review_services.sort_reviews_media(user, id, "movie")


    #below is info for each movie
    movie = movie_services.get_movie(id)
    mov = movie['movie_info']
    budget = format(mov['budget'], ",d")
    revenue = format(mov['revenue'], ",d")
    date = datetime.strptime(mov['release_date'], '%Y-%m-%d')
    release = date.strftime('%b %d, %Y')
    time = mov['runtime'];
    hours = int(math.floor(time / 60));
    minutes = (time % 60);
    runtime = [hours, minutes]
    genres = mov['genres']
    genre_names = []
    for genre in genres:
        genre_names.append(genre['name'])

    try:
        watchlist = Watchlist.objects.get(api_code=id)
    except: watchlist = 'nothing'

    color = "red"
    if score > 60:
        color = "yellow"
    if score > 80:
        color = 'green'


    context = { #<-- info that goes to template
        'movie': movie['movie_info'],
        "genre_names" : genre_names,
        'budget': budget,
        'release': release,
        'revenue': revenue,
        'trailers': trailers,
        'cast': movie['cast_info'],
        'in_list': in_list,
        'score': score,
        'score_color': color,
        'runtime' : runtime,
        'reviews': review_data['reviews'],
        'friend_reviews': review_data['friend_reviews'],
        'avg_score': review_data['avg_score'],
        'avg_score_color': review_data['avg_color'],
    }
    print context['friend_reviews']
    return render(request, 'movieApp/movie_view_page.html', context)




def seasonData(request):
    seasonId = request.GET.get('id')
    seasonNum = request.GET.get('season')
    print request
    print "here"
    result = movie_services.get_season(seasonId, seasonNum)
    return JsonResponse(result, safe=False);


def show_page(request, id):
    in_list = False
    try:
        trailers = movie_services.get_videos(id, 'tv')
    except:
        trailers = 'none'
    print trailers
    status = authenticate(request)
    show = movie_services.get_show(id)

    in_list = False
    review_c = False
    if status == "in":
        user_id = request.session['user']
        in_list = in_watchlist(user_id, id)
        score = review_completed(user_id, id, "tv")
    else:
        score = "not logged"
    user = request.session['user']
    color = "red"
    if score > 60:
        color = "yellow"
    if score > 80:
        color = 'green'


    review_data = review_services.sort_reviews_media(user, id, "tv")
    context = {
        "show": show['show_info'],
        'cast': show['cast_info'],
        'trailers': trailers,
        "in_list": in_list,
        'score': score,
        'score_color': color,
        'reviews': review_data['reviews'],
        'friend_reviews': review_data['friend_reviews'],
        'avg_score': review_data['avg_score'],
        'avg_score_color': review_data['avg_color'],

    }
    return render(request, 'movieApp/tv_view_page.html', context)






def movie_home(request):
    result = services.get_discover()
    return render(request, 'movieApp/movies_home.html', {'result' : result})

def tv_home(request):
    shows = movie_services.popular_tv()
    return render(request, 'movieApp/tv_home.html', {'shows': shows})


def actor_home(request):
    actors = movie_services.popular_actors()
    return render(request, 'movieApp/actors_home.html', {'actors': actors})

def show_season(request, id, season):
    print 'here'
    tv_season = movie_services.get_season(id, season)
    print tv_season
    id = id
    season = season
    return render(request, 'movieApp/season_page.html', {'tv_season': tv_season, 'id' : id, 'season': season})

def show_episode(request, id, season, episode):
    tv_episode = movie_services.get_episode(id, season, episode)
    status = authenticate(request)
    review_c = False
    if status == "in":
        user_id = request.session['user']
        review_c = review_completed(user_id, id, "episode")

    context = {
        'tv_episode': tv_episode,
        "id": id,
        "season": season,
        "episode": episode,
        'completed': review_c
    }
    return render(request, 'movieApp/episode_page.html', context)



def cast_page(request, id): # this render the info page for the individual actor
    person_info = movie_services.get_person(id)
    person = {
        'details': person_info['details'],
        'credits': person_info['credits']
    }

    return render(request, 'movieApp/actor_view_page.html', person )


def discover(request):
    discover = movie_services.get_discover()
    movies = movie_services.popular_movies()
    tv = movie_services.popular_tv()
    actor = movie_services.popular_actors()

    data = {
        "discover": discover,
        "movies": movies,
        "tvs": tv,
        "actors": actor
    }

    return render(request, 'movieApp/discover.html', data)


def discover_more(request, id):


    # this needs tp be more efficent

    if id == "1":
        pagetitle = "Now playing"
        movies = movie_services.get_full_nowplaying("now_playing")
        pagetype = "movie"
    if id == '2':
        pagetitle = "Top Movies"
        movies = movie_services.get_full_nowplaying("top-movies")
        pagetype = "movie"
    if id == '3':
        pagetitle = "Popular"
        movies = movie_services.get_full_nowplaying("popularM")
        pagetype = "movie"
    if id == '4':
        pagetitle = "On Air"
        movies = movie_services.get_full_nowplaying("onair")
        pagetype = "tv"
    if id == '5':
        pagetitle = "Top Rated"
        movies = movie_services.get_full_nowplaying("top-tv")
        pagetype = "tv"
    if id == '6':
        pagetitle = "Popular"
        movies = movie_services.get_full_nowplaying("actors")
        pagetype = "actors"
    # else :
    #     pagetitle = "Popular"
    #     movies = movie_services.get_full_nowplaying("popularM")
    #     pagetype = "actor"
    print movies
    data = {
        "pagetype": pagetype,
        "pagetitle": pagetitle,
        "movies": movies
    }
    return render(request, "movieApp/discover_more.html", data)




# ===========================
#Post Routes
# ===========================

def add_to_watchlist(request): # the post route adds a movie to the Users watchlist

    _type = request.GET.get('type')
    _id = request.GET.get('id')

    if _type == "movie":
        movie = movie_services.get_movie(_id)
        data = {
            "movie": movie['movie_info'], # this is the data for the current movie being displayed
            "user_id": request.session['user'], # the logged in user id from session
            "type": "movie" # whether it is a movie or tv show
        }
        Watchlist.add_movie(data) # add movie to Watchlist

    if _type == "tv":
        show = movie_services.get_show(_id)
        data = {
            "movie": show['show_info'], # this is the data for the current movie being displayed
            "user_id": request.session['user'], # the logged in user id from session
            "type": "tv" # whether it is a movie or tv show
        }
        Watchlist.add_movie(data) # add movie to Watchlist

    result = {"added": True}
    return JsonResponse(result, safe=False)


def delete_from_watchlist(request, id):
    delete_me = Watchlist.objects.get(id=id)
    delete_me.delete()
    return redirect("/")


def makeReview(request, id, season, episode):
    if 'user' not in request.session:
        data = {"score": "N/A"}
        return JsonResponse(data, safe=False)

    user_id = request.session['user']
    data = {
        "id": id,
        "content": request.POST['content'],
        "score": request.POST['score'],
        "user_id": user_id,
        "story_rating": request.POST['story'],
        "entertainment_rating": request.POST['entertainment'],
        "acting_rating": request.POST['acting'],
        "visual_rating": request.POST['visual'],
        "sound_rating": request.POST['sound'],
    }


    if request.POST['type'] == "movie":
        mr = MovieReview.create_review(data)
        if mr == None:
            data = {"score": request.POST['score']}
            return JsonResponse(data, safe=False)
        else:
            UserReview.add_review(mr, "movie", user_id)
            data = {"score": request.POST['score']}
            return JsonResponse(data, safe=False)

    if request.POST['type'] == "tv":
        tr = TVReview.create_review(data)
        if tr == None:
            data = {"score": request.POST['score']}
            return JsonResponse(data, safe=False)
        else:
            UserReview.add_review(tr, "tv", user_id)
            data = {"score": request.POST['score']}
            return JsonResponse(data, safe=False)

    if request.POST['type'] == "episode":
        print "episode"
        data = {
            "id": id,
            "season": season,
            "episode": episode,
            "content": request.POST['content'],
            "score": request.POST['score'],
            "user_id": user_id,
            "story_rating": request.POST['story'],
            "entertainment_rating": request.POST['entertainment'],
            "acting_rating": request.POST['acting'],
            "visual_rating": request.POST['visual'],
            "sound_rating": request.POST['sound'],

        }
        epi = EpisodeReview.create_review(data)
        if epi == None:
            data = {"score": request.POST['score']}
            return JsonResponse(data, safe=False)
        else:
            UserReview.add_review(epi, "episode", user_id)
            data = {"score": request.POST['score']}
            return JsonResponse(data, safe=False)













# end
