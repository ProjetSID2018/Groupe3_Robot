import os
import lxml.html as lh
import json
import datetime as date
from bs4 import BeautifulSoup
import requests


import g4_futurasciences_v1 as g4_fusc
import g4_liberation_v1 as g4_libe
import g4_lemonde_v1 as g4_lmde

import g4_ladepeche_v1 as g4_lade
import g4_20minutes_v1 as g4_min
import g4_nouvel_obs_v1 as g4_noob

import g4_telerama_v1 as g4_tele
import g4_new_gorafi_v1 as g4_gora
import g4_hum_v1 as g4_huma

import g4_latribune_v1 as g4_latri
import g4_lefigaro_v15 as g4_lefi
import g4_lepoint_v11 as g4_lepo

import g4_scienceetvie_v1 as g4_scev
import g4_femina_v1 as g4_femi
import g4_equipe_v12 as g4_eq


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

activation(g4_fusc.recovery_new_articles_fusc, "Futura Science")

activation(g4_libe.recuperation_info_libe, "Liberation")

activation(g4_lmde.recuperation_info_lmde, "Le Monde")

activation(g4_lade.recovery_new_articles_ld, "La Depeche")

activation(g4_min.add_articles, "20 Minutes")

activation(g4_tele.add_articles, "Telerama")

activation(g4_gora.recovery_new_article_lg, "Le Gorafi")

activation(g4_huma.recovery_new_articles_hum, "Humanite")

activation(g4_noob.recovery_new_articles_noob_rss, "Nouvel Obs")

activation(g4_latri.recuperation_info_lt, "La Tribune")

activation(g4_eq.recovery_new_articles_equipe, "Equipe")

activation(g4_femi.recovery_new_articles_fem, "Femina")

activation(g4_scev.recovery_old_articles_sv, "Science et vie")

activation(g4_lefi.recovery_new_articles_lfi, "Le Figaro")


delta = date.datetime.now() - deb
print(delta.total_seconds())
