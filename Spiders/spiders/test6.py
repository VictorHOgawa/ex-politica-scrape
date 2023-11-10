import requests
from requests_html import HTML

source = requests.get('https://www.cenariomt.com.br/cenario-politico/')
html = HTML(html=source.text)
print(source.status_code)
print(html.text)