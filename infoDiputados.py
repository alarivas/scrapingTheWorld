from bs4 import BeautifulSoup
import requests
import re 

url = "https://www.camara.cl/camara/diputados.aspx"

req = requests.get(url)
status = req.status_code

if status == 200:
	html = BeautifulSoup(req.text, "html.parser")
	diputados = html.find_all('li', {'class':'alturaDiputado'})
	for i in range(0,120):
		nombres = diputados[i].contents[3].contents[1].getText().split()
		nombre = nombres[1] + " " + nombres[2]
		region = diputados[i].contents[5].contents[1].string.split()
		distrito = diputados[i].contents[5].contents[3].string.split()
		partido = diputados[i].contents[5].contents[5].string.split()
		print("Nombre: " + nombre + '\n' + "Región: " + region[1] + '\n' + "Distrito: " + distrito[1] + '\n' + "Partido: " + partido[1])
		print('\n')