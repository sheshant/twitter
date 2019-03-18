from django.conf.urls import url
from rest_framework.authtoken.views import obtain_auth_token

from twitter_operations.views import UserRudView, PostTweet, FollowPeople, ShowFollowers, ShowFollowing, UserTimeline, \
    HomeTimeline, UpdateTweet, DeleteTweet, CommentTweet, UpdateComment, DeleteComment, GetAllComments, \
    UnlikeTweet, GetAllLikesToTweet, GetAllLikedTweets, UnfollowPeople, LikeATweet

urlpatterns = [
    url(r'^(?P<pk>\d+)/$', UserRudView.as_view(), name='post-rud'),
    url(r'^api-token-auth/', obtain_auth_token),

    url(r'^post_tweet/$', PostTweet.as_view(), name='post_tweet'),
    url(r'^follow_people/$', FollowPeople.as_view(), name='follow_people'),
    url(r'^unfollow_people/$', UnfollowPeople.as_view(), name='unfollow_people'),
    url(r'^show_followers/$', ShowFollowers.as_view(), name='show_followers'),
    url(r'^show_following/$', ShowFollowing.as_view(), name='show_following'),
    url(r'^user_timeline/$', UserTimeline.as_view(), name='user_timeline'),
    url(r'^home_timeline/$', HomeTimeline.as_view(), name='home_timeline'),
    url(r'^update_tweet/$', UpdateTweet.as_view(), name='update_tweet'),
    url(r'^delete_tweet/$', DeleteTweet.as_view(), name='delete_tweet'),
    url(r'^comment_tweet/$', CommentTweet.as_view(), name='comment_tweet'),
    url(r'^update_comment/$', UpdateComment.as_view(), name='update_comment'),
    url(r'^delete_comment/$', DeleteComment.as_view(), name='delete_comment'),
    url(r'^get_all_comments/$', GetAllComments.as_view(), name='get_all_comments'),
    url(r'^like_tweet/$', LikeATweet.as_view(), name='like_tweet'),
    url(r'^unlike_tweet/$', UnlikeTweet.as_view(), name='unlike_tweet'),
    url(r'^get_all_likes_to_tweet/$', GetAllLikesToTweet.as_view(), name='get_all_likes_to_tweet'),
    url(r'^get_all_liked_tweets/$', GetAllLikedTweets.as_view(), name='get_all_liked_tweets'),
]
