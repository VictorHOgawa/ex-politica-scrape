from datetime import date, datetime, timedelta
from scrapy.item import Item, Field
from urllib.parse import urljoin
from scrapy.http import Request
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

# request = requests.get("http://192.168.10.10:3333/user/website/21c35dba-7f00-4a71-94bb-ff80952aacbf")
# search_words = request.json()
search_words = {'users': [{'id': 'c57d379e-42d4-4878-89be-f2e7b4d61590', 'social_name': 'Roberto Dorner'}, {'id': '3023f094-6095-448a-96e3-446f0b9f46f2', 'social_name': 'Mauro Mendes'}, {'id': '2b9955f1-0991-4aed-ad78-ea40ee3ce00a', 'social_name': 'Emanuel Pinheiro'}]}

main_url = "https://www.folhamax.com/"

class MtFolhamaxSpider(scrapy.Spider):
    name = "Mt_FolhaMax"
    allowed_domains = ["folhamax.com"]
    start_urls = ["https://www.folhamax.com/includes/__lista_noticias.inc.php?pageNum_Pagina=0&query_string=/politica/&totalRows_Pagina=69728"]
    custom_settings = {
        "FEEDS": {
            f"s3://nightapp/MT/News/{name}_{timestamp}.json": {
                "format": "json",
                "encoding": "utf8",
                "store_empty": False,
                "indent": 4,
            }
        },
        'SCRAPEOPS_API_KEY': '0beda8b5-3c2a-4c06-b838-c29285e22fdb',
        'SCRAPEOPS_FAKE_USER_AGENT_ENABLED': True,
        'DOWNLOADER_MIDDLEWARES': {
            'Spiders.middlewares.ScrapeOpsFakeUserAgentMiddleware': 400,
        }
    }
        
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
            # found_names = []
            # for paragraph in content:
            #     for user in search_words['users']:
            #         if user['social_name'] in paragraph:
            #             found_names.append({'name': user['social_name'], 'id': user['id']})
            #             item = articleItem(
            #                 updated=updated,
            #                 title=title,
            #                 content=content,
            #                 link=response.url,
            #                 users=found_names
            #             )
            #             yield item
            item = articleItem(
                updated=updated,
                title=title,
                content=content,
                link=response.url
            )
            yield item
        else:
            raise scrapy.exceptions.CloseSpider