import os
import lxml.html as lh
import json
import datetime as date
from bs4 import BeautifulSoup
import requests
import re

url_rss_gorafi = "http://www.legorafi.fr/feed/"


req = requests.get(url_rss_gorafi)
data = req.text
print('ok')

soup = BeautifulSoup(data, "lxml")

items = soup.find_all("item")
for item in items:
    print(re.search(r"<link/>(.*)", str(item))[1])

