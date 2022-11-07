import tweepy
import csv

client = tweepy.Client(bearer_token='YOUR-DETAILS-HERE')


# Search query
query = 'venezuela, soñé -is:retweet lang:es'

# Name of the output file 
file_name = 'tweets.csv'

#search and results
tweets = client.search_recent_tweets(query=query, tweet_fields=['context_annotations', 'created_at'],
                                     user_fields=['profile_image_url'], expansions='author_id', max_results=100)

# Get users list from the includes object
users = {u["id"]: u for u in tweets.includes['users']}

with open(file_name, 'w', newline='') as filehandle:
    writer = csv.writer(filehandle, delimiter=',', quotechar='"', quoting=csv.QUOTE_ALL)
    
    for tweet in tweets.data:
        if users[tweet.author_id]:
            user = users[tweet.author_id]
            writer.writerow([tweet.created_at, user,tweet.text.replace('\n', '\\n').replace('"', '')])
            print(tweet.created_at, user, tweet.text.replace('\n', '\\n'))
            
