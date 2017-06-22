from bs4 import BeautifulSoup
import requests

url = "http://www.senado.cl/appsenado/index.php?mo=senadores&ac=listado"

req = requests.get(url)

status_code = req.status_code

if status_code == 200:
	html = BeautifulSoup(req.text, "html.parser")
	#entrada = html.find('section',{'class':'seccion2 sans'})
	senadores = html.find_all('tr')
	partido = html.find_all('td')
	for i in range(2,39*2,2):
		print("Nombre: " + senadores[i].contents[3].contents[1].contents[0].getText()) 
		print("Región: " + senadores[i].contents[3].contents[3].contents[1].getText().strip()+ '\n'+"Circunscripción: "+senadores[i].contents[3].contents[3].contents[3].getText())
		print(senadores[i].contents[3].contents[5].contents[0].string  + senadores[i].contents[3].contents[5].contents[1].getText())
		print(partido[2*i - 1].getText()+'\n')