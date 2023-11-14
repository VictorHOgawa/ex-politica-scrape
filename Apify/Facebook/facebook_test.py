import json

with open("/home/scrapeops/Axioon/Spiders/CSS_Selectors/MT/Mt_CenarioMt.json") as f:
    data = json.load(f)

print("data: ", data)

with open("/home/scrapeops/Axioon/Apify/Facebook/Facebook_Page.json", "w") as f:
    json.dump(data, f)