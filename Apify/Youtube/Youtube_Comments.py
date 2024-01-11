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

with open("/home/scrapeops/Axioon/Apify/Results/Youtube/Youtube_Videos_Urls.json", "r") as f:
    input = json.load(f)

input = [{"url": url} for url in input]

client = ApifyClient(os.getenv("YOUTUBE_APIFY_CLIENT_KEY"))

run_input = {
    "maxComments": 20,
    "startUrls": input
}

run = client.actor("p7UMdpQnjKmmpR21D").call(run_input=run_input)

json_array = []
for item in client.dataset(run["defaultDatasetId"]).iterate_items():
    json_data = json.dumps(item, ensure_ascii=False)
    json_array.append(json.loads(json_data))
                
    json_str = json.dumps(json_array, indent=4, ensure_ascii=False)

with open("/home/scrapeops/Axioon/Apify/Results/Youtube/Youtube_Comments.json", "w") as f:
    f.write(json_str)
    
upload_file("/home/scrapeops/Axioon/Apify/Results/Youtube/Youtube_Comments.json", "nightapp", f"Apify/YouTube/Comments/YouTube_Comments_{timestamp}.json")

file_name = requests.post("http://18.231.150.215/webhook/youtube/comments", json={"records": f"Apify/YouTube/Comments/YouTube_Comments_{timestamp}.json"})
