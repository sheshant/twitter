

ERROR_MESSAGES = {
    'INVALID_USER': 'user id "{}" not found',
    'INVALID_TWEET': 'tweet cannot be empty or null',
    'NON_INTEGER_USER_ID': 'please send user_id as integer',
    'ALREADY_FOLLOWING': 'USER ID {} already following USER ID {}',
    'ALREADY_NOT_FOLLOWING': 'USER ID {} already not following USER ID {}',
    'INVALID_FOLLOWING': 'cant follow/unfollow yourself',
    'INVALID_TWEET_ID': 'Tweet id not valid "{}"',
    'TWEET_NOT_FOUND': 'Tweet id "{}" for user id "{}" not found',
    'TWEET_ALREADY_LIKED': 'Tweet id "{}" already liked by user id "{}"',
    'TWEET_NEVER_LIKED': 'Tweet id "{}" never liked by user id "{}"',
    'INVALID_COMMENT': 'no comment provided',
    'INVALID_NEW_COMMENT': 'comment cannot be empty or null',
    'INVALID_COMMENT_ID': 'Comment id "{}" for user id "{}" not found',
}


SUCCESS_MESSAGE = {
    'SUCCESSFULLY_UNFOLLOWED': 'USER ID {} successfully unfollowed USER ID {}',
    'SUCCESSFULLY_DELETED': 'successfully deleted tweet id "{}"',
    'SUCCESSFULLY_DELETED_COMMENT': 'successfully deleted comment id "{}"',
    'SUCCESSFULLY_UNLIKED': 'successfully unliked tweet id "{}"',
    'SUCCESSFULLY_UPDATED': 'successfully updated tweet id "{}" to "{}"',
    'SUCCESSFULLY_UPDATED_COMMENT': 'successfully updated comment id "{}" to "{}"',
}
