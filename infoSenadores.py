from bs4 import BeautifulSoup
import requests
import re
import psycopg2


url = "http://www.senado.cl/appsenado/index.php?mo=senadores&ac=listado"

req = requests.get(url)

status_code = req.status_code
conn = psycopg2.connect("dbname=app user=app password=necesitovida host=152.74.52.213 port=5432")
cursor = conn.cursor()



if status_code == 200:
	html = BeautifulSoup(req.text, "html.parser")
	#entrada = html.find('section',{'class':'seccion2 sans'})
	senadores = html.find_all('tr')
	partido = html.find_all('td')
	for i in range(2,39*2,2):
		aux = senadores[i].contents[3].contents[5].contents[0].string
		tmp= re.split(' |', aux)

		nombre = senadores[i].contents[3].contents[1].contents[0].getText()
		nombre_aux = re.split(',', nombre)
		nombre_final = nombre_aux[1].strip() + ' ' + nombre_aux[0].strip()
		region =senadores[i].contents[3].contents[3].contents[1].getText().strip()
		circunscripcion = senadores[i].contents[3].contents[3].contents[3].getText()
		telefono = tmp[1]+tmp[2]
		mail = senadores[i].contents[3].contents[5].contents[1].getText()
		part = re.split(' ',partido[2*i - 1].getText())
		partido_final = part[1].replace(".", "")
		query1 = "INSERT INTO app_schema.congresista (nombre, partido) VALUES (%s, %s);"
		data1 = (nombre_final, partido_final)
		cursor.execute(query1, data1)
		query2 =  "INSERT INTO app_schema.senador (nombre, email, telefono, circunscripcion) VALUES (%s, %s, %s, %s);"
		data2 = (nombre_final, mail, telefono, circunscripcion)
		cursor.execute(query2, data2)

	conn.commit()	