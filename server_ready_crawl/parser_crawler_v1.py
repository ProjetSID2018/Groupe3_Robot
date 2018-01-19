# -*- coding: utf-8 -*-
"""
Created on Tue Jan 16 10:02:06 2018
Group 4
@authors: Morgan Seguela, Aurelien PELAT
"""

import sys
import datetime as date
import g4_20minutes_ancien_v1 as crwl_min
# import g4_anciens_articles_equipe as crwl_equi
import g4_anciens_articles_ladepeche_v11 as crwl_depe
import g4_anciens_articles_latribune_V0 as crwl_trib
import g4_crawler_figaro_v12 as crwl_lfi
import g4_crawler_lepoint_v12 as crwl_lpt
import g4_crawler_liberation_v1 as crwl_libe
import g4_telerama_crawl_v1 as crwl_tele
import g4_femina_crawler_function as crwl_fem
import g4_hum_crawler_function as crwl_hum
import g4_lemonde_crawler as crwl_lmde
import g4_noob_crawler_function as crwl_noob
import g4_old_articles_Gorafi_v12 as crwl_gora
import g4_old_futurasciences_v1 as crwl_fusc
import g4_scienceetvie_v1 as crwl_scvie

log_file = open('log.log', 'w')
sys.stdout = log_file

target_file = "/var/www/html/projet2018/data/clean/robot/" + \
    str(date.datetime.now().date()) + "/"

deb = date.datetime.now()

try:
    crwl_min.recovery_old_article_minutes(target_file)
    print('20 Minutes crawler OK')
except:
    print('Erreur crawler 20 Minutes')
"""
try:
    crwl_equi.(target_file)
    print("L Equipe Crawler OK")
except:
    print("Erreur crawler L Equipe")
"""
try:
    crwl_depe.recovery_old_articles_LD(target_file)
    print('La depeche crawler OK')
except:
    print('Erreur crawler La Depeche')

try:
    crwl_trib.recovery_new_articles_lt(target_file)
    print('La Tribune crawler OK')
except:
    print('Erreur crawler ')

try:
    crwl_lfi.recovery_new_articles_lfi(target_file)
    print('Le Figaro crawler OK')
except:
    print('Erreur crawler Le Figaro')

try:
    crwl_lpt.recovery_new_articles_lpt(target_file)
    print('Le Point crawler OK')
except:
    print('Erreur crawler ')

try:
    crwl_libe.recovery_new_articles_libe(target_file)
    print(' crawler OK')
except:
    print('Erreur crawler ')

try:
    crwl_tele.add_articles(target_file)
    print('Telerama crawler OK')
except:
    print('Erreur crawler Telerama')

try:
    crwl_fem.recovery_new_articles_fem(target_file)
    print('Femina crawler OK')
except:
    print('Erreur crawler Femina')

try:
    crwl_hum.recovery_new_articles_hum_crawler(target_file)
    print('Humanite crawler OK')
except:
    print('Erreur crawler Humanite')

try:
    crwl_lmde.recuperation_info_lmde(target_file)
    print('Le Monde crawler OK')
except:
    print('Erreur crawler Le Monde')

try:
    crwl_noob.recovery_new_articles_noob_crawler(target_file)
    print('Nouvel Observateur crawler OK')
except:
    print('Erreur crawler Nouvel Observateur')

try:
    crwl_gora.recovery_old_article_lg(target_file)
    print('Le Gorafi crawler OK')
except:
    print('Erreur Le Gorafi')

try:
    crwl_fusc.recovery_old_articles_fusc(target_file)
    print('Futurama Science crawler OK')
except:
    print('Erreur Futurama Science')

try:
    crwl_scvie.recovery_old_articles_sv(target_file)
    print('Science et vie crawler OK')
except:
    print('ErreurScience et vie')

delta = date.datetime.now() - deb
print(delta.total_seconds())
