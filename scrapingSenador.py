
from bs4 import BeautifulSoup
import requests

url = "http://www.senado.cl/appsenado/index.php?mo=sesionessala&ac=detalleVotacion&votaid=6750"

req = requests.get(url)

status_code = req.status_code

asd = False

if status_code == 200:
	html = BeautifulSoup(req.text, "html.parser")
	entrada = html.find('div',{'class': 'col1'})
	print(entrada.contents[1].contents[0] + entrada.contents[2]  + entrada.contents[4].contents[0] + entrada.contents[5])
	senadores = entrada.find_all('tr')
	for i, senador in enumerate(senadores):
		aux = senador.find_all('td')		
		if(asd):
			if(aux[1].string !=" "):
				print(aux[0].string + " Si")
			elif(aux[2].string != " "):
				print(aux[0].string + " No")
			elif(aux[3].string != " "):
				print(aux[0].string + " Abstención")
			elif(aux[4].string != " "):
				print(aux[0].string + " Pareo")		
		asd = True



		
			
	
		