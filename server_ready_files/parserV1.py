import os
import lxml.html as lh
import json
import datetime as date
from bs4 import BeautifulSoup
import requests
import g4_futurasciences_v1 as g4_fusc
import g4_liberation_V1 as g4_libe
import g4_lemonde_V1 as g4_lmde

target_file = "/var/www/html/projet2018/data/clean/robot/" + str(date.datetime.now().date()) +"/"

deb = date.datetime.now()
g4_fusc.recovery_new_articles_fusc(target_file)
g4_libe.recuperation_info_libe(target_file)
g4_lmde.recuperation_info_lmde(target_file)

delta = date.datetime.now() - deb
print(delta.total_seconds())
