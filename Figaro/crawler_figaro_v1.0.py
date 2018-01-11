#Authors : Noemie DELOEUVRE, Morgan SEGUELA, Aurelien PELAT
#Version : 1.0

from bs4 import BeautifulSoup
import requests
import re
import g4_utils_v31 as utils

file_target = "C:/Users/aurel/Documents/Etudes/ProjetIPJournaux/"

url_Figaro = "http://www.lefigaro.fr/"

req = requests.get(url_Figaro)
data = req.text
soup = BeautifulSoup(data, "lxml")

links_themes = []
for a in soup.find_all("a"):
    if (a.get("class") == ['figh-keyword__link']
    and "http://www.lefigaro.fr/" in a.get('href')
    and "http://www.lefigaro.fr/" != a.get('href')): 
            links_themes.append(a.get('href'))

numero_article = 1
for link_theme in links_themes:
    print(numero_article)
    theme = re.search("http://www.lefigaro.fr/(.*)", link_theme)[1]
    theme = re.sub("/", "", theme)
    print("---------------------------------"+theme+"--------------------------------")
    
    
    req = requests.get(link_theme)
    data = req.text
    soup = BeautifulSoup(data, "lxml")
    
    links_sous_themes = []
    for a in soup.find_all("a"):
        if (a.get("class") == ['figh-keyword__link']
        and "http://www.lefigaro.fr/" in a.get('href')):
            links_sous_themes.append(a.get('href'))
    
    for link_sous_theme in links_sous_themes:
        
        print("~~~~~~~"+link_sous_theme+"~~~~~~~~")
        
        req = requests.get(link_sous_theme)
        data = req.text
        soup = BeautifulSoup(data, "lxml")

        items = soup.find_all("item")
        articles_figaro = []
        for h2 in soup.find_all('h2'):
            if (h2.get('class') == ['fig-profile__headline']
            or h2.get('class') == ['fig-profile-headline']):
                articles_figaro.append(h2.a.get('href'))
        
        fichier_json=[]
        for article in articles_figaro:
            req = requests.get(article)
            data = req.text
        
            soup = BeautifulSoup(data, "lxml")
        
            titre = soup.title.string
            print(titre)
               
            auteur = []
            
            for a in soup.find_all('a'):
                if a.get("class") == ['fig-content-metas__author']:
                    auteur.append(re.sub("\s\s+", "", a.get_text()))
            
            date_publi = ""
            
            for time in soup.find_all('time'):
                for valeur in re.finditer('[0-9]{2}\/[0-9]{2}\/[0-9]{4}', str(time)):
                    date_p = valeur.group(0)
            
            contenu = ""
            
            for p in soup.find_all('p'):
                if p.get("class") == ['fig-content__chapo']:
                    contenu = p.get_text() + " "
                    
            for div in soup.find_all('div'):
                if div.get("class") == ['fig-content__body']:
                    for p in div.find_all('p'):
                        contenu += p.get_text() + " "
            
            new_article = {
                    "title" : titre,
                    "newspaper" : 'Le Figaro.fr',
                    "author" : auteur,
                    "date_publi" : date_p,
                    "content" : contenu,
                    "theme" : theme
            }

            fichier_json.append(new_article)
        
        
        utils.create_json(file_target, fichier_json, 'LeFigaroExistant/', 'lfi')