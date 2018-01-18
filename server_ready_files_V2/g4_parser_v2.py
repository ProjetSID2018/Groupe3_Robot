import os
import lxml.html as lh
import json
import datetime as date
from bs4 import BeautifulSoup
import requests


import g4_20minutes_v1 as min20
import g4_equipe_function_v13 as equipe
import G4_femina_crawler_function as femina
import g4_hum_crawler_function as hum_crawl
import g4_hum_rss_function as hum_rss
import g4_ladepeche_V1 as depeche
import g4_latribune_V1 as tribune
import g4_lefigaro_v15 as figaro
import g4_lepoint_v11 as point
import g4_liberation_V1 as liberation
import g4_noob_crawler_function as noob_crawl
import g4_noob_rss_function as noob_rss
import g4_scienceetvie_v1 as sv
import g4_telerama_v1 as tele


def activation(rss_function, newspaper):
    """active les fonctions de collecte

    Arguments:
        rss_function {func} -- Collecting Function
        newspaper {string} -- Newspaper Name
    """

    target_file = "/var/www/html/projet2018/data/clean/robot/" + \
        str(date.datetime.now().date()) + "/"

    # target_file = "data/clean/robot/" + str(date.datetime.now().date()) +"/"

    try:
        rss_function(target_file)
        print(newspaper + " OK")
    except Exception as exception:
        print(exception)
        print(type(exception).__name__)
        print("Erreur " + newspaper)


deb = date.datetime.now()

activation(liberation.recuperation_info_libe, "Liberation")

activation(depeche.recovery_new_articles_ld, "La Depeche")

activation(min20.add_articles, "20 Minutes")

activation(tele.add_articles, "Telerama")

activation(hum_crawl.recovery_new_articles_hum_crawler, "Humanite")

activation(hum_rss.recovery_new_articles_hum_rss, "Humanite")

activation(noob_crawl.recovery_new_articles_noob_crawler, "Nouvel Obs")

activation(noob_rss.recovery_new_articles_noob_rss, "Nouvel Obs")

activation(tribune.recuperation_info_lt, "La Tribune")

activation(point.recovery_new_articles_lpt, "Le Point")

activation(equipe.recovery_new_articles_equipe, "Equipe")

activation(femina.recovery_new_articles_fem, "Femina")

activation(sv.recovery_old_articles_sv, "Science et vie")

activation(figaro.recovery_new_articles_lfi, "Le Figaro")


delta = date.datetime.now() - deb
print(delta.total_seconds())
