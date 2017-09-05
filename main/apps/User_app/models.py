from __future__ import unicode_literals
from django.db import models

# ****************************************************************
# ****************************************************************
# BCRIPT NEEDS TO BE ADDED BEFORE DEPLOYMENT
# ****************************************************************
# ****************************************************************

# Create your models here.
# =================================================================
# Model Functions
# =================================================================
class UserManager(models.Manager):
    def register(self, data):
        errors = []
        try: #check to see if the email is already in use
            User.objects.get(email=data['email'])
            print 'email is already registered'
            errors.append('This email is already registered')
        except:
            pass
            #first name validations
        if data['first_name'] == '':
            errors.append('The First name cannot be blank')
        elif data['first_name'].isdigit():
            errors.append('The First Name can only be characters!')
        #Last Name Validations
        if data['first_name'] == '':
            errors.append('The First name cannot be blank')
        elif data['first_name'].isdigit():
            errors.append('The First Name can only be characters!')
        #email Validations

        if data['email'] == '':
            errors.append('The Email Field cannot be blank')
        # ----------------------
        # MUST ADD EMAIL REGEX INTO VALIDATIONS
        # ---------------------
        # Password validation
        if len(data['password']) < 1 :
            errors.append('The password cannot be blank')


        if len(errors) == 0: #if there are no errors in the validations
            user = User.objects.create( # create the new user
                first_name=data['first_name'],
                last_name=data['last_name'],
                email=data['email'],
                password=data['password'],
            )
            print 'User was added'
            return {'user': user, 'errors': None}
        else:
            print 'User was NOT added'
            return {'user': None, 'errors': errors}



    def login(self, data): #the function for validating a log in
        errors = []
        try:
            foundUser = User.objects.get(email=data['email'])
            print "User is found"
            if foundUser.password == data['password']:
                return {'user': foundUser, 'errors': None}
            else:
                errors.append('Email or password is incorrect')
                return {'user': None, 'errors': errors }

        except:
            print "there is no user with that name"
            errors.append('Email or password is incorrect')
            return {'user': None, 'errors': errors }

# =================================================================
# Models
# =================================================================
#this is the Model for our users ==================
class User(models.Model):
#Users
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.CharField(max_length=100)
    password = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = UserManager()

    @classmethod
    def Fullname_toString(self, user): #<-- must put the user object in
        f = user.first_name.title()
        l = user.last_name.title()
        return str(f + " " + l)


# this is the model for the profile thats attached to a user =======
class Profile(models.Model):
    hometown = models.CharField(max_length=100, default='null')
    birthday = models.DateField()
    country = models.CharField(max_length=100)
    user_id = models.ForeignKey(User, related_name='profile')

class ProPicture(models.Model):
    picture = models.ImageField(upload_to='documents/', blank=True)
    user_id = models.ForeignKey(User, related_name='profilePic')


# establishes a friendship so user can see friends list =========

class Friend(models.Model):
    users = models.ManyToManyField(User, related_name='friend_set')
    current_user = models.ForeignKey(User, related_name='owner', null=True)

    # method for adding friends=========

    # don't know why these methods aren't being recognized when I call on them----------------------------------------
    @classmethod
    def add_friend(cls, current_user, new_friend):
        friend, created = cls.objects.get_or_create(
        current_user=current_user
        )
        friend.users.add(new_friend)
        print "friend added"
        Notification.add_friend_notification(new_friend.id, current_user.id)

    #  method for removing friends =======

    @classmethod
    def lose_friend(cls, current_user, new_friend):
        friend, created = cls.objects.get_or_create(
        current_user=current_user
        )
        friend.users.remove(new_friend)



class Notification(models.Model):
    user = models.ForeignKey(User, null=True)
    message = models.CharField(max_length=100, default='null')
    category = models.CharField(max_length=50, default='null')
    viewed = models.BooleanField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


    @classmethod
    def add_friend_notification(self, user_id, follower_id):
        user = User.objects.get(id=user_id)
        follower = User.objects.get(id=follower_id)

        full_name = User.Fullname_toString(follower)
        message = full_name + " " + "has followed you"


        Notification.objects.create(
            user = user,
            message = message,
            category = follower,
            viewed = False,
        )
        print 'notification created '


    @classmethod
    def was_viewed(self, notification):
        notification.viewed = True
        notification.save()





# end
