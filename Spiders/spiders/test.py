import requests

s = requests.Session()
r = s.get('https://www.folhamax.com/includes/__lista_noticias.inc.php?pageNum_Pagina=0&query_string=/politica/&totalRows_Pagina=69728',verify=False)
r = s.post('https://www.folhamax.com/includes/__lista_noticias.inc.php?pageNum_Pagina=0&query_string=/politica/&totalRows_Pagina=69728', auth=('user', 'pass'),verify=False)
print(r.status_code)
print(r.text)