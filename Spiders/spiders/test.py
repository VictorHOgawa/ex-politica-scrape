from bs4 import BeautifulSoup
import requests
import json

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

response = requests.post(url, json=payload, headers=headers)

html = response.json()['extracted_html']

bs = BeautifulSoup(html, 'html.parser')

article_banner = bs.find_all("a", {"class": "w-100"})

links = []

for link in article_banner:
	links.append(link['href'])

print(links)