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

with open("/home/scrapeops/Axioon/Apify/Results/Facebook/Facebook_Posts_Urls.json", "r") as f:
    input = json.load(f)

input = [{"url": url} for url in input]

client = ApifyClient(os.getenv("FACEBOOK_APIFY_CLIENT_KEY"))

run_input = {
    "includeNestedComments": False,
    "resultsLimit": 20,
    "startUrls": input
}

run = client.actor("us5srxAYnsrkgUv2v").call(run_input=run_input)

json_array = []
for item in client.dataset(run["defaultDatasetId"]).iterate_items():
    json_data = json.dumps(item, ensure_ascii=False)
    json_array.append(json.loads(json_data))
    
    json_str = json.dumps(json_array, indent=4, ensure_ascii=False)
    
with open("/home/scrapeops/Axioon/Apify/Results/Facebook/Facebook_Comments.json", "w") as f:
    f.write(json_str)
    
upload_file(f"/home/scrapeops/Axioon/Apify/Results/Facebook/Facebook_Comments.json", "nightapp", f"Apify/Facebook/Comments/Facebook_Comments_{timestamp}.json")

file_name = requests.post("http://18.231.150.215/webhook/facebook/comments", json={"records": f"Apify/Facebook/Comments/Facebook_Comments_{timestamp}.json"})
