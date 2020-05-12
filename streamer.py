# CS PROJECT 2020

from tweepy import API
from tweepy import Cursor
from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream
import twitter_credentials_master
import time

# TODO when client responds to server post via reply, the stream picks that thinking its a post from the server which
#  results in an error when splitting in on_data


class TwitterClient:
    """
    Class for viewing the timeline tweets.
    """

    def __init__(self, twitter_user=None):
        self.auth = TwitterAuthenticator().authenticate_twitter_app()
        self.twitter_client = API(self.auth)
        self.user_timeline = twitter_user

    def get_user_timeline_tweets(self, num_tweets):
        """
        Returns a list of tweets from the timeline of the user.
        :param num_tweets: number of tweets to return from the latest.
        ;param ret_link_flag: flag that indicates if tweet has a shortened link.
        :return: list of timeline tweets.
        """
        timeline_tweets = []
        for tweet in Cursor(self.twitter_client.user_timeline).items(num_tweets):
            # user_timeline is set to the default value of the
            # user using the API.
            timeline_tweets.append(tweet.text)
        return timeline_tweets

    def get_user_timeline_replies(self, num_tweets, ret_link_flag = False):
        """
        Returns a list of tweets from the timeline of the user.
        :param num_tweets: number of tweets to return from the latest.
        ;param ret_link_flag: ....
        :return: list of timeline tweets.
        """
        timeline_tweets = []

        if not ret_link_flag:
            for tweet in Cursor(self.twitter_client.user_timeline).items(num_tweets):
                # user_timeline is set to the default value of the user using the API.

                # Loop as long as the post is a reply.
                if str(tweet.in_reply_to_status_id) != 'None':
                    timeline_tweets.append(tweet.text)
                else:
                    return timeline_tweets
            return timeline_tweets

        else:
            for tweet in Cursor(self.twitter_client.user_timeline,  tweet_mode='extended').items(num_tweets):
                # user_timeline is set to the default value of the user using the API.

                if ret_link_flag and str(tweet.in_reply_to_status_id) != 'None':
                    # print(tweet.entities['urls'][0]['expanded_url'])

                    # Getting the correct un tempered link and pairing it with the correct text
                    timeline_tweets.append(tweet.full_text.split(':')[0] + ': ' +
                                           tweet.entities['urls'][0]['expanded_url'])

                else:
                    return timeline_tweets

            return timeline_tweets


# # # # TWITTER API AUTHENTICATOR # # # #
class TwitterAuthenticator:
    """
    Class for authenticating with the Twitter API.
    """

    @staticmethod
    def authenticate_twitter_app():
        """
        Method that performs the authentication with the API with the 4 keys.
        :return: authentication object
        """
        auth = OAuthHandler(twitter_credentials_master.CONSUMER_KEY, twitter_credentials_master.CONSUMER_KEY_SECRET)
        auth.set_access_token(twitter_credentials_master.ACCESS_TOKEN, twitter_credentials_master.ACCESS_TOKEN_SECRET)
        return auth


# # # # TWEETS STREAM # # # #
class TwitterStreamer:
    """
    Class for streaming and processing streamed-live tweets.
    """

    def __init__(self):
        self.twitter_authenticator = TwitterAuthenticator()

    def write_streamed_tweets(self, tweet_stream_file, key_list):
        """
        Method that handles authentication and connection with the twitter API
        :param tweet_stream_file: The file that the streamed
        tweets will be written to.
        :param key_list: The filter option - filter by a
        given list of hashtags.
        """

        # Twitter authentication and connection.
        listener = TweetsListener(tweet_stream_file)
        auth = self.twitter_authenticator.authenticate_twitter_app()
        stream = Stream(auth, listener)

        # Filter Twitter stream by keywords.
        stream.filter(follow=key_list)

    @staticmethod
    def stream():
        keyword_list = ['1183062885808988163']
        fetched_tweets_filename = 'Support/tweets.txt'

        twitter_streamer = TwitterStreamer()
        twitter_streamer.write_streamed_tweets(fetched_tweets_filename, keyword_list)


