from bs4 import BeautifulSoup
import requests
import re
import psycopg2

def createTimeStamp(fecha):
	aux = fecha.split()
	day = aux[0].strip()
	month = aux[2].strip()
	year = aux[4].strip()
	time = aux[5].strip()
	month = monthToNumber(month)
	day = fixDay(day)
	fecha = year + "-" + month + "-" + day + " " + time
	return fecha

def monthToNumber(month):
	if month.lower() == "ene":
		month = "01"
	elif month.lower() == "feb":
		month = "02"
	elif month.lower() == "mar":
		month = "03"
	elif month.lower() == "abr":
		month = "04"
	elif month.lower() == "may":
		month = "05"
	elif month.lower() == "jun":
		month = "06"
	elif month.lower() == "jul":
		month = "07"
	elif month.lower() == "ago":
		month = "08"
	elif month.lower() == "sep":
		month = "09"
	elif month.lower() == "oct":
		month = "10"
	elif month.lower() == "nov":
		month = "11"
	elif month.lower() == "dic":
		month = "12"
	return month

def fixDay(day):
	if len(day) < 2:
		day = "0" + day 
	return day

def fixName(name):
	aux = re.split(', ', name)
	name = aux[1] + " " + aux[0]
	name = re.split(' ', name)
	if len(name) == 4:
		name = name[0] + " " + name[1] + " " + name[2]
	elif len(name) == 3:
		name = name[0] + " " + name[1]
	return name


if __name__ == '__main__':
	

	#conn = psycopg2.connect("dbname= user= password= host=152.74.52.213 port=5432")
	#cursor = conn.cursor()
	#25358 25845
	for i in range(25498, 25499):
		url = "https://www.camara.cl/trabajamos/sala_votacion_detalle.aspx?prmID=" + str(i)
		req = requests.get(url)
		status_code = req.status_code

				

		if status_code == 200:
			html = BeautifulSoup(req.text, "html.parser")
			entrada = html.find('div',{'class': 'stress'})
			
			"""try:
				if entrada.contents[5].contents[1].string.strip() != "Sesión:":
					fecha = createTimeStamp(entrada.contents[3].contents[2].string.replace("hrs.", "").strip())
					tema = entrada.contents[5].contents[2].string.strip()
					articulo = entrada.contents[7].contents[2].string.strip()
					print("Fecha: " + fecha + '\n' + "Tema: " + tema + '\n' + "Art: " + articulo + '\n' + str(i))

			except AttributeError:
				pass"""

			aFavor = html.find('table',{'id': 'ctl00_mainPlaceHolder_dtlAFavor'})
			print("Diputados a favor: " + '\n')
			for diputado in aFavor.find_all('a'):
				print(fixName(diputado.contents[0].string.strip()))
			print('\n')

			enContra = html.find('table',{'id': 'ctl00_mainPlaceHolder_dtlEncontra'})
			print("Diputados en contra: " + '\n')
			for diputado in enContra.find_all('a'):
				print(fixName(diputado.contents[0].string.strip()))
			print('\n')

			abstencion = html.find('table',{'id': 'ctl00_mainPlaceHolder_dtlAbstencion'})
			print("Diputados abstención: " + '\n')
			for diputado in abstencion.find_all('a'):
				print(fixName(diputado.contents[0].string.strip()))
			print('\n')

			art5 = html.find('table',{'id': 'ctl00_mainPlaceHolder_dtlArt5'})
			print("Diputados art5: " + '\n')
			for diputado in art5.find_all('a'):
				print(fixName(diputado.contents[0].string.strip()))		
			print('\n')

			pareo = html.find('table',{'id': 'ctl00_mainPlaceHolder_dtlPareos'})
			print("Diputados pareo: " + '\n')
			for diputado in pareo.find_all('a'):
				print(fixName(diputado.contents[0].string.strip()))
			