# -*- coding: utf-8 -*-
"""
 Groupe 4
 MOTHES Céline
 V1 : create code
"""
import datetime as date
import unidecode
import re
import g4_utils_v40 as utils


def recovery_information_fusc(url):
    """
        Arguments:
            url : string
        Return :
            article : dictionary
        It retrieve for each article the title, newspaper, author, date, theme
    """
    soup = utils.recovery_flux_url_rss(url)
    # retrieve title
    title = ''
    title = unidecode.unidecode(soup.title.string)
    indice = title.find('|')
    if indice != -1:
        title = title[:indice-1]
    # retrieve the author
    author = []
    tag_author = soup.find('h3', attrs={'itemprop': 'author'})
    author.append(tag_author.get_text())

    # retrieve date
    publi_date = ''
    regex_date = re. search('[0-9]{2}\/[0-9]{2}\/[0-9]{4}', soup.time.string)
    publi_date = regex_date.group(0)
    publi_date = str(date.datetime.strptime(publi_date, '%d/%m/%Y').date())

    # retrieve content
    content = ''
    for p in soup.find_all('p'):
        for p2 in re.finditer('py0p5', p.get('class')[-1]):
            content += p.get_text()
    content = unidecode.unidecode(content)

    # retrieve theme
    delimiter = url.split('/')
    theme = delimiter[3]

    article = utils.recovery_article(title, 'FuturaSciences', author,
                                     publi_date, content, theme)
    return(article)


def recovery_old_articles_fusc(file_target = '/var/www/html/projet2018/data/clean/robot/'):
    """
        it create a json for each article
    """
    url = "https://www.futura-sciences.com/sitemap-html/actualites/"
    url_fusc = "https://www.futura-sciences.com"
    for ii in range(1, 202):
        links_article = []
        soup = utils.recovery_flux_url_rss(url + str(ii) + "/")
        for tag_div_link in soup.find_all('div', attrs={"class": "has-divider-bottom latest-item"}):
            links_article.append(url_fusc + tag_div_link.a.get('href'))
        list_articles = []
        for link_article in links_article:
            new_article = recovery_information_fusc(link_article)
            if not utils.is_empty(new_article):
                list_articles.append(new_article)
        utils.create_json(file_target, list_articles, 'FuturaSciences', 'fusc')


if __name__ == '__main__':
    recovery_old_articles_fusc()
