from django.shortcuts import render
import tweepy
from tweepy import OAuthHandler, StreamListener, Stream
import time
import json
from elasticsearch import Elasticsearch, RequestsHttpConnection
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_protect, csrf_exempt
from django.views.decorators.http import require_GET
import geocoder

es_host = 'search-kafkaes-kexoskshytfpf53pbciezngzkq.us-west-2.es.amazonaws.com'

es = Elasticsearch(host = es_host,
                    port = 443,
                    use_ssl =True,
                    verify_certs = True,
                    connection_class=RequestsHttpConnection)

# class listener(StreamListener):
#     def __init__(self, time_limit=60):
#         self.time = time.time()
#         self.limit = time_limit
#         self.data = []
#         super(listener, self).__init__()
#
#
#     def on_data(self, data):
#         if (time.time() - self.time) < self.limit:
#             tweet_data = json.loads(data)
#             if tweet_data['place'] is not None:
#                 try:
#                     # self.data.append(tweet_data)
#                     # print tweet_data.keys()
#                     placecoord = tweet_data['place']['bounding_box']['coordinates'][0][0]
#                     print placecoord
#                     lat = placecoord[1]
#                     longi = placecoord[0]
#                     doc = {
#                         'title': tweet_data['text'],
#                         'location': {
#                             'lat': lat,
#                             'longi': longi
#                         }
#                     }
#                     # print doc['title']
#                     es.index(index="tweetindex", doc_type="Collections", id=tweet_data['id'], body=doc)
#                 except Exception as e:
#                     print "place error ", e
#                 return True
#             elif tweet_data['place'] is None and tweet_data['user'] is not None and tweet_data['user']['location'] is not None:
#                 try:
#                     doc = {
#                         'title' : tweet_data["text"],
#                         'location' : {
#                             'lat': geocoder.google(tweet_data['user']['location']).latlng[0],
#                             'longi': geocoder.google(tweet_data['user']['location']).latlng[1],
#                         }
#                     }
#                     es.index(index="tweetindex", doc_type="Collections", id=tweet_data['id'], body=doc)
#                 except Exception as e:
#                     print "user error ", e
#                 return True
#             elif tweet_data['place'] is None and tweet_data['user']['location'] is None:
#                 print "else loop"
#                 return True
#         else:
#             return False
#
#     def appendfile(self):
#         with open('./raw_1.json', 'w') as f:
#             json.dump(self.data, f)
#
#     def on_error(self, status):
#         print("response: %s" % status)
#         if status == 420:
#             return False

# @csrf_protect
# def filter(request):
#     print "yes"
#     if request.method == "POST":
#         try:
#             print request.method
#             if 'input' in request.POST:
#                 query = str(request.POST.get('input', ''))
#                 # print query
#                 try:
#                     l = listener(time_limit=30)
#                     twitter_stream = Stream(auth, l)
#                     twitter_stream.filter(track=[query])
#                     tweets = es.search(index='tweetindex',doc_type="Collections", body={"from": 0, "size": 1000, "query": {"match": {"title":query}}})
#                     # print tweets.keys()
#                     latlonginfo = []
#                     for tweet in tweets['hits']['hits']:
#                         info = {}
#                         info['lat'] = tweet['_source']['location']['lat']
#                         info['longi'] = tweet['_source']['location']['longi']
#                         info['title'] = tweet['_source']['title']
#                         latlonginfo.append(info)
#                         print (info)
#                     print latlonginfo
#                     return JsonResponse({'tweets': latlonginfo})
#                 except Exception as e:
#                     print e
#                     return HttpResponse('Error')
#         except Exception as e:
#             print e

# @csrf_protect
# def init(request):
#     api = tweepy.API(auth)
#     trends = api.trends_place(1)
#     trending_topic_names = []
#     for vol in (val for item, val in trends[0].iteritems() if item == 'trends'):
#         trending_topic_indx = sorted(range(len(vol)), key=lambda k: vol[k]['tweet_volume'])[::-10]
#         for i, _ in enumerate(trending_topic_indx):
#             if vol[i]['tweet_volume'] is not None:
#                 trending_topic_names.append(vol[i]['name'])
#         # trending_topic_names = [vol[i]['name'] for i in trending_topic_indx]
#
#     print(trending_topic_names)
#     return render(request, 'TweetMap/home.html', {'trendings': trending_topic_names})

# @csrf_exempt
# def snsnotification(request):
#     body = json.loads(request.body.decode("utf-8"))
#     print(type(body))
#     hdr = body['Type']
#     if hdr == 'SubscriptionConfirmation':
#         url = body['SubscribeURL']
#         print("Subscription Confirmation - Visiting URL : " + url)
#         http = urllib3.PoolManager()
#         r = http.request('GET', url)
#     print(r.status)
#
#     if hdr == 'Notification':
#         print("SNS Notification")
#         tweet = json.loads(body['Message'])
#         es.index(index='TweetSentiments', doc_type='tweet', id=tweet["id"], body=tweet)
#
#     return HttpResponse(status=200)

@csrf_protect
def senti_init(request):
    li = ['DragRace', 'ThingsToBeAshamedOf', 'Kadri', 'Gerald Green',
          'Madison Bumgarner', 'poweroutage','SelfiesForGirlsongirls']
    return render(request, 'TweetMap/tweetsenti.html')

@csrf_protect
def sentifilter(request):
    print "yes"
    if request.method == "POST":
        try:
            print request.method
            if 'input' in request.POST:
                query = str(request.POST.get('input', ''))
                print query
                try:
                    if query == 'All' or query == '' or query == None:
                        elasticQuery = {
                            'match_all':{}
                        }
                    else:
                        elasticQuery = {
                            "query_string": {
                                "query": query.lower()
                            }
                        }
                    tweets = es.search(index='tweetskafka',doc_type="tweet", body=
                                        {"sort" :[ {"id" : {"order" : "desc"} }], "from": 0, "size": 1000, "query": elasticQuery})
                    latlonginfo = []
                    for tweet in tweets['hits']['hits']:
                        info = {}
                        info['lat'] = tweet['_source']['location']['lat']
                        info['longi'] = tweet['_source']['location']['longi']
                        info['title'] = tweet['_source']['title']
                        info['sentiment'] = tweet['_source']['sentiment']
                        info['score'] = tweet['_source']['score']
                        latlonginfo.append(info)
                        print (info)
                    print latlonginfo
                    return JsonResponse({'tweets': latlonginfo})
                except Exception as e:
                    print e
                    return HttpResponse('Error')
        except Exception as e:
            print e

