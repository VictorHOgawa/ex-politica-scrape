from datetime import date, datetime, timedelta
from ...upload_file import upload_file
from apify_client import ApifyClient
from dotenv import load_dotenv
import requests
import json
import os

load_dotenv()

now = datetime.now()
timestamp = datetime.timestamp(now)
last_week = date.today() - timedelta(days=7)

input = requests.get("http://18.231.150.215/scrape/instagram")

input = input.json()

input = input["instagram"]

instagram_names = [item["instagram"] for item in input]

instagram_ids = [item["id"] for item in input]

client = ApifyClient(os.getenv("INSTAGRAM_APIFY_CLIENT_KEY"))

run_input = {
    "username": [f"{instagram_name}" for instagram_name in instagram_names],
    "resultsLimit": 10,
}

run = client.actor("zTSjdcGqjg6KEIBlt").call(run_input=run_input)

json_array = []
posts_set = set()
for item in client.dataset(run["defaultDatasetId"]).iterate_items():
    json_data = json.dumps(item, ensure_ascii=False)
    json_array.append(json.loads(json_data))
    
    for item in json_array:
        if "taggedUsers" in item:
            if item["url"]:
                posts_set.add(item["url"])
            for taggedUser in item["taggedUsers"]:
                for instagram_name, instagram_id in zip(instagram_names, instagram_ids):
                    if taggedUser["username"].lower() == instagram_name.lower():
                        item["instagram_id"] = instagram_id
                        item["instagram_username"] = instagram_name

    json_str = json.dumps(json_array, ensure_ascii=False, indent=4)
    posts_array = list(posts_set)
    posts_str = json.dumps(posts_array, indent=4, ensure_ascii=False)
    
with open ("/home/scrapeops/Axioon/Apify/Results/Instagram/Instagram_Mentions.json", "w") as f:
    f.write(json_str)

with open("/home/scrapeops/Axioon/Apify/Results/Instagram/Instagram_Mentions_Urls.json", "w") as f:
    f.write(posts_str)
    
upload_file("/home/scrapeops/Axioon/Apify/Results/Instagram/Instagram_Mentions.json", "nightapp", f"Apify/Instagram/Mentions/Instagram_Mentions_{timestamp}.json")

file_name = requests.post("http://18.231.150.215/webhook/instagram/mentions", json={"records": f"Apify/Instagram/Mentions/Instagram_Mentions_{timestamp}.json"})
