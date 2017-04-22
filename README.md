# Tweet-sentiment-Trendz
This web application is a scalable version of <a href="https://github.com/shaivikochar/Tweetrendz">Tweettrendz</a>.
This application uses Twitter Streaming API to fetch tweets from the twitter hose in real-time with 
Geolocation & English Language Filtering and plot the tweets on a map along with the sentiment of the tweet.

### Application utilises:
- Google Map API: Plotting the tweets on a map with customised Markers
- Elastic Search: Efficient searching of tweets based on keywords stored in JSON format on AWS ElasticSearch Service
- Textblob Sentiment Analysis API: This generates the positive, negative or neutral sentiment evaluation for the text of the submitted Tweet.
- Apache Kafka: A queueing service to store the streamed tweets making them available for consumption and notification service that notifies the subscriber of new available tweets.

### Run the application:
- Download the project
- Add/Change Twitter, AWS, and MonkeyLearn API Keys in config.ini file.
- Run manage.py file
  ```python
   python manage.py runserver
   ```
- Run sentiment.py and kafkatweets.py on AWS instance, if you have created one. Else, you can look onto the instructions below

### Installation instruction of Apache Kafka on AWS:
- Install Kafka by downloading
	```bash
  sudo apt-get install default-jre
  sudo apt-get install zookeeperd
  wget "http://mirror.cc.columbia.edu/pub/software/apache/kafka/0.10.2.0/kafka_2.11-0.10.2.0.tgz"
  tar -xzf kafka_2.11-0.10.2.0.tgz
  ```
- Run the Zookeeper
  ```bash
  cd kafka_2.11-0.10.2.0
  bin/zookeeper-server-start.sh config/zookeeper.properties
  ```
- In config/server.properties, add the following lines
	listeners=PLAINTEXT://<your-instance-privateIP>:9092
	advertise.listeners=PLAINTEXT://<your-instance-privateIP>:9092
	To save the read-only file, 
  ```bash
  :w !sudo tee %
  O
  :q!
  ```
- Run the Kafka server on another Instaance's terminal 
  ``` bash
	KAFKA_HEAP_OPTS="-Xms512M -Xmx512M" bin/kafka-server-start.sh config/server.properties
  ```
- Finally, Run the below commands on different Instance's terminal
  ```
  python sentiment.py
  python kafkatweets.py
  ```
