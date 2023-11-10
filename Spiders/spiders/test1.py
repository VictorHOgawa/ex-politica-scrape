import requests
from requests_html import HTML

source = requests.get('https://sonoticias.com.br/politica-listagem')
html = HTML(html=source.text)
print(source.status_code)
print(html.text)