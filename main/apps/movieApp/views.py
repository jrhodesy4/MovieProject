from django.shortcuts import render, redirect
from . import movie_services, review_services
from ..homeApp import services
from .models import Watchlist
from ..User_app.models import User
from ..movieApp.models import MovieReview, TVReview, EpisodeReview, UserReview
# from ..homeApp import services



# Create your views here.
def movie_page(request, id): # this renders the selected individual movie page
    in_list = False
    if 'user' in request.session:
        user = User.objects.get(id=request.session['user'])
        watchlist = Watchlist.objects.filter(user__id=user.id)
        for movie in watchlist: #<-- this is to check if movie is already in watchlist
            if movie.api_Movie_code == id:
                in_list = True
    review_completed = False
    user_id = request.session['user']
    try:
        MovieReview.objects.get(api_code=id, user_id=user_id)
        review_completed = True
    except Exception as e:
        pass
    movie = movie_services.get_movie(id)
    reviews = review_services.all_movie_reviews(id)

    context = { #<-- info that goes to template
        'movie': movie['movie_info'],
        'cast': movie['cast_info'],
        'reviews' : reviews,
        'in_list': in_list
    }
    return render(request, 'movieApp/movie_page.html', context)

def show_page(request, id):
    show = movie_services.get_show(id)
    reviews = TVReview.objects.filter(api_code=id)
    context = {
        "show": show,
        "id": id,
        "reviews": reviews,
    }
    return render(request, 'movieApp/tv_page.html', context)

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
    context = {
        'tv_episode': tv_episode,
        "id": id,
        "season": season,
        "episode": episode
    }
    return render(request, 'movieApp/episode_page.html', context)



def cast_page(request, id): # this render the info page for the individual actor
    person_info = movie_services.get_person(id)
    person = {
        'details': person_info['details'],
        'credits': person_info['credits']
    }
    return render(request, 'movieApp/cast_page.html', person )



# ===========================
#Post Routes
# ===========================

def add_to_watchlist(request, id): # the post route adds a movie to the Users watchlist
    if request.method == 'POST':
        movie = services.get_movie(id)
        data = {
            "movie": movie['movie_info'], # this is the data for the current movie being displayed
            "user_id": request.session['user'] # the logged in user id from session
        }
        Watchlist.add_movie(data) # add movie to Watchlist
        return redirect('/movie/' + id)


def delete_from_watchlist(request, id):
    delete_me = Watchlist.objects.get(id=id)
    delete_me.delete()
    return redirect("/profile")


def makeReview(request, id, season, episode):
    if 'user' not in request.session:
        return redirect('/')
    if request.method == "POST":
        user_id = request.session['user']

        if request.POST['type'] == "movie":

            data = {
                "id": id,
                "content": request.POST['content'],
                "score": request.POST['score'],
                "user_id": user_id
            }
            mr = MovieReview.create_review(data)
            if mr == None:
                return redirect('/movie/' + id)
            else:
                UserReview.add_review(mr, "movie", user_id)
                return redirect('/movie/' + id)

        if request.POST['type'] == "tv":
            data = {
                "id": id,
                "content": request.POST['content'],
                "score": request.POST['score'],
                "user_id": user_id
            }
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
                "user_id": user_id
            }
            epi = EpisodeReview.create_review(data)
            if epi == None:
                return redirect('/episode/' + id + "/" + season + "/" + episode)
            else:
                UserReview.add_review(epi, "episode", user_id)
                return redirect('/episode/' + id + "/" + season + "/" + episode)













# end
