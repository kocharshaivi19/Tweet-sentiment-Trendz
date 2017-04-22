import json
from kafka import KafkaConsumer
from textblob import TextBlob
from elasticsearch import Elasticsearch, RequestsHttpConnection

if __name__ == '__main__':
    print("Sentiment Analysis Begin!!")
    es_host = 'search-kafkaes-kexoskshytfpf53pbciezngzkq.us-west-2.es.amazonaws.com'
    es = Elasticsearch(host=es_host,
                       port=443,
                       use_ssl=True,
                       verify_certs=True,
                       connection_class=RequestsHttpConnection)
    while True:
        consumer = KafkaConsumer('tweetskafka', bootstrap_servers='172.31.36.206:9092', auto_offset_reset='earliest',
                                               value_deserializer = lambda m: json.loads(m.decode('ascii')))

        print("Publishing %d messages from queue")
        for tweet in consumer:
            text = tweet.value["title"]
            print text
            tweet.value['score'] = TextBlob(text).sentiment.polarity
            if tweet.value['score'] < -0.12:
                tweet.value['sentiment'] = 'negative'
            elif tweet.value['score'] >= -0.12 and tweet.value['score'] <= 0.12:
                tweet.value['sentiment'] = 'neutral'
            elif tweet.value['score'] > 0.12:
                tweet.value['sentiment'] = 'positive'
            else:
                tweet.value['sentiment'] = 'positive'

            print tweet.topic, tweet.value['id'], tweet.value

            es.index(index='tweetskafka-es', doc_type='tweet', id=tweet.value["id"], body=tweet.value)