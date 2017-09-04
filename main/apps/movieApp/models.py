from __future__ import unicode_literals
from ..User_app.models import User
from django.db import models
from . import movie_services


class Watchlist(models.Model): #creates a watchlist
    api_Movie_code = models.CharField(max_length=100)
    movie_title = models.CharField(max_length=50)
    poster_path = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    # objects = WatchlistManager()

    @classmethod
    def add_movie(self, data):

        user = User.objects.get(id=data['user_id'])
        movie = data['movie']
        my_watchlist = Watchlist.objects.filter(user=user)


        Watchlist.objects.create( #<-- add the movie to the watchlist
            api_Movie_code = movie['id'],
            movie_title = movie['title'],
            poster_path = movie['poster_path'],
            user = user
        )
        print "added"
        return

    @classmethod
    def remove(self, data):
        return

#this is the Model for our movies ==================


class MovieReview(models.Model):
    user_id = models.CharField(max_length=100)
    api_code = models.CharField(max_length=100)
    title = models.CharField(max_length=50)
    poster_path = models.CharField(max_length=100)
    backdrop_path = models.CharField(max_length=100)
    content = models.CharField(max_length=140)
    score = models.PositiveIntegerField(null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    @classmethod
    def create_review(self, data):

        try:
            MovieReview.objects.get(user_id= data['user_id'])
            print "already wrote a review"
            return None
        except:
            pass
        movie = movie_services.get_movie(data['id'])['movie_info']

        movie_review = MovieReview.objects.create(
            user_id = data['user_id'],
            api_code = data['id'],
            content = data['content'],
            score = data['score'],
            title = movie['title'],
            poster_path = movie["poster_path"],
            backdrop_path = movie['backdrop_path']
        )
        return movie_review


class TVReview(models.Model):
    user_id = models.CharField(max_length=100)
    api_code = models.CharField(max_length=100)
    title = models.CharField(max_length=50)
    poster_path = models.CharField(max_length=100)
    backdrop_path = models.CharField(max_length=100)
    content = models.CharField(max_length=140)
    score = models.PositiveIntegerField(null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    @classmethod
    def create_review(self, data):
        try:
            TVReview.objects.get(user_id=data['user_id'])
            return None
        except:
            pass
        tv = movie_services.get_show(data['id'])
        tv_review = TVReview.objects.create(
            user_id = data['user_id'],
            api_code = data['id'],
            content = data['content'],
            score = data['score'],
            title = tv['name'],
            poster_path = tv["poster_path"],
            backdrop_path = tv['backdrop_path']
        )
        return tv_review

class EpisodeReview(models.Model):
    user_id = models.CharField(max_length=100)
    api_code = models.CharField(max_length=100)
    season = models.CharField(max_length=10)
    episode = models.CharField(max_length=10)
    series_title = models.CharField(max_length=50)
    episode_title = models.CharField(max_length=50)
    still_path = models.CharField(max_length=100)
    poster_path = models.CharField(max_length=100)
    content = models.CharField(max_length=140)
    score = models.PositiveIntegerField(null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    @classmethod
    def create_review(self, data):
        try:
            EpisodeReview.objects.get(user_id=data['user_id'])
            return None
        except:
            pass

        epi = movie_services.get_episode(data['id'], data['season'], data['episode'])
        season = movie_services.get_season(data['id'], data['season'])

        epi_review = EpisodeReview.objects.create(
            user_id = data['user_id'],
            api_code = data['id'],
            season = data['season'],
            episode = data['episode'],
            episode_title = epi['name'],
            series_title = season['name'],
            still_path = epi['still_path'],
            poster_path = season['poster_path'],
            content = data['content'],
            score = data['score'],


        )
        return epi_review

class UserReview(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='users')
    movie_review = models.ManyToManyField(MovieReview, related_name='movies')
    tv_review = models.ManyToManyField(TVReview, related_name='tvs')
    episode_review = models.ManyToManyField(EpisodeReview, related_name='episodes')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    @classmethod
    def create_new(self, id):
        user = User.objects.get(id=id)
        UserReview.objects.create(
            user = user
        )
        return
    @classmethod
    def add_review(self, review, _type, user_id):
        user = User.objects.get(id=user_id)
        ur = UserReview.objects.get(user=user)
        if _type == "movie":
            ur.movie_review.add(review)
            ur.save()
        if _type == "tv":
            ur.tv_review.add(review)
            ur.save()
        if _type == "episode":
            ur.episode_review.add(review)
            ur.save()
        return
# class Review(models.Model):
#     user_id = models.ForeignKey(User, related_name='users')
#     api_Movie_code = models.CharField(max_length=100)
#     movie_title = models.CharField(max_length=50)
#     poster_path = models.CharField(max_length=100)
#     backdrop_path = models.CharField(max_length=100)
#     content = models.CharField(max_length=140)
#     score = models.PositiveIntegerField(null=True)
#     created_at = models.DateTimeField(auto_now_add=True)
#     updated_at = models.DateTimeField(auto_now=True)
#
#
#     @classmethod
#     def add_review(self, data):
#         movie = services.get_movie(data['id'])['movie_info']
#         review = Review.objects.create(
#             user_id = User.objects.get(id = data['user_id']),
#             content = data['content'],
#             score = data['score'],
#             api_Movie_code = data['id'],
#             poster_path = movie["poster_path"],
#             movie_title = movie['title'],
#             backdrop_path = movie['backdrop_path']
#         )
#         return review
#



























        # end
