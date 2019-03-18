import os

from django.conf import settings
from django.contrib.auth.models import User
from django.db import models
from datetime import datetime

# Create your models here.


GENDER = (
    ('male', 'MALE'),
    ('female', 'FEMALE'),
)


class UserProfile(models.Model):
    user = models.OneToOneField(User, related_name='user', on_delete=models.CASCADE)
    photo_path = models.ImageField(upload_to='images/', default=os.path.join(settings.BASE_DIR, 'images/xrSh9Z0.jpg'))
    gender = models.CharField(max_length=15, choices=GENDER)

    def __str__(self):
        return self.user.get_full_name()

    def get_photo_path(self):
        return os.path.join('/static', os.path.basename(self.photo_path.path))


class Tweet(models.Model):
    user = models.ForeignKey(User, related_name='tweets', on_delete=models.CASCADE)
    tweet = models.CharField(max_length=150, null=False, blank=False)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.tweet

    def update(self, new_tweet):
        if new_tweet:
            self.tweet = new_tweet
            self.modified_at = datetime.now()
            self.save()
            return self.tweet


class Follower(models.Model):
    follower_user = models.ForeignKey(User, related_name='followed', on_delete=models.CASCADE)
    followed_user = models.ForeignKey(User, related_name='follower', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('follower_user', 'followed_user',)

    def __str__(self):
        return '{} follows {}'.format(self.follower_user.get_full_name(), self.followed_user.get_full_name())


class LikeTweet(models.Model):
    user = models.ForeignKey(User, related_name='likes', on_delete=models.CASCADE)
    tweet = models.ForeignKey(Tweet, related_name='likes', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'tweet',)

    def __str__(self):
        return '{} likes tweet "{}"'.format(self.user.get_full_name(), self.tweet)


class Comment(models.Model):
    user = models.ForeignKey(User, related_name='comment', on_delete=models.CASCADE)
    tweet = models.ForeignKey(Tweet, related_name='comment', on_delete=models.CASCADE)
    comment = models.CharField(max_length=150, null=False, blank=False)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.comment

    def update(self, new_comment):
        if new_comment:
            self.tweet = new_comment
            self.modified_at = datetime.now()
            self.save()
            return self.comment





