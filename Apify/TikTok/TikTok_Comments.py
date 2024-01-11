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

with open("/home/scrapeops/Axioon/Apify/Results/TikTok/TikTok_Posts_Urls.json") as f:
    input = json.load(f)

client = ApifyClient(os.getenv("TIKTOK_APIFY_CLIENT_KEY"))

run_input = {
    "postURLs": input,
    "commentsPerPost": 20,
    "maxRepliesPerComment": 0,
}
run = client.actor("BDec00yAmCm1QbMEI").call(run_input=run_input)

json_array = []
for item in client.dataset(run["defaultDatasetId"]).iterate_items():
    json_data = json.dumps(item, ensure_ascii=False)
    json_array.append(json.loads(json_data))

    json_str = json.dumps(json_array, ensure_ascii=False, indent=4)

with open("/home/scrapeops/Axioon/Apify/Results/TikTok/TikTok_Comments.json", "w") as f:
    f.write(json_str)
    
upload_file("/home/scrapeops/Axioon/Apify/Results/TikTok/TikTok_Comments.json", "nightapp", f"Apify/TikTok/Comments/TikTok_Comments_{timestamp}.json")

file_name = requests.post("http://18.231.150.215/webhook/tiktok/comments", json={"records": f"Apify/TikTok/Comments/TikTok_Comments_{timestamp}.json"})
