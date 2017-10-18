from django.shortcuts import render, redirect
from .models import User, Profile, Friend, Notification, ProPicture
from ..movieApp.models import Watchlist, UserReview, MovieReview, TVReview, EpisodeReview
from django.conf import settings
from django.core.files.storage import FileSystemStorage
from . import user_services
from datetime import datetime, timedelta
import math




"""
things that need to be added?
1. validation messages
2. make sure that password is protected using Bcrpt and confirm password

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
    month_difference = int(difference.days / 30)
    year_difference = int(month_difference / 12)
    data = {
        "poster_path": review['poster_path'],
        "overall_score": review['score'],
        "overall_color": ovScoreColor(review['score']),
        'story_percent': subPercent(review['story_rating']),
        'story_color': subScoreColor(review['story_rating']),
        'ent-percent': subPercent(review['entertainment_rating']),
        'ent_color': subScoreColor(review['entertainment_rating']),
        'act_percent': subPercent(review['acting_rating']),
        'act_color': subScoreColor(review['acting_rating']),
        'vis_percent': subPercent(review['visual_rating']),
        'vis_color': subScoreColor(review['visual_rating']),
        'sound_percent': subPercent(review['sound_rating']),
        'sound_color': subScoreColor(review['sound_rating']),
        'minute_difference': minute_difference,
        'hour_difference': hour_difference,
        'day_difference': day_difference,
        'month_difference' : month_difference,
        'year_difference': year_difference
    }

    return data


def profileFormat(user): # <--- this function will return profile info how we want
    first = user.first_name
    last = user.last_name
    try :
        pic = ProPicture.objects.get(user_id=user.id)
        profile_pic = pic.picture
        is_pic = True
    except:
        profile_pic = first[0] + last[0]
        is_pic = False
    data = {
        'profile_id': user.id,
        'first_name': first,
        'last_name': last,
        'is_profile_pic': is_pic,
        'pic_name': profile_pic
    }
    return data


# Create your views here.
# =================================================================
# template renders
# =================================================================
def login_page(request): #renders the login page template
    return render(request, 'User_app/login_page.html')

def register_page(request): #renders the register page template
    return render(request, 'User_app/register_page.html')



def editProfilePicture(request):
    if request.method == 'POST' and request.FILES['myfile']:
        myfile = request.FILES['myfile']
        fs = FileSystemStorage()
        filename = fs.save(myfile.name, myfile)
        uploaded_file_url = fs.url(filename)
        oldProfilePic = ProPicture.objects.get(user_id = User.objects.get(id = request.session['user']))
        oldProfilePic.picture = uploaded_file_url
        oldProfilePic.save()
        return redirect('/profile')


def profile(request):
    if 'user' not in request.session:
        return redirect('/login')



    user = User.objects.get(id=request.session['user'])
    profile = Profile.objects.filter(user_id = User.objects.get(id = request.session['user']))

    user_profile = profileFormat(user)


    reviews = user_services.get_reviews(request.session['user'])
    length = len(reviews)
    friend, created = Friend.objects.get_or_create(current_user=User.objects.get(id = request.session['user']))
    following = friend.users.all()
    followers = Friend.objects.filter(users=user)

    followerPics = []
    pics = []
    user_pic = []


    followers_final =[]
    for follower in followers:
        data = profileFormat(follower.current_user)
        followers_final.append(data)

    following_final = []
    for person in following:
        data = profileFormat(person)
        following_final.append(data)



    final_form_reviews =[] # <-- this returns the reviews and makes them formated correctly
    for review in reviews:
        data = createReviewFormat(review);
        final_form_reviews.append(data)

    print following_final
    context = {
        'length' : length,
        'followers' : followers,
        'following' : following,
        'profile' : profile,
        'follower_dic' : followers_final,
        'following_dic' : following_final,
        'watchlist': Watchlist.objects.filter(user=request.session["user"]),
        'reviews' : final_form_reviews,
        'user': user_profile

    }
    return render(request, "User_app/profile.html", context)

def user_page(request, id):
    if 'user' not in request.session:
        return redirect('/login')

    try: #this is so if user does not exist it will not crash
        user = User.objects.get(id = id)
    except:
        return redirect('/')

    person_profile = profileFormat(user) #here is the persons profile info formated

    #gets the reviews and length of them
    reviews = user_services.get_reviews(id)
    length = len(reviews)

    try:
        myFollow = Friend.objects.get(users=User.objects.get(id=id), current_user=User.objects.get(id = request.session['user']))
    except:
        myFollow = "you don't follow"


    followers = Friend.objects.filter(users=User.objects.get(id = id))


    friend, created = Friend.objects.get_or_create(current_user=User.objects.get(id = id))
    following = friend.users.all()

    followers_final =[]
    for follower in followers:
        data = profileFormat(follower.current_user)
        followers_final.append(data)

    following_final = []
    for person in following:
        data = profileFormat(person)
        following_final.append(data)


    final_form_reviews =[]
    for review in reviews:
        data = createReviewFormat(review);
        final_form_reviews.append(data)
    print "******following********"
    print following_final
    print "******followers********"
    print followers_final

    data = {
        'length': length,
        'reviews': final_form_reviews,
        'myFollow': myFollow,
        'user': person_profile,
        'following': following.count,
        'followers': followers.count,
        'following_dic' : following_final,
        'followers_dic' : followers_final,
    }

    return render(request, 'User_app/user.html', data)


def notification_page(request):
    user_id = request.session['user']
    user = User.objects.get(id=user_id)
    User.Fullname_toString(user)
    notifications = Notification.objects.filter(user=user).order_by('created_at')
    context = {
        "notifications": notifications,
    }

    for notification in notifications:
        if notification.viewed == False:
            Notification.was_viewed(notification)

    return render(request, "User_app/notifications.html", context)





# =================================================================
# POST request's
# =================================================================


def newProfilePicture(request):
    if request.method == 'POST' and request.FILES['myfile']:
        myfile = request.FILES['myfile']
        fs = FileSystemStorage()
        filename = fs.save(myfile.name, myfile)
        uploaded_file_url = fs.url(filename)
        profilePic = ProPicture.objects.create(
        picture = uploaded_file_url,
        user_id = User.objects.get(id = request.session['user'])
        )
        profilePic.save()
        return redirect('/profile')

def createProfile(request):
    if request.method == 'POST':
        profile = Profile.objects.create(
            birthday = request.POST['birthday'],
            hometown = request.POST['hometown'],
            country = request.POST['country'],
            user_id = User.objects.get(id = request.session['user']),
        )
        profile.save()
        return redirect('/profile')

def editProfile(request):
    if request.method == 'POST':
        profile = Profile.objects.get(user_id = User.objects.get(id = request.session['user']))
        birthday = request.POST['birthday']
        hometown = request.POST['hometown']
        country = request.POST['country']
        profile.birthday = birthday
        profile.hometown = hometown
        profile.country = country
        profile.save()
        return redirect('/profile')



def register_account(request): #this function creates the account
    if request.method == 'POST':
        account_info = {
            "first_name": request.POST['first_name'],
            "last_name": request.POST['last_name'],
            "email": request.POST['email'],
            "password": request.POST['password']
        }
        result = User.objects.register(account_info)
        user_id = result['user'].id
        if result['errors'] == None:
            request.session['name'] = result['user'].first_name
            request.session['user'] = user_id
            request.session['action'] = "registered"
            UserReview.create_new(user_id)
            return redirect('/')
        else:
            print result['errors']
            return redirect("/register")


def log_user_in(request): # this is to the log the user in
    if request.method == 'POST':
        login_info = {
            "email": request.POST['email'],
            "password": request.POST['password']
        }

        result = User.objects.login(login_info)

        if result['errors'] == None:
            request.session['email'] = result['user'].email
            request.session['name'] = result['user'].first_name
            request.session['user'] = result['user'].id
            request.session['action'] = "logged in"
            return redirect('/')
        else:
            print result['errors']
            return redirect('/login')





# renders the specific user page, other than the current user


def logout(request):
    request.session.clear()
    return redirect('/login')


# function that calls on the Friend Methods to add or remove a friend

def change_friends(request, operation, id):
    new_friend = User.objects.get(id=id)
    id = id
    if operation == 'add':
        Friend.add_friend(User.objects.get(id=request.session['user']), new_friend)
    elif operation == 'remove':
        Friend.lose_friend(User.objects.get(id=request.session['user']), new_friend)

    return redirect('/user/' + id)


def searchUsers(request):
    if request.method == 'POST':
        count = User.objects.filter(first_name__icontains=request.POST['person']).count()
        users = User.objects.filter(first_name__icontains=request.POST['person'])
        print users
        return render(request, 'homeApp/search.html', {'users' : users, 'count' : count})





# end
