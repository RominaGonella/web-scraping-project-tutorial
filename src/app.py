# instalo librerias que no están por defecto
#pip install pandas

# importo librerias
import pandas as pd
import sqlite3
import requests
from bs4 import BeautifulSoup

# datos
r = requests.get('https://www.macrotrends.net/stocks/charts/TSLA/tesla/revenue')
html_data = r.text
print(type(html_data))

# busco la tabla que interesa
data = BeautifulSoup(html_data, 'html.parser')
tablas = data.findAll('table')
id_tabla = None
for i in range(len(tablas)):
    if "Tesla Quarterly Revenue" in str(tablas[i]):
        id_tabla = i
        print("la tabla que busco está en el índice ", str(id_tabla))
        break
tabla = tablas[id_tabla]
lista = tabla.tbody.find_all('tr')

# creo data frame
tesla_revenue = pd.DataFrame(columns=["Date", "Revenue"])
for fila in lista:
    col = fila.find_all("td")
    if (col != []):
        Date = col[0].text
        Revenue = col[1].text.replace("$", "").replace(",", "")
        tesla_revenue = tesla_revenue.append({"Date":Date, "Revenue":Revenue}, ignore_index=True)
print(tesla_revenue)
print(f'cantidad de filas = {len(tesla_revenue)}')

# saco filas vacías en Revenue
tesla_revenue = tesla_revenue[tesla_revenue['Revenue'] != '']
print(tesla_revenue)
print(f'cantidad de filas = {len(tesla_revenue)}')

# chequeo que no hayan NaN ni vacíos
print(tesla_revenue.Revenue.unique())
print(tesla_revenue.Date.unique())

# armo lista para la DB
lista = list(tesla_revenue.to_records(index=False))
lista

# creo DB
connection = sqlite3.connect('Tesla.db')
c = connection.cursor()

# creo tabla y agrego datos
c.execute('CREATE TABLE IF NOT EXISTS revenue (Date, Revenue)')
c.executemany('INSERT INTO revenue VALUES (?,?)', lista)
# guardo cambios en DB
connection.commit()

# verifico si quedó bien al traer datos de DB
query = c.execute('SELECT * FROM revenue')
for row in query:
    print(row)