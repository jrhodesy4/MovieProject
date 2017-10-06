from django.contrib import admin
from .models import Watchlist, MovieReview, TVReview, EpisodeReview, UserReview

# Register your models here.

admin.site.register(Watchlist)
admin.site.register(MovieReview)
admin.site.register(TVReview)
admin.site.register(EpisodeReview)
admin.site.register(UserReview)
