import tweepy
import csv

# Token de una cuenta con acceso 
bearer_token = "YOUR-DETAILS-HERE"
client = tweepy.Client(bearer_token=bearer_token, wait_on_rate_limit=True)

# Nombre del archivo CSV
file_name = "tweets.csv"

# Queries segun plan
queries = [
    "soñe venezuela -is:retweet lang:es"
]

with open(file_name, "w", newline="", encoding="utf-8") as filehandle:
    writer = csv.writer(filehandle, delimiter=",", quotechar='"', quoting=csv.QUOTE_ALL)
    writer.writerow(["created_at", "username", "text"])  # cabecera CSV

    for query in queries:
        # Expansions
        response = client.search_recent_tweets(
            query=query,
            tweet_fields=["created_at", "lang"],
            user_fields=["username", "profile_image_url"],
            expansions=["author_id"],
            max_results=100,
        )

        if response.data is None:
            continue

        # Los usuarios vienen en includes
        users = {u["id"]: u for u in response.includes["users"]} if response.includes else {}

        for tweet in response.data:
            user = users.get(tweet.author_id, {})
            username = user.get("username", "desconocido")

            text = tweet.text.replace("\n", "\\n").replace('"', "")
            writer.writerow([tweet.created_at, username, text])

            print(tweet.created_at, username, text)
