from django.contrib.auth.models import User
from rest_framework import generics
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework.views import APIView

from twitter_operations.models import Tweet, Comment, LikeTweet
from twitter_operations.permission import TokenPermission
from twitter_operations.serializers import UserSerializer, ShowFollowerSerializer, \
    ShowFollowedSerializer, TweetSerializer, CommentSerializer, LikeTweetUserSerializer
from twitter_operations.utils import post_tweet, follow_people, unfollow_people, validate_user_id, update_tweet, \
    delete_tweet, like_tweet, unlike_tweet, comment_tweet, upadte_comment, delete_comment, validate_tweet_id


class UserRudView(generics.RetrieveUpdateDestroyAPIView):
    lookup_field = 'pk'
    serializer_class = UserSerializer

    def get_queryset(self):
        return User.objects.all()

    def get_serializer_context(self, *args, **kwargs):
        return {"request": self.request}


class PostTweet(APIView):
    permission_classes = (TokenPermission, )

    def post(self, request):
        return post_tweet(request.data, request.user)


class FollowPeople(APIView):
    def post(self, request):
        return follow_people(request.data, request.user)


class UnfollowPeople(APIView):
    def post(self, request):
        return unfollow_people(request.data, request.user)


class ShowFollowers(APIView):
    pagination_class = PageNumberPagination
    paginator = pagination_class()

    def post(self, request):
        user_id = validate_user_id(request.data.get('user_id'))
        if isinstance(user_id, Response):
            return user_id

        user = User.objects.get(pk=user_id)
        queryset = user.follower.all().order_by('-created_at').prefetch_related('follower_user')
        page = self.paginator.paginate_queryset(queryset, request)
        serializer = ShowFollowerSerializer(page, many=True)
        return self.paginator.get_paginated_response(serializer.data)


class ShowFollowing(APIView):
    pagination_class = PageNumberPagination
    paginator = pagination_class()

    def post(self, request):
        user_id = validate_user_id(request.data.get('user_id'))
        if isinstance(user_id, Response):
            return user_id

        user = User.objects.get(pk=user_id)
        queryset = user.followed.all().order_by('-created_at').prefetch_related('followed_user')
        page = self.paginator.paginate_queryset(queryset, request)
        serializer = ShowFollowedSerializer(page, many=True)
        return self.paginator.get_paginated_response(serializer.data)


class UserTimeline(APIView):
    pagination_class = PageNumberPagination
    paginator = pagination_class()

    def post(self, request):
        user_id = validate_user_id(request.data.get('user_id'))
        if isinstance(user_id, Response):
            return user_id

        user = User.objects.get(pk=user_id)
        queryset = user.tweets.all().order_by('-created_at')
        page = self.paginator.paginate_queryset(queryset, request)
        serializer = TweetSerializer(page, many=True)
        return self.paginator.get_paginated_response(serializer.data)


class HomeTimeline(APIView):
    pagination_class = PageNumberPagination
    paginator = pagination_class()

    def post(self, request):
        user_ids = list(request.user.followed.all().values_list('followed_user__pk', flat=True)) + [request.user.pk]
        queryset = Tweet.objects.filter(user_id__in=user_ids).order_by('-created_at')
        page = self.paginator.paginate_queryset(queryset, request)
        serializer = TweetSerializer(page, many=True)
        return self.paginator.get_paginated_response(serializer.data)


class UpdateTweet(APIView):
    permission_classes = (TokenPermission, )

    def post(self, request):
        return update_tweet(request.data, request.user)


class DeleteTweet(APIView):
    permission_classes = (TokenPermission, )

    def post(self, request):
        return delete_tweet(request.data, request.user)


class CommentTweet(APIView):
    permission_classes = (TokenPermission, )

    def post(self, request):
        return comment_tweet(request.data, request.user)


class UpdateComment(APIView):
    permission_classes = (TokenPermission, )

    def post(self, request):
        return upadte_comment(request.data, request.user)


class DeleteComment(APIView):
    permission_classes = (TokenPermission, )

    def post(self, request):
        return delete_comment(request.data, request.user)


class GetAllComments(APIView):
    pagination_class = PageNumberPagination
    paginator = pagination_class()

    def post(self, request):
        tweet_id = validate_tweet_id(request.data.get('tweet_id'))
        if isinstance(tweet_id, Response):
            return tweet_id

        queryset = Comment.objects.filter(tweet_id=tweet_id)
        page = self.paginator.paginate_queryset(queryset, request)
        serializer = CommentSerializer(page, many=True)
        return self.paginator.get_paginated_response(serializer.data)


class LikeATweet(APIView):
    permission_classes = (TokenPermission, )

    def post(self, request):
        return like_tweet(request.data, request.user)


class UnlikeTweet(APIView):
    permission_classes = (TokenPermission, )

    def post(self, request):
        return unlike_tweet(request.data, request.user)


class GetAllLikesToTweet(APIView):
    pagination_class = PageNumberPagination
    paginator = pagination_class()

    def post(self, request):
        tweet_id = validate_tweet_id(request.data.get('tweet_id'))
        if isinstance(tweet_id, Response):
            return tweet_id

        queryset = LikeTweet.objects.filter(tweet_id=tweet_id)
        page = self.paginator.paginate_queryset(queryset, request)
        serializer = LikeTweetUserSerializer(page, many=True)
        return self.paginator.get_paginated_response(serializer.data)


class GetAllLikedTweets(APIView):
    pagination_class = PageNumberPagination
    paginator = pagination_class()

    def post(self, request):
        user_id = validate_user_id(request.data.get('user_id'))
        if isinstance(user_id, Response):
            return user_id

        queryset = Tweet.objects.filter(pk__in=LikeTweet.objects.filter(
            user_id=user_id).values_list('tweet_id', flat=True))
        page = self.paginator.paginate_queryset(queryset, request)
        serializer = TweetSerializer(page, many=True)
        return self.paginator.get_paginated_response(serializer.data)




