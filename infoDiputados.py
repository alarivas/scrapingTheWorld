from bs4 import BeautifulSoup
import requests
import re 
import psycopg2

url = "https://www.camara.cl/camara/diputados.aspx"

req = requests.get(url)
status = req.status_code
conn = psycopg2.connect("dbname= user= password= host=152.74.52.213 port=5432")
cursor = conn.cursor()

if status == 200:
	html = BeautifulSoup(req.text, "html.parser")
	diputados = html.find_all('li', {'class':'alturaDiputado'})
	for i in range(0,120):
		nombres = diputados[i].contents[3].contents[1].getText()
		nombres = nombres.replace("Sr.", "")
		nombres = nombres.replace("Sra.","")
		nombres = nombres.strip()
		region = diputados[i].contents[5].contents[1].string.split()
		distrito = diputados[i].contents[5].contents[3].string.split()
		distrito_final = distrito[1].replace("N°", "")
		partido = diputados[i].contents[5].contents[5].string.split()
		query1 = "INSERT INTO app_schema.congresista (nombre, partido) VALUES (%s, %s);"
		data1 = (nombres, partido[1])
		cursor.execute(query1, data1)
		query2 = "INSERT INTO app_schema.diputado (nombre, distrito) VALUES (%s, %s);"
		data2 = (nombres, distrito_final)
		cursor.execute(query2, data2)
		#print("Nombre: " + nombres + '\n' + "Región: " + region[1] + '\n' + "Distrito: " + distrito_final + '\n' + "Partido: " + partido[1])
		#print('\n')
	conn.commit()