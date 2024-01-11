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

input = requests.get("http://18.231.150.215/scrape/youtube")

input = input.json()

input = input["youtube"]

channel_names = [item["youtube"] for item in input]

channel_ids = [item["id"] for item in input]

client = ApifyClient(os.getenv("YOUTUBE_APIFY_CLIENT_KEY"))

run_input = {
    "dateFilter": last_week,
    "details": True,
    "proxySettings": {
        "useApifyProxy": True
    },
    "start_urls": [{"url": f"https://www.youtube.com/@{channel_name}"} for channel_name in channel_names]
}

run = client.actor("TyjYgGDGcTNVmil8z").call(run_input=run_input)

json_array = []
posts_set = set()
for item in client.dataset(run["defaultDatasetId"]).iterate_items():
    json_data = json.dumps(item, ensure_ascii=False)
    json_array.append(json.loads(json_data))
    
    for item in json_array:
        if item["url"]:
            posts_set.add(item["url"])
        for channel_name, channel_id in zip(channel_names, channel_ids):
            if item["inputChannelUrl"].lower() == f"https://www.youtube.com/@{channel_name}/about".lower():
                item["channel_id"] = channel_id
                
    json_str = json.dumps(json_array, indent=4, ensure_ascii=False)
    posts_array = list(posts_set)
    posts_str = json.dumps(posts_array, indent=4, ensure_ascii=False)

with open("/home/scrapeops/Axioon/Apify/Results/Youtube/Youtube_Videos.json", "w") as f:
    f.write(json_str)

with open("/home/scrapeops/Axioon/Apify/Results/Youtube/Youtube_Videos_Urls.json", "w") as f:
    f.write(posts_str)
    
upload_file(f"/home/scrapeops/Axioon/Apify/Results/Youtube/Youtube_Videos.json", "nightapp", f"Apify/YouTube/Videos/YouTube_Videos_{timestamp}.json")

file_name = requests.post("http://18.231.150.215/webhook/youtube/video", json={"records": f"Apify/YouTube/Videos/YouTube_Videos_{timestamp}.json"})