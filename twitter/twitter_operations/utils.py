from datetime import datetime

from django.contrib.auth.models import User
from rest_framework.response import Response
from rest_framework.status import HTTP_400_BAD_REQUEST, HTTP_201_CREATED, HTTP_200_OK

from twitter_operations.constants import ERROR_MESSAGES, SUCCESS_MESSAGE
from twitter_operations.models import Follower, Tweet, LikeTweet, Comment
from twitter_operations.serializers import TweetSerializer, FollowerSerializer, LikeTweetSerializer, CommentSerializer


def validate_user_id(user_id):
    if not (user_id and user_id.isdigit() and User.objects.filter(pk=user_id).exists()):
        return Response(data={'error': ERROR_MESSAGES['INVALID_USER'].format(user_id)}, status=HTTP_400_BAD_REQUEST)
    return int(user_id)


def validate_tweet_id(tweet_id):
    if not (tweet_id and tweet_id.isdigit() and Tweet.objects.filter(pk=tweet_id).exists()):
        return Response(data={'error': ERROR_MESSAGES['INVALID_TWEET_ID'].format(tweet_id)}, status=HTTP_400_BAD_REQUEST)
    return int(tweet_id)


def post_tweet(params, user):
    tweet = params.get('tweet', '')
    if not tweet:
        return Response(data={'error': ERROR_MESSAGES['INVALID_TWEET']}, status=HTTP_400_BAD_REQUEST)

    params['user'] = user.pk
    params['created_at'] = datetime.now()
    tweet_serializer = TweetSerializer(data=params)
    if tweet_serializer.is_valid():
        tweet_serializer.save()
        return Response(data=tweet_serializer.data, status=HTTP_201_CREATED)
    else:
        return Response(data=tweet_serializer.errors, status=HTTP_400_BAD_REQUEST)


def follow_people(params, user):
    followed_user = validate_user_id(params.get('user_id'))
    if isinstance(followed_user, Response):
        return followed_user

    if Follower.objects.filter(follower_user_id=user.pk, followed_user_id=followed_user).exists():
        return Response(data={'error': ERROR_MESSAGES['ALREADY_FOLLOWING'].format(user.pk, followed_user)},
                        status=HTTP_400_BAD_REQUEST)

    if followed_user == user.pk:
        return Response(data={'error': ERROR_MESSAGES['INVALID_FOLLOWING'].format(user.pk, followed_user)},
                        status=HTTP_400_BAD_REQUEST)

    data_params = {
        'follower_user': user.pk,
        'followed_user': followed_user
    }
    follower_serializer = FollowerSerializer(data=data_params)
    if follower_serializer.is_valid():
        follower_serializer.save()
        return Response(data=follower_serializer.data, status=HTTP_201_CREATED)
    else:
        return Response(data=follower_serializer.errors, status=HTTP_400_BAD_REQUEST)


def unfollow_people(params, user):
    followed_user = validate_user_id(params.get('user_id'))
    if isinstance(followed_user, Response):
        return followed_user

    follower_queryset = Follower.objects.filter(follower_user_id=user.pk, followed_user_id=followed_user)
    if not follower_queryset.exists():
        return Response(data={'error': ERROR_MESSAGES['ALREADY_NOT_FOLLOWING'].format(user.pk, followed_user)},
                        status=HTTP_400_BAD_REQUEST)

    if followed_user == user.pk:
        return Response(data={'error': ERROR_MESSAGES['INVALID_FOLLOWING'].format(user.pk, followed_user)},
                        status=HTTP_400_BAD_REQUEST)

    follower_queryset.first().delete()
    return Response(data={'message': SUCCESS_MESSAGE['SUCCESSFULLY_UNFOLLOWED'].format(user.pk, followed_user)},
                    status=HTTP_200_OK)


def update_tweet(params, user):
    new_tweet = params.get('tweet', '')
    if not new_tweet:
        return Response(data={'error': ERROR_MESSAGES['INVALID_TWEET']}, status=HTTP_400_BAD_REQUEST)

    tweet_id = validate_tweet_id(params.get('tweet_id'))
    if isinstance(tweet_id, Response):
        return tweet_id

    tweet_queryset = Tweet.objects.filter(pk=tweet_id, user_id=user.pk)
    if not tweet_queryset.exists():
        return Response(data={'error': ERROR_MESSAGES['TWEET_NOT_FOUND'].format(tweet_id, user.pk)},
                        status=HTTP_400_BAD_REQUEST)

    tweet_queryset.update(tweet=new_tweet, modified_at=datetime.now())
    return Response(data={'message': SUCCESS_MESSAGE['SUCCESSFULLY_UPDATED'].format(tweet_id, new_tweet)},
                    status=HTTP_200_OK)


