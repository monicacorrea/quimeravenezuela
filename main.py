import tweepy
import csv

client = tweepy.Client(bearer_token='YOUR-DETAILS-HERE')


# Name and path of the file 
file_name = 'tweets.csv'

# Replace with your own search query/quieries
queries = [
    'soñe, venezuela -is:retweet lang:es',
    'soñe, maracaibo -is:retweet lang:es',
    'soñe, caracas -is:retweet lang:es',
    'soñe, amazonas -is:retweet lang:es'
]

# Open CSV file for writing
with open(file_name, 'w', newline='') as filehandle:
    writer = csv.writer(filehandle, delimiter=',', quotechar='"', quoting=csv.QUOTE_ALL)

    # Go through each query
    for query in queries:
        # Search result for current query
        tweets = client.search_recent_tweets(query=query, tweet_fields=['context_annotations', 'created_at'], user_fields=['profile_image_url'], expansions='author_id', max_results=100)
        
        # Ignore empty response
        if tweets.meta['result_count'] != 0:
            # Get users list from the includes object
            users = {u["id"]: u for u in tweets.includes['users']}

            # Go through each tweet
            for tweet in tweets.data:
                if users[tweet.author_id]:
                    user = users[tweet.author_id]
                    
                    # Save to CSV
                    writer.writerow([tweet.created_at, user,tweet.text.replace('\n', '\\n').replace('"', '')])
                    
                    # Print to user
                    print(tweet.created_at, user, tweet.text.replace('\n', '\\n'))
            
