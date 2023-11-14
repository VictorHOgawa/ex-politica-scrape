# from selenium import webdriver
# from selenium.webdriver.common.keys import Keys
# from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
# from time import sleep
# import re
# from selenium.webdriver.chrome.options import Options as ChromeOptions

# options = webdriver.ChromeOptions()
# options.add_argument("--headless")
# options.add_argument("--no-sandbox")
# driver = webdriver.Chrome(options=options)

# driver = webdriver.Chrome("/usr/bin/google-chrome-stable")  
# driver.get("https://www.jornalopcao.com.br/categoria/politica/?pg=1")

# page_source = driver.page_source

# soup = BeautifulSoup(page_source)

# article = soup.find("div", class_="template-part-component-feed-item")

# article_link = article.find("a", class_="main_link").get("href")

# print("article_link: ", article_link)

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.proxy import *

options = Options()
options.add_argument('--headless')
options.add_argument('--no-sandbox')
options.add_argument('--disable-dev-shm-usage')


myProxy = "https://dripcrawler.p.rapidapi.com/"
proxy = Proxy({
    'proxyType': ProxyType.MANUAL,
    'httpProxy': myProxy,
    'sslProxy': myProxy,
    'noProxy': ''})

options = Options()
options.proxy = proxy
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
 
driver.get("https://www.folhamax.com/includes/__lista_noticias.inc.php?pageNum_Pagina=0&query_string=/politica/&totalRows_Pagina=69728")

page_source = driver.page_source

soup = BeautifulSoup(page_source)

print(soup.prettify())

# article = soup.find("div", class_="template-part-component-feed-item")

# article_link = article.find("a", class_="main_link").get("href")

# print("article_link: ", article_link)