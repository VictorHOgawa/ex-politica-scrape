# from datetime import date, datetime, timedelta
# from ..items import articleItem
# from scrapy.http import Request
# from urllib.parse import urljoin
# import locale
# import requests
# import scrapy
# import json

# locale.setlocale(locale.LC_TIME, 'pt_BR.UTF-8')

# with open("Spiders/CSS_Selectors/GO/Go_DiarioDaManha.json") as f:
#     search_terms = json.load(f)
    
# now = datetime.now()
# timestamp = datetime.timestamp(now)

# today = date.today().strftime("%d/%m/%Y")
# today = datetime.strptime(today, "%d/%m/%Y")

# search_limit = date.today() - timedelta(days=1)
# search_limit = datetime.strptime(search_limit.strftime("%d/%m/%Y"), "%d/%m/%Y")

# # request = requests.get("http://172.20.10.2:3333/scrape/news/6eb8b551-9a16-4f5f-91c4-9c76a2513d0b")
# # search_words = request.json()
# search_words = {'users': [{'id': '123', 'social_name': 'Roberto Naves'}, {'id': '456', 'social_name': 'Antônio Gomide'}, {'id': '789', 'social_name': 'Márcio Corrêa'}]}

# main_url = "https://www.dm.com.br/ajax/noticiasCategory?offset=0&categoryId=49&amount=10"

# class GoDiarioDaManha(scrapy.Spider):
#     name = "Go_DiarioDaManha"
#     allowed_domains = ["dm.com.br"]
#     start_urls = ["https://www.dm.com.br/ajax/noticiasCategory?offset=0&categoryId=49&amount=20"]
#     custom_settings = {
#         "FEEDS": {
#             f"s3://nightapp/News/GO/{name}_{timestamp}.json": {
#                 "format": "json",
#                 "encoding": "utf8",
#                 "store_empty": False,
#                 "indent": 4,
#             }
#         }
#     }
    
#     def parse(self, response):
#         for article in response.css(search_terms['article']):
#             link = article.css(search_terms['link']).get()
#             yield Request(f"https://dm.com.br{link}", callback=self.parse_article, priority=1)
#         next_page = "https://www.dm.com.br/ajax/noticiasCategory?offset=20&categoryId=49&amount=20"
#         if next_page is not None:
#             yield response.follow(next_page, callback=self.parse)
#         else:
#             print("NÃO TEM NEXT BUTTON")
            
#     def parse_article(self, response):
#         updated = response.css(search_terms['updated'])[-1].get()
#         updated = updated.split(",")[1]
#         updated = updated.replace("de", "").strip()
#         updated = datetime.strptime(updated, "%d  %B  %Y").strftime("%d/%m/%Y")
#         updated = datetime.strptime(updated, "%d/%m/%Y")
#         print("updated: ", updated)
#         title = response.css(search_terms['title']).get()
#         content = response.css(search_terms['content']).getall()
#         if search_limit <= updated <= today:
#             found_names = []
#             for paragraph in content:
#                 for user in search_words['users']:
#                     if user['social_name'] in paragraph:
#                         found_names.append({'name': user['social_name'], 'id': user['id']})
#                         item = articleItem(
#                             updated=updated,
#                             title=title,
#                             content=content,
#                             link=response.url,
#                             users=found_names
#                         )
#                         yield item
#         else:
#             raise scrapy.exceptions.CloseSpider