def delete_tweet(params, user):
    tweet_id = validate_tweet_id(params.get('tweet_id'))
    if isinstance(tweet_id, Response):
        return tweet_id

    tweet_queryset = Tweet.objects.filter(pk=tweet_id, user_id=user.pk)
    if not tweet_queryset.exists():
        return Response(data={'error': ERROR_MESSAGES['TWEET_NOT_FOUND'].format(tweet_id, user.pk)},
                        status=HTTP_400_BAD_REQUEST)

    tweet_queryset.delete()
    return Response(data={'message': SUCCESS_MESSAGE['SUCCESSFULLY_DELETED'].format(tweet_id)}, status=HTTP_200_OK)


def like_tweet(params, user):
    tweet_id = validate_tweet_id(params.get('tweet_id'))
    if isinstance(tweet_id, Response):
        return tweet_id

    if LikeTweet.objects.filter(user_id=user.pk, tweet_id=tweet_id).exists():
        return Response(data={'error': ERROR_MESSAGES['TWEET_ALREADY_LIKED'].format(tweet_id, user.pk)},
                        status=HTTP_400_BAD_REQUEST)

    params_data = {'tweet_id': tweet_id, 'user_id': user.pk}
    like_tweet_serializer = LikeTweetSerializer(data=params_data)
    if like_tweet_serializer.is_valid():
        like_tweet_serializer.save()
        return Response(data=like_tweet_serializer.data, status=HTTP_201_CREATED)
    else:
        return Response(data=like_tweet_serializer.errors, status=HTTP_400_BAD_REQUEST)


def unlike_tweet(params, user):
    tweet_id = validate_tweet_id(params.get('tweet_id'))
    if isinstance(tweet_id, Response):
        return tweet_id

    tweet_queryset = LikeTweet.objects.filter(user_id=user.pk, tweet_id=tweet_id)
    if not tweet_queryset.exists():
        return Response(data={'error': ERROR_MESSAGES['TWEET_NEVER_LIKED'].format(tweet_id, user.pk)},
                        status=HTTP_400_BAD_REQUEST)

    tweet_queryset.delete()
    return Response(data={'message': SUCCESS_MESSAGE['SUCCESSFULLY_UNLIKED'].format(tweet_id)}, status=HTTP_200_OK)


def comment_tweet(params, user):
    tweet_id = validate_tweet_id(params.get('tweet_id'))
    if isinstance(tweet_id, Response):
        return tweet_id

    if not params.get('comment'):
        return Response(data={'error': ERROR_MESSAGES['INVALID_COMMENT']},
                        status=HTTP_400_BAD_REQUEST)

    params_data = {
        'user_id': user.pk,
        'tweet_id': tweet_id,
        'comment': params.get('comment'),
        'created_at': datetime.now()
    }

    comment_serializer = CommentSerializer(data=params_data)
    if comment_serializer.is_valid():
        comment_serializer.save()
        return Response(data=comment_serializer.data, status=HTTP_201_CREATED)
    else:
        return Response(data=comment_serializer.errors, status=HTTP_400_BAD_REQUEST)


def upadte_comment(params, user):
    comment_id = params.get('comment_id')
    comment_queryset = Comment.objects.filter(pk=comment_id, user_id=user.pk)
    if not comment_id or not comment_id.isdigit() or not comment_queryset.exists():
        return Response(data={'error': ERROR_MESSAGES['INVALID_COMMENT_ID'].format(comment_id, user.pk)},
                        status=HTTP_400_BAD_REQUEST)

    new_comment = params.get('comment', '')
    if not new_comment:
        return Response(data={'error': ERROR_MESSAGES['INVALID_NEW_COMMENT']}, status=HTTP_400_BAD_REQUEST)

    comment_queryset.update(comment=new_comment, modified_at=datetime.now())
    return Response(data={'message': SUCCESS_MESSAGE['SUCCESSFULLY_UPDATED_COMMENT'].format(comment_id, new_comment)},
                    status=HTTP_200_OK)


def delete_comment(params, user):
    comment_id = params.get('comment_id')
    comment_queryset = Comment.objects.filter(pk=comment_id, user_id=user.pk)
    if not comment_id or not comment_id.isdigit() or not comment_queryset.exists():
        return Response(data={'error': ERROR_MESSAGES['INVALID_COMMENT_ID'].format(comment_id, user.pk)},
                        status=HTTP_400_BAD_REQUEST)

    comment_queryset.delete()
    return Response(data={'message': SUCCESS_MESSAGE['SUCCESSFULLY_DELETED_COMMENT'].format(comment_id)}, status=HTTP_200_OK)



