from datetime import date, datetime, timedelta
from scrapy.item import Item, Field
from scrapy.http import Request
import requests
import scrapy
import json
import re

class articleItem(Item):
    title = Field()
    updated = Field()
    content = Field()
    link = Field()
    users = Field()

with open("/home/scrapeops/Axioon/Spiders/CSS_Selectors/MT/Mt_CenarioMt.json") as f:
    search_terms = json.load(f)

now = datetime.now()
timestamp = datetime.timestamp(now)

today = date.today().strftime("%d/%m/%Y")
today = datetime.strptime(today, "%d/%m/%Y")

# days=150 => last 10 days
search_limit = date.today() - timedelta(days=1)
search_limit = datetime.strptime(search_limit.strftime("%d/%m/%Y"), "%d/%m/%Y")

request = requests.get("http://172.30.32.1:3333/user/website/1a6efd0a-a1f8-4bdb-86ab-7e7dc68cc9f4")
search_words = request.json()
# search_words = {'users': [{'id': 'c57d379e-42d4-4878-89be-f2e7b4d61590', 'social_name': 'Roberto Dorner'}, {'id': '3023f094-6095-448a-96e3-446f0b9f46f2', 'social_name': 'Mauro Mendes'}, {'id': '2b9955f1-0991-4aed-ad78-ea40ee3ce00a', 'social_name': 'Emanuel Pinheiro'}]}

class MtCenariomtSpider(scrapy.Spider):
    name = "Mt_CenarioMt"
    allowed_domains = ["cenariomt.com.br"]
    start_urls = ["https://www.cenariomt.com.br/cenario-politico/"]
    custom_settings = { 
    "FEEDS": {
        f"s3://nightapp/News/MT/{name}_{timestamp}.json": {
            "format": "json",
            "encoding": "utf8",
            "store_empty": False,
            "indent": 4,
        }
    }
} 
    def parse(self, response):
        for article in response.css(search_terms['article']):
            link = article.css(search_terms['link']).get()
            yield Request(link, callback=self.parse_article, priority=1)
        next_page = response.css(search_terms['next_page'])[-1].get()
        if next_page is not None:
            yield response.follow(next_page, callback=self.parse)
        else:
            print("NÃO TEM NEXT BUTTON")
            
    def parse_article(self, response):
        updated = response.css(search_terms['updated']).get()
        updated = re.search(r"\d{2}/\d{2}/\d{4}", updated).group()
        updated = datetime.strptime(updated, "%d/%m/%Y")
        title = response.css(search_terms['title']).get()
        content = response.css(search_terms['content']).getall()
        if search_limit <= updated <= today:
            found_names = []
            for paragraph in content:
                for user in search_words['users']:
                    if user['social_name'] in paragraph:
                        found_names.append({'name': user['social_name'], 'id': user['id']})
                        item = articleItem(
                            updated=updated,
                            title=title,
                            content=content,
                            link=response.url,
                            users=found_names
                        )
                        yield item
        else:
            raise scrapy.exceptions.CloseSpider
        