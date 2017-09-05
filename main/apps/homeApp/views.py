from django.shortcuts import render, redirect, HttpResponse
from . import services
from ..User_app.models import User, Profile, Friend
# from ..movieApp.models import Movie
from ..User_app import views
from django.views.generic.edit import FormView
import json
import requests



# Create your views here.
"""

api key = 286abf6056d0a1338f772d1b7202e728
"""
def index(request):
    result = services.get_discover()
    if "user" in request.session :
        status = 'You are logged in'
        users = User.objects.exclude(id= request.session['user']).order_by('-created_at')
        friend, created = Friend.objects.get_or_create(current_user=User.objects.get(id = request.session['user']))
        friends = friend.users.all()
        try:
            profile = Profile.objects.filter(user_id=User.objects.get(id=request.session['user']))
        except:
            pass
        return render(request, 'homeApp/index.html', {'status': status, 'result': result, 'users': users, 'friends': friends, 'profile': profile})

    else:
        status = "You are NOT logged in"
        users = User.objects.all().order_by('-created_at')
        return render(request, 'homeApp/index.html', {'status': status, 'result': result, 'users': users})




def feed(request):
    if "user" not in request.session:
        return redirect('/')

    user = User.objects.get(id=request.session['user'])
    friends = Friend.objects.get(current_user=user)
    feed_list = []
    for friend in friends.users.all():
        movie_reviews = Review.objects.filter(user_id=friend.id)
        # print movie_reviews
        for review in movie_reviews:
            feed_list.append(review)



    context = {
        "friends": friends,
        "feed": feed_list,
    }

    return render(request, "homeApp/newsfeed.html", context)



def testing(request):
    return redirect('/')


def search_movies(request):
    if request.is_ajax():
        q=request.GET.get('term', '')
        movies = 'https://api.themoviedb.org/3/search/movie?api_key=286abf6056d0a1338f772d1b7202e728&language=en-US&query=' + q + '&page=1&include_adult=false'
        # movies = 'https://api.themoviedb.org/3/search/multi?api_key=286abf6056d0a1338f772d1b7202e728&language=en-US&query=' + q + '&page=1&include_adult=false'
        json_data = requests.get(movies).json()
        # print json_data
        results = json_data['results']
        # print results
        print '***************'
        movArray = []
        for movie in results:
            # print movie['id']
            movie_json = {}
            movie_json['id'] = movie['id']

            movie_json['label'] = movie['title']

            if "title" in movie:
                movie_json['label'] = movie['title']
            else:
                movie_json['label'] = movie['name']

            movie_json['value'] = movie['title']
            movArray.append(movie_json)
        data = json.dumps(movArray)
    else:
        data = 'fail'
    mimetype = 'application/json'
    print data
    return HttpResponse(data, mimetype)


def get_places(request):
    if request.is_ajax():
        q = request.GET.get('term', '')
        users = User.objects.filter(first_name__icontains = q )|User.objects.filter(last_name__icontains = q)| User.objects.filter(email__icontains = q)
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
    return HttpResponse(data, mimetype)

def search(request):
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




def mockup(request):
    return render(request, 'homeApp/main-mockup.html')
