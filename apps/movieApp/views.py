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
from random import *

# from ..homeApp import services

# custom defintions here =======================
def authenticate(request): #<----- this is to tell whether the user is logged in or not
    if 'user' in request.session:
        return "in"
    else:
        return redirect('/login')

def in_watchlist(user_id, id): #<----- if media is in the user watchlist returns boolean
    user = User.objects.get(id=user_id)
    try:
        Watchlist.objects.get(user__id=user.id, api_code=id)
        return True
    except:
        return False

def review_completed(user_id, id, media_type): #<----- if the user has completed a review for item returns boolean
    if media_type == "movie":
        try:
            review = MovieReview.objects.get(api_code=id, user_id=user_id)
            return review.score
        except:
            return "no score"
    if media_type == "tv":
        try:
            review = TVReview.objects.get(api_code=id, user_id=user_id)
            return review.score
        except:
            return "no score"
    if media_type == "episode":
        try:
            review = EpisodeReview.objects.get(api_code=id, user_id=user_id)

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
    try:
        budget = format(mov['budget'], ",d")
    except:
        budget = 'None listed'
    try:
        revenue = format(mov['revenue'], ",d")
    except: revenue = "None listed"
    date = datetime.strptime(mov['release_date'], '%Y-%m-%d')
    try:
        release = date.strftime('%b %d, %Y')
    except:
        release = "None listed"
    try:
        time = mov['runtime'];
        hours = int(math.floor(time / 60));
        minutes = (time % 60);
    except:
        pass
    try:
        runtime = [hours, minutes]
    except:
        runtime = "None listed"
    try:
        genres = mov['genres']
        genre_names = []
        for genre in genres:
            genre_names.append(genre['name'])
    except:
        genre_names = ["none"]

    try:
        watchlist = Watchlist.objects.get(api_code=id)
    except: watchlist = 'nothing'

    color = "red"
    if score > 60:
        color = "yellow"
    if score > 80:
        color = 'green'

    # if review_data['friend_reviews']:
    screenwriters = []
    directors = []
    friend_reviews = review_data['friend_reviews']
    for crew in movie['cast_info']['crew']:
        if crew['job'] == 'Screenplay':
            screenwriters.append(crew)
        if crew['job'] == 'Director':
            directors.append(crew)

    # else:
    #     friend_reviews = 'no friends'
    context = { #<-- info that goes to template
        'movie': movie['movie_info'],
        "genre_names" : genre_names,
        "directors": directors,
        "screenwriters": screenwriters,
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
        'friend_reviews': friend_reviews,
        'avg_score': review_data['avg_score'],
        'avg_score_color': review_data['avg_color'],
    }


    return render(request, 'movieApp/movie_view_page.html', context)




def seasonData(request):
    seasonId = request.GET.get('id')
    seasonNum = request.GET.get('season')
    result = movie_services.get_season(seasonId, seasonNum)
    return JsonResponse(result, safe=False);


def show_page(request, id):
    in_list = False
    try:
        trailers = movie_services.get_videos(id, 'tv')
        if trailers == []:
            trailers = 'none'
    except:
        trailers = 'none'


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

    eproducers = []
    producer = []
    for crew in show['cast_info']['crew']:
        if crew['job'] == 'Executive Producer':
            eproducers.append(crew)
        if crew['job'] == 'Producer':
            producer.append(crew)
    execlist = len(eproducers)
    prodlist = len(producer)
    review_data = review_services.sort_reviews_media(user, id, "tv")
    context = {
        "show": show['show_info'],
        'cast': show['cast_info'],
        'eproducers': eproducers,
        'producer': producer,
        'execlist': execlist,
        'prodlist': prodlist,
        'trailers': trailers,
        "in_list": in_list,
        'score': score,
        'score_color': color,
        'reviews': review_data['reviews'],
        'friend_reviews': review_data['friend_reviews'],
        'avg_score': review_data['avg_score'],
        'avg_score_color': review_data['avg_color'],

    }


    print len(context['friend_reviews'])
    return render(request, 'movieApp/tv_view_page.html', context)




def show_episode(request, id, season, episode):
    tv_episode = movie_services.get_episode(id, season, episode)
    status = authenticate(request)
    review_c = False
    in_list = False
    if status == "in":
        user_id = request.session['user']
        review_c = review_completed(user_id, id, "episode")
        in_list = in_watchlist(user_id, id)
    else:
        review_c = "not logged"

    color = "red"
    if review_c > 60:
        color = "yellow"
    if review_c > 80:
        color = 'green'

    user = request.session['user']
    review_data = review_services.sort_reviews_media(user, id, "tv")

    context = {
        'tv_episode': tv_episode,
        "id": id,
        'in_list': in_list,
        "color" : color,
        "season": season,
        "episode": episode,
        'completed': review_c,
        'reviews': review_data['reviews'],
        'friend_reviews': review_data['friend_reviews'],
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

    total_number = len(movies) - 1

    rand_num = randint(0, total_number)
    rec_movie =  movies[rand_num]['id']
    rec = movie_services.get_recommendations(rec_movie)



    data = {
        "discover": rec,
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

    media_type = request.GET.get('type')
    _id = request.GET.get('id')

    if media_type == "movie":
        movie = movie_services.get_movie(_id)
        data = {
            "movie": movie['movie_info'], # this is the data for the current movie being displayed
            "user_id": request.session['user'], # the logged in user id from session
            "type": "movie" # whether it is a movie or tv show
        }
        Watchlist.add_movie(data) # add movie to Watchlist

    if media_type == "tv":
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
