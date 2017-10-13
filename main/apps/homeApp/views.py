from django.shortcuts import render, redirect, HttpResponse
from . import services
from ..User_app import user_services
from ..User_app.models import User, Profile, Friend
# from ..movieApp.models import
from ..User_app import views
from django.views.generic.edit import FormView
from django.core import serializers
from django.http import JsonResponse
import json
import requests


# Create your views here.
"""
api key = 286abf6056d0a1338f772d1b7202e728
"""
def search(request):
    search = request.GET.get('search-info')
    result = services.search_database(search)
    return JsonResponse(result, safe=False)
    # return HttpResponse(serializers.serialize("json", final), content_type='application/json')


def index(request):
    result = services.get_discover()

    if "user" not in request.session:
        return redirect('/login')
    if "user" in request.session :
        status = 'You are logged in'
    user = request.session['user']
    reviews = user_services.get_feed_reviews(user)

    data = {
        "reviews": reviews
    }

    return render(request, 'homeApp/index.html', data)



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
