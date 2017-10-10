from django.shortcuts import render, redirect
from . import movie_services, review_services
from ..homeApp import services
from .models import Watchlist
from ..User_app.models import User
from ..movieApp.models import MovieReview, TVReview, EpisodeReview, UserReview
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

def review_completed(user_id, id, _type): #<----- if media is in the user watchlist returns boolean
    if _type == "movie":
        try:
            MovieReview.objects.get(api_code=id, user_id=user_id)
            print "user has already written a review"
            return True
        except:
            return False
    if _type == "tv":
        try:
            TVReview.objects.get(api_code=id, user_id=user_id)
            print "user has already written a review"
            return True
        except:
            return False
    if _type == "episode":
        try:
            EpisodeReview.objects.get(api_code=id, user_id=user_id)
            print "user has already written a review"
            return True
        except:
            return False

# Create your views here.=======================
# =====================================================================
# =====================================================================


def movie_page(request, id): # this renders the selected individual movie page
    in_list = False
    status = authenticate(request)
    review_c = False
    if status == "in":
        user_id = request.session['user']
        in_list = in_watchlist(user_id, id)
        review_c = review_completed(user_id, id, "movie")

    # user_id = request.session['user']
    movie = movie_services.get_movie(id)
    reviews = review_services.all_movie_reviews(id)
    print reviews
    try:
        watchlist = Watchlist.objects.get(api_code=id)
    except: watchlist = 'nothing'


    context = { #<-- info that goes to template
        'movie': movie['movie_info'],
        'cast': movie['cast_info'],
        'reviews' : reviews,
        'in_list': in_list,
        'completed': review_c,
    }
    return render(request, 'movieApp/movie_view_page.html', context)

def show_page(request, id, season):
    tv_season = movie_services.get_season(id, season)
    print tv_season
    id = id
    season = season
    show = movie_services.get_show(id)
    reviews = TVReview.objects.filter(api_code=id)
    in_list = False
    review_c = False
    # status = authenticate(request)
    # if status == "in":
    #     user_id = request.session['user']
    #     in_list = in_watchlist(user_id, id)
    #     review_c = review_completed(user_id, id, "tv")

    context = {
        "show": show['show_info'],
        'cast': show['cast_info'],
        "id": id,
        "season": season,
        "tv_season": tv_season,
        "reviews": reviews,
        # "in_list": in_list,
        # 'watchlist': Watchlist.objects.filter(user=request.session["user"]),
        # 'completed': review_c,

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
    if id == "1":
        pagetitle = "Now playing"
        movies = movie_services.get_full_nowplaying()
    if id == '2':
        pagetitle = "Top Movies"
    if id == '3':
        pagetitle = "Upcoming"
    if id == '4':
        pagetitle = "On Air"
    if id == '5':
        pagetitle = "Top Rated"
    if id == '6':
        pagetitle = "Popular"
    print movies
    data = {
        "pagetitle": pagetitle,
        "movies": movies
    }
    return render(request, "movieApp/discover_more.html", data)




# ===========================
#Post Routes
# ===========================

def add_to_watchlist(request, id): # the post route adds a movie to the Users watchlist
    if request.method == 'POST':
        _type = request.POST['type']

        if _type == "movie":
            movie = movie_services.get_movie(id)
            data = {
                "movie": movie['movie_info'], # this is the data for the current movie being displayed
                "user_id": request.session['user'], # the logged in user id from session
                "type": "movie" # whether it is a movie or tv show
            }
            Watchlist.add_movie(data) # add movie to Watchlist
            return redirect('/movie/' + id)

        if _type == "tv":
            show = movie_services.get_show(id)
            data = {
                "movie": show, # this is the data for the current movie being displayed
                "user_id": request.session['user'], # the logged in user id from session
                "type": "tv" # whether it is a movie or tv show
            }
            Watchlist.add_movie(data) # add movie to Watchlist
            return redirect('/show/' + id)

def delete_from_watchlist(request, id):
    delete_me = Watchlist.objects.get(id=id)
    delete_me.delete()
    return redirect("/profile")


def makeReview(request, id, season, episode):
    if 'user' not in request.session:
        return redirect('/')
    if request.method == "POST":
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
                return redirect('/movie/' + id)
            else:
                UserReview.add_review(mr, "movie", user_id)
                return redirect('/movie/' + id)

        if request.POST['type'] == "tv":
            tr = TVReview.create_review(data)
            if tr == None:
                return redirect('/show/' + id)
            else:
                UserReview.add_review(tr, "tv", user_id)
                return redirect('/show/' + id)

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
                return redirect('/episode/' + id + "/" + season + "/" + episode)
            else:
                UserReview.add_review(epi, "episode", user_id)
                return redirect('/episode/' + id + "/" + season + "/" + episode)













# end
