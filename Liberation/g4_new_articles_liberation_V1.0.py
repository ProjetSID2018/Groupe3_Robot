#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Tue Jan  9 13:28:26 2018

@author: Hbabou Nabil, Seguela Morgan

V1.0 
Extraction des articles du fux RSS

V1.1
Decoupage du code en Fonctions
"""

import os
import lxml.html as lh
import json
import datetime as date
from bs4 import BeautifulSoup
import requests
import re
from unidecode import unidecode 
import g4_utils_v2 as utilsg4

def get_rss_infos():
    """Get all articles link
    
    Returns:
        list -- list of articles url
    """

    url_rss_lib = "http://www.liberation.fr/rss"
    req = requests.get(url_rss_lib)
    data = req.text
    soup = BeautifulSoup(data, "lxml")

    rss_items = soup.find_all("li")

    rss_list = []

    link_rss = []

    for ri in rss_items:
        if ri.get("class") == ['rss-item']:
            rss_list.append(ri.a.get('href'))
            
    for rl in rss_list:
        req = requests.get(rl)
        data = req.text
        soup = BeautifulSoup(data, "lxml")
        entre = soup.find_all('entry')
        for e in entre :
            link_rss.append(e.link.get('href'))

    return link_rss


def get_information(article_link):
    """Extact informations from all these articles
    
    Arguments:
        article_link {string} -- url of an article
    
    Returns:
        dict -- dict of all informations
    """

    
    
    if "video" in article_link:
        return None

    else:
        
        req = requests.get(article_link)
        data = str(unidecode(req.text))
        soup = BeautifulSoup(data, "lxml")
        print(article_link)
        if soup.find("div", class_ = "direct-headband"):
            return None
        else:
            balise_title = soup.find('title').get_text()
            print(balise_title)

            if(balise_title):
                newspaper = balise_title[-10:]
                title = balise_title[0:-12]
            else :
                print("Probleme_liberation article :\n", article_link)

            if newspaper != "Liberation":
                return None

            else:
                author = ""
                for span in soup.find_all('span'):
                    if span.get("class") == ['author']:
                        print(article_link)
                        if(span.a):
                            author = span.a.string
                    if span.get("class") == ['date']:
                        print("ok")
                        if(span.time):
                            date_p = date.datetime.strptime(span.time.get("datetime"),"%Y-%m-%dT%H:%M:%S").date()
                            date_p = date_p.strftime(span.time.get("datetime"))
                
                
                content = ""        
                for div in soup.find_all('div'):
                    for p in div.find_all('p'):
                        content += p.get_text() + " "
                content = re.sub("<>", "", content)
                
                new_article = {
                        "title" : title,
                        "newspaper" : newspaper,
                        "author" : [author],
                        "date_publi" : date_p,
                        "theme" : " ",
                        "content" : content
                }
                return new_article

def recuperation_info_libe():
    """Main fonction that get all articles url, extract the informations and create a JSON File
    """

    file_target = "data/clean/robot/" + str(date.datetime.now().date()) +"/"
    os.makedirs(file_target, exist_ok=True)

    source = "liberation/"

    link_rss = get_rss_infos()
    
    list_articles = []

    for lr in link_rss:
        print(lr)
        informations = get_information(lr)
        if informations:
            list_articles.append(get_information(lr))

    utilsg4.create_json(file_target, list_articles, source, "libe")


if __name__ == '__main__':
    recuperation_info_libe()
