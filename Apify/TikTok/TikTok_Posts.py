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

input = requests.get("http://18.231.150.215/scrape/tiktok")

input = input.json()

input = input["tiktok"]

tiktok_names = [item["tiktok"] for item in input]

tiktok_ids = [item["id"] for item in input]

client = ApifyClient(os.getenv("TIKTOK_APIFY_CLIENT_KEY"))

for tiktok_name, tiktok_id in zip(tiktok_names, tiktok_ids):
    
    run_input = {
        "disableCheerioBoost": False,
        "disableEnrichAuthorStats": False,
        "profiles": [tiktok_name],
        "shouldDownloadCovers": False,
        "shouldDownloadSlideshowImages": False,
        "shouldDownloadVideos": False
    }
    run = client.actor("OtzYfK1ndEGdwWFKQ").call(run_input=run_input)

    json_array = []
    json_str = ""
    posts_str = ""
    posts_set = set()
    for item in client.dataset(run["defaultDatasetId"]).iterate_items():
        json_data = json.dumps(item, ensure_ascii=False)
        json_array.append(json.loads(json_data))
        
        for item in json_array:
            if item["webVideoUrl"]:
                posts_set.add(item["webVideoUrl"])
                if tiktok_name.lower() in item["webVideoUrl"].lower():
                    item["tiktok_id"] = tiktok_id

        json_str = json.dumps(json_array, ensure_ascii=False, indent=4)
        posts_array = list(posts_set)
        posts_str = json.dumps(posts_array, ensure_ascii=False, indent=4)

    if json_str != "":
        with open(f"/home/scrapeops/Axioon/Apify/Results/TikTok/TikTok_Posts_{tiktok_name}.json", "w") as f:
            f.write(json_str)

    if posts_str != "":
        with open(f"/home/scrapeops/Axioon/Apify/Results/TikTok/TikTok_Posts_Urls_{tiktok_name}.json", "w") as f:
            f.write(posts_str)
        
    if json_str != "":
        upload_file(f"/home/scrapeops/Axioon/Apify/Results/TikTok/TikTok_Posts_{tiktok_name}.json", "nightapp", f"Apify/TikTok/Posts/TikTok_Posts_{tiktok_name}_{timestamp}.json")

    if json_str != "":
        file_name = requests.post("http://18.231.150.215/webhook/tiktok", json={"records": f"Apify/TikTok/Posts/TikTok_Posts_{tiktok_name}_{timestamp}.json"})
