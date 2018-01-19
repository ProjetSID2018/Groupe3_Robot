#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Thu Jan 18 14:39:41 2018

@author: nabil
"""
import os
import datetime as date
from bs4 import BeautifulSoup
import requests
import re
from unidecode import unidecode
import g4_utils_v2 as utilsg4


def recent(url):
    rubriques = []
    links = []
    actualite = []
    req = requests.get(url)
    data = str(unidecode(req.text))
    soup = BeautifulSoup(data, "lxml")
    # In moment
    for nav in soup.find_all('nav', id="en_ce_moment"):
        for nv in nav.find_all("a"):
            actualite.append(url+nv.get("href"))
    # Recovery the articles in moment
    for act in actualite:
        req = requests.get(act)
        data = str(unidecode(req.text))
        soup = BeautifulSoup(data, "lxml")
        for h in soup.find_all('h3'):
            for lien in h.find_all('a'):
                links.append(url+lien.get('href'))
    # Sections
    for nav in soup.find_all('nav', id="navigation-generale"):
        for nv in nav.find_all("a"):
            rubriques.append(url+nv.get("href"))
            rubriques = rubriques[1:]
    # Recovery the articles of the different sections
    for rub in rubriques:
        req1 = requests.get(rub)
        data1 = str(unidecode(req1.text))
        soup1 = BeautifulSoup(data1, "lxml")
        for art in soup1.find_all('article'):
            for lien in art.find_all('a'):
                links.append(url+lien.get('href'))
    return links


def info_articles(article_link):
    req = requests.get(article_link)
    data = req.text
    soup = BeautifulSoup(data, "lxml")

    title = unidecode.unidecode(soup.find('title').string)

    newspaper = "Le Monde"

    # Article theme
    if(soup.find("li", class_="ariane z2")):
        theme = soup.find("li", class_="ariane z2").find("a").get_text()
    else:
        theme = 'Forum'

    # Author of the article
    if(soup.find("span", class_="auteur")):
        if(soup.find("span", class_="auteur").a):
            author = soup.find("span", class_="auteur").find("a").get_text()
        else:
            author = soup.find("span", class_="auteur").get_text()
        author = re.sub(r"\s\s+", " ", author)
        author = re.sub(r"^ ", "", author)
    else:
        author = ""

    # publication date
    da = re.search(r"\d{4}-\d{2}\-\d{2}", soup.find("time").get("datetime"))[0]
    if(da):
        date_p = date.datetime.strptime(da, "%Y-%m-%d").strftime("%d/%m/%Y")
    else:
        date_p = str(date.datetime.now().strftime("%d/%m/%Y"))

    # Article content
    content = ""
    for div in soup.find_all('div'):
        for p in div.find_all('p'):
            content += p.get_text() + " "
    content = unidecode.unidecode(re.sub(r"\s\s+", " ", content))

    new_article = utilsg4.recovery_article(
        title, newspaper, [author], date_p, content, theme)

    return new_article

def recuperation_info_lmde():
    # Directory path
    file_target = "/Users/nabil/Desktop/data/clean/robot/" + str(date.datetime.now().date()) + "/"
    os.makedirs(file_target, exist_ok=True)
    source = "l/"
    file_target_source = file_target + source
    os.makedirs(file_target_source, exist_ok=True)
    abbreviation = "lmde"
    url = "http://www.lemonde.fr"
    links = recent(url)
    i = 0
    list_articles = []
    for article_link in links:
        if "/article/" in article_link:
            i += 1
            list_articles.append(info_articles(article_link))

            if i == 20:
                utilsg4.create_json(
                    file_target, list_articles, source, abbreviation)
                i = 0
                list_articles = []

    utilsg4.create_json(file_target, list_articles, file_target_source, abbreviation)


if __name__ == '__main__':
    recuperation_info_lmde()
