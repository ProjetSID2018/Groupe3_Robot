import os
import lxml.html as lh
import json
import datetime as date
from bs4 import BeautifulSoup
import requests
import re

fileTarget = "C:/Users/deloe/Desktop/Travail_ecole/M1_SID/Projet_inter_promo/"

article = "http://www.legorafi.fr/2018/01/03/un-mec-qui-chantait-la-la-la-sous-la-douche-accuse-gregoire-de-plagiat/"

req = requests.get(article)
data = req.text

soup = BeautifulSoup(data, "lxml")
prettyHTML = soup.prettify()

#print(prettyHTML)

sources = "LeGorafi/"
cur_date = date.datetime.now().date()

balise_title = soup.title.string
sep = balise_title.split("—")
titre = sep[0]
journal = sep[1]

for span in soup.find_all('span'):
    if span.get("class") == ['context']:
        auteur = span.a.string
        for valeur in re.finditer('[0-9]{2}\/[0-9]{2}\/[0-9]{4}', str(span)):
            date = valeur.group(0)

contenu = ""            
for div in soup.find_all('div'):
    if div.get("class") == ['content']:
        for p in div.find_all('p'):
           contenu += p.get_text() + " "


data = [{
    "title" : titre,
    "newspaper" : journal,
    "author" : auteur,
    "date_publi" : date,
    "content" : contenu
}]
    
print(data)