import tweepy
from tweepy import OAuthHandler, StreamListener, Stream
import time
import json
from kafka import KafkaProducer
import ConfigParser


Config = ConfigParser.ConfigParser()
Config.read("../../config.ini")

twitter_auth = OAuthHandler(Config.get('twitter', 'consumer_key'), Config.get('twitter', 'consumer_secret'))
twitter_auth.set_access_token(Config.get('twitter', 'access_token'), Config.get('twitter', 'access_token_secret'))
twitter_api = tweepy.API(twitter_auth, wait_on_rate_limit_notify=True, retry_count=3, retry_delay=5)

print("######### Twitter Authentication Success ######")

class messagelistener(StreamListener):
    def __init__(self):
        self.count = 0
        self.producer = KafkaProducer(bootstrap_servers='172.31.36.206:9092',
                                      value_serializer=lambda m: json.dumps(m).encode('ascii'))
        super(StreamListener, self).__init__()

    def on_data(self, data):
        tweet_data = json.loads(data)
        if tweet_data['place'] is not None:
            try:
                placecoord = tweet_data['place']['bounding_box']['coordinates'][0][0]
                print placecoord
                lat = placecoord[1]
                longi = placecoord[0]
                username = tweet_data['user']['name']
                doc = {
                    'id': tweet_data['id'],
                    'username' : username,
                    'title': tweet_data['text'],
                    'location': {
                        'lat': lat,
                        'longi': longi
                    },
                    'created_at': tweet_data['created_at'],
                }
                print doc
                self.count += 1
                if self.count == 10:
                    self.count = 0
                    print("Sleeping")
                    time.sleep(10)

                self.producer.send('tweetskafka', doc)

            except Exception as e:
                print "Place is there with exception", e
        else:
            print "No geolocation"

    def on_error(self, status_code):
        if status_code == 420:
            print ("Rate Limit")
            return True

if __name__ == '__main__':
    print("Twitter Stream Begin!!")
    l = messagelistener()
    while True:
        try:
            twitter_stream = Stream(twitter_api.auth, l)
            twitter_stream.filter(track=['nationalhighfiveday','Ted Nugent',
                                         'Sabres','Tim Murray','Tim Phillips',
                                         'MyWorldRevolvesAround', 'Scott Brown',
                                         'trump', 'Snapchat', 'Kadri', 'poweroutage', 'Kylie'],
                                  languages=['en'])
        except Exception as e:
            print (e)