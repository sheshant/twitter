from django.contrib import admin
from django.contrib.admin import BooleanFieldListFilter

from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.core.urlresolvers import reverse
from django.template.defaultfilters import escape

from twitter_operations.models import UserProfile, Tweet, Follower, Comment, LikeTweet


class UserAdmin(BaseUserAdmin):
    list_display = ('username', 'first_name', 'last_name', 'email', 'is_active', 'image_tag', 'date_joined')
    search_fields = ('username', 'email', 'date_joined')

    def image_tag(self, obj):
        return '<img src="/static/%s" style="max-height:40px;max-width:40px">' % obj.user.photo_path.url.split('/')[-1]

    image_tag.short_description = 'Image'
    image_tag.allow_tags = True


class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'first_name', 'last_name', 'email', 'is_active', 'user_link', 'image_tag', 'gender')
    list_filter = ('gender',)

    @staticmethod
    def first_name(obj):
        return obj.user.first_name

    @staticmethod
    def last_name(obj):
        return obj.user.last_name

    @staticmethod
    def email(obj):
        return obj.user.email

    @staticmethod
    def is_active(obj):
        return obj.user.is_active

    def user_link(self, obj):
        user = obj.user
        return '<a href="{}" target="_blank">{}</a>'.format(reverse("admin:auth_user_change", args=(user.id,)),
                                                            escape(user.username))

    user_link.allow_tags = True

    def image_tag(self, obj):
        return u'<img src="/static/%s" style="max-height:40px;max-width:40px">' % obj.photo_path.url.split('/')[-1]

    image_tag.short_description = 'Image'
    image_tag.allow_tags = True


class TweetAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'tweet', 'created_at')
    search_fields = ('user', 'tweet')
    list_filter = ('created_at',)


class FollowerAdmin(admin.ModelAdmin):
    list_display = ('follower_user', 'followed_user', 'created_at')
    search_fields = ('follower_user', 'followed_user')


class LikeTweetAdmin(admin.ModelAdmin):
    list_display = ('user', 'tweet', 'created_at')
    search_fields = ('user', 'tweet')
    list_filter = ('created_at',)


class CommentAdmin(admin.ModelAdmin):
    list_display = ('user', 'tweet', 'comment', 'created_at')
    search_fields = ('user', 'tweet', 'comment')
    list_filter = ('created_at',)


admin.site.unregister(User)
admin.site.register(User, UserAdmin)
admin.site.register(UserProfile, UserProfileAdmin)
admin.site.register(Tweet, TweetAdmin)
admin.site.register(Follower, FollowerAdmin)
admin.site.register(Comment, CommentAdmin)
admin.site.register(LikeTweet, LikeTweetAdmin)
