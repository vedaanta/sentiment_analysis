import json
import urllib
from twitter import Twitter, OAuth, TwitterHTTPError, TwitterStream

ACCESS_TOKEN = '532910413-HJ2Gm3TzWuyoMKmjmoHPsKB7TxeGZQTB384xmzy0'
ACCESS_SECRET = 'Jv3hq7rqOHnFoB7GogcwR5TeXlSAGvJlFQeRIA4RjqlbK'
CONSUMER_KEY = 'lwVRdqugXOcHXAhbl1SqkOKMZ'
CONSUMER_SECRET = '8O1bXQw5SoveRgaDEAaFX98qq2sxmfDyRYR9gQ4Zjzb9rubBTn'

oauth = OAuth(ACCESS_TOKEN, ACCESS_SECRET, CONSUMER_KEY, CONSUMER_SECRET)

twitter = Twitter(auth=oauth)

iterator = twitter.search.tweets(q="#ShahInGujarat150",lang='en',count=150)
f  = open('train.txt', 'w')
for result in iterator["statuses"]:
	tweet = json.loads(json.dumps(result).strip())
	if 'text' in tweet:
		print tweet['text']
		encoded_str = tweet['text'].encode("utf8").replace('\n',' ')
		print encoded_str
		f.write("positive\t"+encoded_str+'\n')

iterator = twitter.search.tweets(q="#AmitGoBack",lang='en',count=150)
f  = open('train.txt', 'w')
for result in iterator["statuses"]:
	tweet = json.loads(json.dumps(result).strip())
	if 'text' in tweet:
		print tweet['text']
		encoded_str = tweet['text'].encode("utf8").replace('\n',' ')
		print encoded_str
		f.write("negative\t"+encoded_str+'\n')
