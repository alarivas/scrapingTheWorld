
from bs4 import BeautifulSoup
import requests
import re
import psycopg2


def createTimeStamp(fecha):
	aux = fecha.split()
	day = aux[4].strip()
	month = aux[6].strip()
	year = aux[8].strip()
	time = aux[11].strip()
	month = monthToNumber(month)
	day = fixDay(day)
	fecha = year + "-" + month + "-" + day + " " + time
	return fecha

def monthToNumber(month):
	if month.lower() == "enero":
		month = "01"
	elif month.lower() == "febrero":
		month = "02"
	elif month.lower() == "marzo":
		month = "03"
	elif month.lower() == "abril":
		month = "04"
	elif month.lower() == "mayo":
		month = "05"
	elif month.lower() == "junio":
		month = "06"
	elif month.lower() == "julio":
		month = "07"
	elif month.lower() == "agosto":
		month = "08"
	elif month.lower() == "septiembre":
		month = "09"
	elif month.lower() == "octubre":
		month = "10"
	elif month.lower() == "noviembre":
		month = "11"
	elif month.lower() == "diciembre":
		month = "12"
	return month

def fixDay(day):
	if len(day) < 2:
		day = "0" + day 
	return day

def fixName(name):
	aux = re.split(', ', name)
	name = aux[1] + " " + aux[0]
	return name


if __name__ == '__main__':

	conn = psycopg2.connect("dbname= user= password= host=152.74.52.213 port=5432")
	cursor = conn.cursor()
	for i in range (6680, 6774):
		url = "http://www.senado.cl/appsenado/index.php?mo=sesionessala&ac=detalleVotacion&votaid=" + str(i)
		req = requests.get(url)
		status_code = req.status_code

		

		asd = False

		if status_code == 200:
			html = BeautifulSoup(req.text, "html.parser")
			entrada = html.find('div',{'class': 'col1'})
			fecha = createTimeStamp(entrada.contents[2])
			tema = entrada.contents[5].strip()

			#query1 = "INSERT INTO app_schema.votacion (fecha_hora, tema) VALUES (%s, %s);"
			#data1 = (fecha, tema)
			#cursor.execute(query1, data1)
			senadores = entrada.find_all('tr')
			for i, senador in enumerate(senadores):
				aux = senador.find_all('td')
				voto = ""		
				
				if(asd):
					nombre = fixName(aux[0].string)
					if(aux[1].string !=" "):
						voto = "Si"
					elif(aux[2].string != " "):
						voto = "No"
					elif(aux[3].string != " "):
						voto = "Abstención"
					elif(aux[4].string != " "):
						voto = "Pareo"		
					query2 = "INSERT INTO app_schema.voto (fecha_hora, nombre_congresista, voto) VALUES (%s, %s, %s);"
					data2 = (fecha, nombre, voto)
					cursor.execute(query2, data2)
				asd = True
			conn.commit()
		

		