# # # # TWEET STREAM LISTENER # # # #
class TweetsListener(StreamListener):
    """
    Basic class that prints received tweets.
    """

    def __init__(self, tweet_stream_file):
        StreamListener.__init__(self)
        self.tweet_stream_file = tweet_stream_file

    def on_data(self, data):

        # If a reply ignore this tweet
        if DataAnalyzer.check_reply(data):
            print('Ignoring the tweet')
            return True
        print('Not ignoring the tweet')

        # Trying to write to tweets.py reply
        try:
            data = DataAnalyzer.extract_media_url(data)
            data = data.replace('media_url:', '')
            # print(data)
            with open(self.tweet_stream_file, 'a') as file:
                # file.write(data + '\n')
                file.write(data)
            return True

        except BaseException as ex:
            print('Error with data: ' + str(ex))
        return True

    def on_error(self, status):
        """
        Method that handles errors.
        :param status: error received.
        :return: False if app needs to be stopped.
        """
        if status == 420:
            # Return false on_data method if rate limit occurs -
            # too many request will result in a warning.
            return False
        print(status)


class DataAnalyzer:
    """
    Class to analyze streamed data.
    """

    @staticmethod
    def extract_text(data):
        data_text_bit = data.split(',')[3]
        # Data text bit: '"text":"RAW DATA"'
        raw_text = data_text_bit.replace('"', '').replace('text:', '')
        return raw_text

    @staticmethod
    def extract_media_url(data):
        data_text_bit = data.split(',')[69]
        # Data media https url: '"media_url_https":"URL"'
        raw_url = data_text_bit.replace('"', '').replace('media_url_https:', '')
        raw_url = raw_url.replace('\\', '')

        HandlePost.recent_post_id = DataAnalyzer.extract_status_id(data)
        print(HandlePost.recent_post_id)

        HandlePost.is_reply = DataAnalyzer.check_reply(data)

        return raw_url

    @staticmethod
    def extract_status_id(data):
        data_status_id_bit = data.split(',')[2]
        print(data_status_id_bit)
        raw_id = data_status_id_bit.replace('"', '').replace('id_str:', '')
        raw_id = raw_id.replace('\\', '')
        return raw_id

    @staticmethod
    def check_reply(data):
        data_status_id_bit = data.split(',')[8]
        print(data_status_id_bit)
        raw_id = data_status_id_bit.replace('"', '').replace('in_reply_to_status_id:', '')

        # This line of code is here because reply json is built in a different way.
        if 'in_reply_to_user_id:' in raw_id:
            return True

        # If reply return true
        return raw_id != 'null'


class HandlePost:
    """
    A class used to post a tweet with an encoded image and a status.
    """

    # Id of the recent post received
    recent_post_id = ''
    is_reply = False

    @staticmethod
    def post_tweet(filename, message):
        """
        Simple method that posts a tweet with an image and status.
        :param filename: The path to the encoded image to upload.
        :param message: The message to post as status.
        """
        auth = TwitterAuthenticator.authenticate_twitter_app()
        tweet_poster = API(auth)
        tweet_poster.update_with_media(filename, message)
        print('[!]  The post has been uploaded with the encoded image')

    @staticmethod
    def post_comment(status_id, message):
        auth = TwitterAuthenticator.authenticate_twitter_app()
        comment_post = API(auth)
        comment_post.update_status(message, status_id)


if __name__ == '__main__':
    pass
    # List of twitter users' ids to filter.
    # keyword_list = ['1183062885808988163']
    # keyword_list = ['donald trump']

    # File to save streamed tweets to.
    #fetched_tweets_filename = 'tweets.txt'

    # Get top tweets from user timeline.
    # twitter_client = TwitterClient()
    # print(twitter_client.get_user_timeline_tweets(1))

    # Listen and filter stream.
    #twitter_streamer = TwitterStreamer()
    #twitter_streamer.write_streamed_tweets(fetched_tweets_filename, keyword_list)
