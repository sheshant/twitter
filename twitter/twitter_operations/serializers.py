
from django.contrib.auth.models import User
from rest_framework import serializers

from twitter_operations.models import Tweet, Follower, LikeTweet, Comment


class UserSerializer(serializers.ModelSerializer):
    url = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = User
        fields = [
            'url',
            'id',
            'username',
            'first_name',
            'last_name',
            'email',
            'date_joined',
        ]
        read_only_fields = ['id']

    # converts to JSON
    # validations for data passed

    def get_url(self, obj):
        # request
        request = self.context.get("request")
        return obj.user.get_api_url(request=request)

    def validate_title(self, value):
        qs = User.objects.filter(username=value)
        if self.instance:
            qs = qs.exclude(pk=self.instance.pk)
        if qs.exists():
            raise serializers.ValidationError("This username has already been taken")
        return value


class ShowFollowerSerializer(serializers.ModelSerializer):
    id = serializers.SerializerMethodField(read_only=True)
    username = serializers.SerializerMethodField(read_only=True)
    full_name = serializers.SerializerMethodField(read_only=True)
    date_joined = serializers.SerializerMethodField(read_only=True)
    photo = serializers.SerializerMethodField(read_only=True)
    gender = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Follower
        fields = [
            'id',
            'username',
            'full_name',
            'date_joined',
            'photo',
            'gender',
            'created_at',
        ]

    def get_id(self, obj):
        return obj.follower_user.pk

    def get_username(self, obj):
        return obj.follower_user.username

    def get_full_name(self, obj):
        return obj.follower_user.get_full_name()

    def get_date_joined(self, obj):
        return obj.follower_user.date_joined

    def get_photo(self, obj):
        return obj.follower_user.user.get_photo_path()

    def get_gender(self, obj):
        return obj.follower_user.user.gender


class ShowFollowedSerializer(serializers.ModelSerializer):
    id = serializers.SerializerMethodField(read_only=True)
    username = serializers.SerializerMethodField(read_only=True)
    full_name = serializers.SerializerMethodField(read_only=True)
    date_joined = serializers.SerializerMethodField(read_only=True)
    photo = serializers.SerializerMethodField(read_only=True)
    gender = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Follower
        fields = [
            'id',
            'username',
            'full_name',
            'date_joined',
            'photo',
            'gender',
            'created_at',
        ]

    def get_id(self, obj):
        return obj.followed_user.pk

    def get_username(self, obj):
        return obj.followed_user.username

    def get_full_name(self, obj):
        return obj.followed_user.get_full_name()

    def get_date_joined(self, obj):
        return obj.followed_user.date_joined

    def get_photo(self, obj):
        return obj.followed_user.user.get_photo_path()

    def get_gender(self, obj):
        return obj.followed_user.user.gender


class TweetSerializer(serializers.ModelSerializer):

    class Meta:
        model = Tweet
        fields = ['user', 'tweet', 'created_at']


class FollowerSerializer(serializers.ModelSerializer):

    class Meta:
        model = Follower
        fields = ['follower_user', 'followed_user']


class LikeTweetSerializer(serializers.ModelSerializer):
    user_id = serializers.IntegerField()
    tweet_id = serializers.IntegerField()

    class Meta:
        model = LikeTweet
        fields = ['user_id', 'tweet_id']


class CommentSerializer(serializers.ModelSerializer):
    user_id = serializers.IntegerField()
    tweet_id = serializers.IntegerField()

    class Meta:
        model = Comment
        fields = ['user_id', 'tweet_id', 'comment', 'created_at']


class LikeTweetUserSerializer(serializers.ModelSerializer):
    id = serializers.SerializerMethodField(read_only=True)
    username = serializers.SerializerMethodField(read_only=True)
    full_name = serializers.SerializerMethodField(read_only=True)
    date_joined = serializers.SerializerMethodField(read_only=True)
    photo = serializers.SerializerMethodField(read_only=True)
    gender = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = LikeTweet
        fields = [
            'id',
            'username',
            'full_name',
            'date_joined',
            'photo',
            'gender',
            'created_at',
        ]

    def get_id(self, obj):
        return obj.user.pk

    def get_username(self, obj):
        return obj.user.username

    def get_full_name(self, obj):
        return obj.user.get_full_name()

    def get_date_joined(self, obj):
        return obj.user.date_joined

    def get_photo(self, obj):
        return obj.user.user.get_photo_path()

    def get_gender(self, obj):
        return obj.user.user.gender

