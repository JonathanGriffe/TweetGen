import requests
import json
import pickle
import re
import os

BEARER_TOKEN = os.environ.get("BEARER_TOKEN")

id = 44196397


def pullTweets(id):
    url = f"https://api.twitter.com/2/users/{id}/tweets?exclude=retweets&max_results=100&tweet.fields=text"
    res = {"meta": {"next_token": ""}}
    tweetList = []
    while "meta" in res and "next_token" in res["meta"]:
        next_token = res["meta"]["next_token"]
        urlReq = url if not next_token else url + f"&pagination_token={next_token}"
        resString = requests.get(urlReq, headers={"Authorization": f"Bearer {BEARER_TOKEN}"})
        res = json.loads(resString.text)
        if "data" in res:
            tweetList.extend([d['text'] for d in res["data"]])
    with open('data/' + str(id), 'w') as file:
        tweetList = [re.sub(r'http\S+', '', code.encode('utf-8', errors='ignore').decode('utf-8').replace("\n", "")) + "\n" for code in tweetList]
        tweetList = list(filter(lambda tweet: len(tweet) >= 30, tweetList))
        print(len(tweetList))
        file.writelines(tweetList)


pullTweets(id)