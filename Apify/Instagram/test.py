# from apify_client import ApifyClient
# from datetime import date, datetime

# import json

# input = [
#     "https://www.instagram.com/p/C0IGezPMZ5X/",
#     "https://www.instagram.com/p/CxBjY-yRo35/",
#     "https://www.instagram.com/p/C2Iwc1XxLWZ/",
#     "https://www.instagram.com/p/CxdYfRmszAb/",
#     "https://www.instagram.com/p/C1FVF-tu-Cr/",
# ]

# with open("Cookies.json") as f:
#     cookies = json.load(f)

# for link in input: 
# # Initialize the ApifyClient with your API token
#     client = ApifyClient("apify_api_DBrvEynIe09EOVyxrNzDeq3k7YFB7V0YYWHc")

#     # Prepare the Actor input
#     run_input = {
#         "action": "scrapeCommentsOfPost",
#         "cookie": cookies,
#         "deepScrape": False,
#         "maxDelay": 15,
#         "minDelay": 5,
#         "proxy": {
#             "useApifyProxy": True,
#             "apifyProxyGroups": [],
#             "apifyProxyCountry": "US"
#         },
#         "scrapeCommentsOfPost.url": link
#     }

#     now = datetime.now()
#     timestamp = datetime.timestamp(now)

#     # Run the Actor and wait for it to finish
#     run = client.actor("l1BtWne1lAWINIpJb").call(run_input=run_input)

#     json_array = []

#     # Fetch and print Actor results from the run's dataset (if there are any)
#     for item in client.dataset(run["defaultDatasetId"]).iterate_items():
#         json_data = json.dumps(item, ensure_ascii=False)
#         json_array.append(json.loads(json_data))
                    
#         json_str = json.dumps(json_array, indent=4, ensure_ascii=False)

#     with open(f"Apify/Results/Instagram/teste_5_links{timestamp}.json", "w") as f:
#         f.write(json_str)
import os

print(os.environ['APIFY_KEY'])