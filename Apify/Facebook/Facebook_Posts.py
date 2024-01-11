from ...upload_file import upload_file
from apify_client import ApifyClient
from dotenv import load_dotenv
from datetime import datetime
import requests
import json
import os

load_dotenv()

now = datetime.now()
timestamp = datetime.timestamp(now)

input = requests.get("http://18.231.150.215/scrape/facebook")

input = input.json()

input = input["facebook"]

facebook_names = [item["facebook"] for item in input]

facebook_ids = [item["id"] for item in input]

client = ApifyClient(os.getenv("FACEBOOK_APIFY_CLIENT_KEY"))

run_input = {
    "resultsLimit": 5,
    "startUrls": [
        { "url": f"https://www.facebook.com/{facebook_name}/" } for facebook_name in facebook_names
    ] }

run = client.actor("KoJrdxJCTtpon81KY").call(run_input=run_input)

json_array = []
posts_set = set()
for item in client.dataset(run["defaultDatasetId"]).iterate_items():
    json_data = json.dumps(item, ensure_ascii=False)
    json_array.append(json.loads(json_data))
    
    for item in json_array:
        if item["topLevelUrl"]:
            posts_set.add(item["topLevelUrl"])
        for facebook_name, facebook_id in zip(facebook_names, facebook_ids):
            if item["facebookUrl"].lower() == f"https://www.facebook.com/{facebook_name}/".lower():
                item["facebook_id"] = facebook_id
        
    json_str = json.dumps(json_array, indent=4, ensure_ascii=False)
    posts_array = list(posts_set)
    posts_str = json.dumps(posts_array, indent=4, ensure_ascii=False)
    
with open("/home/scrapeops/Axioon/Apify/Results/Facebook/Facebook_Posts.json", "w") as f:
    f.write(json_str)
    
with open("/home/scrapeops/Axioon/Apify/Results/Facebook/Facebook_Posts_Urls.json", "w") as f:
    f.write(posts_str)
    
upload_file("/home/scrapeops/Axioon/Apify/Results/Facebook/Facebook_Posts.json", "nightapp", f"Apify/Facebook/Posts/Facebook_Posts_{timestamp}.json")

file_name = requests.post("http://18.231.150.215/webhook/facebook/posts", json={"records": f"Apify/Facebook/Posts/Facebook_Posts_{timestamp}.json"})