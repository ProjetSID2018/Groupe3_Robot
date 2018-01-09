import os
import lxml.html as lh
import json
import datetime as date
from bs4 import BeautifulSoup
import requests
import re

url_rss_gorafi = "http://www.20minutes.fr/feeds/rss-actu-france.xml"


req = requests.get(url_rss_gorafi)
data = req.text
print('ok')

soup = BeautifulSoup(data, "lxml")

items = soup.find_all("item")
for item in items:
    print(re.search(r"<link/>(.*)<pubdate>", str(item))[1])

