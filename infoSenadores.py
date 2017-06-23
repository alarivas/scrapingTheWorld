from bs4 import BeautifulSoup
import requests
import re

url = "http://www.senado.cl/appsenado/index.php?mo=senadores&ac=listado"

req = requests.get(url)

status_code = req.status_code

if status_code == 200:
	html = BeautifulSoup(req.text, "html.parser")
	#entrada = html.find('section',{'class':'seccion2 sans'})
	senadores = html.find_all('tr')
	partido = html.find_all('td')
	for i in range(2,39*2,2):
		aux = senadores[i].contents[3].contents[5].contents[0].string
		tmp= re.split(' |', aux)

		nombre = senadores[i].contents[3].contents[1].contents[0].getText()
		region =senadores[i].contents[3].contents[3].contents[1].getText().strip()
		circunscripcion = senadores[i].contents[3].contents[3].contents[3].getText()
		telefono = tmp[1]+tmp[2]
		mail = senadores[i].contents[3].contents[5].contents[1].getText()
		part = re.split(' ',partido[2*i - 1].getText())
		print("Nombre: " + nombre) 
		print("Región: " + region + '\n'+"Circunscripción: "+circunscripcion)
		print("Teléfono: " + telefono)
		print("email: " + mail)
		print("Partido: " + part[1] + '\n')
		