#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Thu Jan 18 14:35:53 2018

@author: nabil
"""

import os
import datetime as date
from bs4 import BeautifulSoup
import requests
import re
from unidecode import unidecode
import g4_utils_v2 as utilsg4


def linkRSS(url_rss_lib):
    rss_list = []
    link_rss = []
    req = requests.get(url_rss_lib)
    data = req.text
    soup = BeautifulSoup(data, "lxml")
    rss_items = soup.find_all("tr")
    # Flux RSS
    for ri in rss_items:
        rss_list.append(ri.a.get('href'))
    for rl in rss_list:
        req = requests.get(rl)
        dt = req.text
        sp = BeautifulSoup(dt, "lxml")
        item = sp.find_all('item')
        # recovery link rss for each article
        for i in item:
            link_rss.append(re.search(r"<link/>(.*)", str(i)).group(1))
    return link_rss


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


def recuperation_info_lmde_rss():
    # Directory path
    file_target = "/Users/nabil/Desktop/data/clean/robot/" + str(date.datetime.now().date()) + "/"
    os.makedirs(file_target, exist_ok=True)
    source = "l/"
    file_target_source = file_target + source
    os.makedirs(file_target_source, exist_ok=True)
    url_rss_lib = "http://www.lemonde.fr/rss/"
    abbreviation = "lmde"
    listRSS = linkRSS(url_rss_lib)
    i = 0
    list_articles = []
    for article_link in listRSS:
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
    recuperation_info_lmde_rss()
