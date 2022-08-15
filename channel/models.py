from datetime import date
from pyexpat import model
from django.db import models
from django.contrib.auth import get_user_model
from datetime import datetime
import uuid

# from .views import profile
# Create your models here.
User = get_user_model()


class Profile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    id_user = models.IntegerField()
    bio = models.CharField(max_length=100, blank=True)
    profileimg = models.ImageField(
        upload_to='profile_image', default='blank-profile-picture.png')
    location = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return self.user.username


class Post(models.Model):
    id = models.UUIDField(
        verbose_name=str, primary_key=True, default=uuid.uuid4)
    # str_id=id
    user = models.CharField(max_length=100)  # username
    image = models.ImageField(upload_to='post_images')
    caption = models.TextField()
    created_at = models.DateTimeField(default=datetime.now)
    no_of_likes = models.IntegerField(default=0)

    def __str__(self):
        return self.user


class FollowersCount(models.Model):
    follower = models.CharField(max_length=100)
    user = models.CharField(max_length=100)

    def __str__(self):
        return self.user


class LikePost(models.Model):
    # postt=models.ForeignKey(Post, on_delete=models.CASCADE)  ## name given bcz it clashes with other
    post_id = models.CharField(max_length=500)
    username = models.CharField(max_length=100)
    liked_at = models.DateTimeField(default=datetime.now)
    owner = models.CharField(max_length=100, default="")

    def __str__(self):
        return self.username


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, null=True)
    comment_post_id = models.UUIDField(verbose_name=str, default=uuid.uuid4)
    # ## name given bcz it clashes with other
    post_idd = models.CharField(max_length=500)
    profile_image = models.ImageField(
        upload_to='newprofile', default='blank-profile-picture.png')
    body = models.TextField()
    user = models.CharField(max_length=100)
    date_added = models.DateTimeField(default=datetime.now)

    def __str__(self):
        return self.user
