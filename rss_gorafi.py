import os
import lxml.html as lh
import json
import datetime as date
from bs4 import BeautifulSoup
import requests

url_rss_gorafi = "http://www.legorafi.fr/feed/"

req = requests.get(url_rss_gorafi)
data = req.text

soup = BeautifulSoup(data)

items = soup.find_all("item")
print(items)


