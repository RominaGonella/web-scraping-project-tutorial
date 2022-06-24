# your librerias
import pandas as pd
import sqlite3
import requests
from bs4 import BeautifulSoup

# datos
r = requests.get('https://www.macrotrends.net/stocks/charts/TSLA/tesla/revenue')
#html_data = r.json()
html_data = r.text
print(html_data)

# limpio
data = BeautifulSoup(html_data, 'html.parser')
data2 = data.prettify()
print(data2)