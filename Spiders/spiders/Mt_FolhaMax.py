from datetime import date, datetime, timedelta
from scrapy.item import Item, Field
from urllib.parse import urljoin
from scrapy.http import Request
from random import randint
import urllib
import requests
import locale
import scrapy
import json

class articleItem(Item):
    title = Field()
    updated = Field()
    content = Field()
    link = Field()
    users = Field()

locale.setlocale(locale.LC_TIME, 'pt_BR.UTF-8')

with open("/home/scrapeops/Axioon/Spiders/CSS_Selectors/MT/Mt_FolhaMax.json") as f:
    search_terms = json.load(f)
    
now = datetime.now()
timestamp = datetime.timestamp(now)

today = date.today().strftime("%d/%m/%Y")
today = datetime.strptime(today, "%d/%m/%Y")

search_limit = date.today() - timedelta(days=1)
search_limit = datetime.strptime(search_limit.strftime("%d/%m/%Y"), "%d/%m/%Y")

# request = requests.get("http://192.168.0.224/scrape/news/1ee1046b-1fe7-4308-92ae-121e524082ea")
# search_words = request.json()
search_words = {'users': [{'id': 'c57d379e-42d4-4878-89be-f2e7b4d61590', 'social_name': 'Roberto Dorner'}, {'id': '3023f094-6095-448a-96e3-446f0b9f46f2', 'social_name': 'Mauro Mendes'}, {'id': '2b9955f1-0991-4aed-ad78-ea40ee3ce00a', 'social_name': 'Emanuel Pinheiro'}]}

main_url = "https://www.folhamax.com/"

# 
# 

url = "https://dripcrawler.p.rapidapi.com/"

payload = {
	"url": "https://www.folhamax.com/includes/__lista_noticias.inc.php?pageNum_Pagina=0&query_string=/politica/&totalRows_Pagina=69728",
	"javascript_rendering": "False"
}
headers = {
	"content-type": "application/json",
	"X-RapidAPI-Key": "941a69a26dmshfef948a2824884cp1b23eajsn68e4d5b09e8b",
	"X-RapidAPI-Host": "dripcrawler.p.rapidapi.com"
}

# 
# 

class MtFolhamaxSpider(scrapy.Spider):
    name = "Mt_FolhaMax"
    allowed_domains = ["folhamax.com"]
    start_urls = ["https://www.folhamax.com/includes/__lista_noticias.inc.php?pageNum_Pagina=0&query_string=/politica/&totalRows_Pagina=69728"]
    custom_settings = {
        "FEEDS": {
            f"s3://nightapp/News/MT/{name}_{timestamp}.json": {
                "format": "json",
                "encoding": "utf8",
                "store_empty": False,
                "indent": 4,
            }
        },
    }

    def start_requests(self):
        yield Request(self.start_urls[0], callback=self.parse, headers=headers)

    def parse(self, response):
        for article in response.css(search_terms['article']):
            link = article.css(search_terms['link']).get()
            yield Request(link, callback=self.parse_article, priority=1)
        next_page = response.css(search_terms['next_page']).get()
        next_page = urljoin(main_url, next_page)
        if next_page is not None:
            yield response.follow(next_page, callback=self.parse)
        else:
            print("NÃO TEM NEXT BUTTON")
            
    def parse_article(self, response):
        updated = response.css(search_terms['updated']).get()
        updated = updated.split(",")[1].strip()
        updated = updated.replace("de", "").strip()
        updated = datetime.strptime(updated, "%d  %B  %Y").strftime("%d/%m/%Y")
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