import requests
from requests_html import HTML

source = requests.get('https://www.olhardireto.com.br/noticias/index.asp?id=33&editoria=politica-mt&pagina=1')
html = HTML(html=source.text)
print(source.status_code)
print(html.text)