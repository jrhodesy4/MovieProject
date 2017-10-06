from django.contrib import admin
from .models import User, Profile, ProPicture, Friend, Notification

# Register your models here.

admin.site.register(User)
admin.site.register(Profile)
admin.site.register(ProPicture)
admin.site.register(Friend)
admin.site.register(Notification)
