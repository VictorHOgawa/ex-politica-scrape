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
    "directUrls": [f"https://www.instagram.com/{instagram_name}" for instagram_name in instagram_names],
    "resultsType": "details",
    "resultsLimit": 20,
    "addParentData": False,
    "searchType": "hashtag",
    "searchLimit": 1,
    "untilDate": last_week
}

run = client.actor("shu8hvrXbJbY3Eb9W").call(run_input=run_input)

json_array = []
for item in client.dataset(run["defaultDatasetId"]).iterate_items():
    json_data = json.dumps(item, ensure_ascii=False)
    json_array.append(json.loads(json_data))
    
    for item in json_array:
        for instagram_name, instagram_id in zip(instagram_names, instagram_ids):
            if item["username"].lower() == instagram_name.lower():
                item["instagram_id"] = instagram_id
    
    json_str = json.dumps(json_array, indent=4, ensure_ascii=False)

with open("/home/scrapeops/Axioon/Apify/Results/Instagram/Instagram_Profiles.json", "w") as f:
    f.write(json_str)
    
upload_file("/home/scrapeops/Axioon/Apify/Results/Instagram/Instagram_Profiles.json", "nightapp", f"Apify/Instagram/Profiles/Instagram_Profiles_{timestamp}.json")

file_name = requests.post("http://18.231.150.215/webhook/instagram/profile", json={"records": f"Apify/Instagram/Profiles/Instagram_Profiles_{timestamp}.json"})
