"""
@author Morgan Seguela
V1 : Tout les journaux
"""
import datetime as date

import g4_futurasciences_v1 as g4_fusc
import g4_liberation_V1 as g4_libe
import g4_lemonde_V1 as g4_lmde
import g4_20minutes_v1 as g4_min
import g4_nouvel_obs_V1 as g4_noob
import g4_telerama_v1 as g4_tele
import g4_new_gorafi_v1 as g4_gora
import g4_nouveaux_articles_hum as g4_huma
import g4_latribune_V1 as g4_latri
import g4_ladepeche_V1 as g4_lade
import g4_lepoint_v11 as g4_lepo
import g4_lefigaro_v15 as g4_lefi


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


DEB = date.datetime.now()

activation(g4_fusc.recovery_new_articles_fusc, "Futura Science")

activation(g4_libe.recuperation_info_libe, "Liberation")

activation(g4_lmde.recuperation_info_lmde, "Le Monde")

activation(g4_lade.recovery_new_articles_ld, "La Depeche")

activation(g4_min.add_articles, "20 Minutes")

activation(g4_tele.add_articles, "Telerama")

activation(g4_gora.recovery_new_article_lg, "Le Gorafi")

activation(g4_huma.recovery_new_articles_hum, "Humanite")

activation(g4_noob.recovery_new_articles_noob, "Nouvel Obs")

activation(g4_latri.recuperation_info_lt, "La Tribune")

activation(g4_lepo.recovery_new_articles_lpt, "Le Point")

activation(g4_lefi.recovery_new_articles_lfi, "Le Figaro")

DELTA = date.datetime.now() - DEB
print(DELTA.total_seconds())
