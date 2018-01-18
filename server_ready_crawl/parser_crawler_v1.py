# -*- coding: utf-8 -*-
"""
Created on Tue Jan 16 10:02:06 2018

@author: Aurelien PELAT
"""

import datetime as date
import g4_crawler_lepoint_v12 as lepoint
import g4_crawler_figaro_v12 as lefigaro

target_file = "/var/www/html/projet2018/data/clean/robot/" + str(date.datetime.now().date()) +"/"

deb = date.datetime.now()

try:
    lepoint.recovery_new_articles_lpt(target_file)
    print("Le Point Crawler OK")
except:
    print("Erreur Le Point")

try:
    lefigaro.recovery_new_articles_lfi(target_file)
    print("Le Figaro Crawler OK")
except:
    print("Erreur Le Figaro")

delta = date.datetime.now() - deb
print(delta.total_seconds())
