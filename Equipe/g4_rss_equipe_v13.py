# Group 4
# DELOEUVRE Noémie, BENJEBRIA Sofian

import g4_utils_v40 as utils
import re
import datetime as date


def recovery_information_equipe(url_article):
    """
        Arguments:
            - url of one article
        Returns:
            - informations of the article
    """
    soup_article = utils.recovery_flux_url_rss(url_article)

    # Retrieving of title
    balise_title = soup_article.title.get_text()
    sep = balise_title.split(" - ")
    title = sep[0]
    title = title.encode("latin1").decode()

    # Retrieving of the author
    author = []
    aut = ""
    for meta in soup_article.find_all('meta'):
        if meta.get("name") == 'Author':
            aut = meta.get("content")
            aut = aut.encode("latin1").decode()
            author.append(aut)

    # Retrieving of date of publication
    for div in soup_article.find_all('div'):
        if div.get("class") == ['article__date']:
            for t in div.find_all('time'):
                if t.get("itemprop") == 'datePublished':
                    raw_date = t.get("datetime")
                    date_p = raw_date[0:10]

    # Retrieving of the artical theme
    theme = ""
    for div in soup_article.find_all('div'):
        if div.get("class") == ['navigation__sousmenu']:
            theme = div.get("libelle")
            theme = theme.encode("latin1").decode()

    # Retrieving the content of the article
    contents = ""
    for div in soup_article.find_all('div'):
        if div.get("itemprop") == 'mainEntityOfPage':
            for div2 in div.find_all('div'):
                for valeur in re.finditer('lire-aussi',
                                          str(div2.get("class"))):
                    div2.string = ""
                for valeur2 in re.finditer('paragraphe__exergue',
                                           str(div2.get("class"))):
                    div2.string = ""
            for span in div.find_all('span'):
                span.string = ""
            for block in div.find_all('blockquote'):
                block.string = ""
            for p in div.find_all('p'):
                if p.get("data-type") == 'Accroche':
                    contents = p.get_text()
                    contents = re.sub(r"\s\s+", " ", contents)
                    contents = contents.replace('°', ' ° ')

    article = utils.recovery_article(title, 'Equipe',
                                     author, date_p, contents, theme)
    return(article)


def recovery_link_new_articles_equipe(url_rss):
    """
        Arguments:
            - url of the page containing feed links for
            the different categories
        Returns :
            - list of urls of the different categories

    """
    soup = utils.recovery_flux_url_rss(url_rss)

    liste_url = []
    # Retrieving all urls of new RSS feeds of different categories
    for div in soup.find_all('div'):
        if div.get("class") == ['glace']:
            for a in div.find_all('a'):
                val = re.compile('^(http://www.lequipe.fr/rss/actu_rss)')
                for valeur in val.finditer(str(a.get("href"))):
                    liste_url.append(a.get("href"))

    return(liste_url)


def recovery_new_articles_equipe(file_target="data/clean/robot/" +
                                 str(date.datetime.now().date()) + "/"):
    """
        Returns:
            - creation of a json for each new article
    """
    file_json = []
    i = 0
    list_url = recovery_link_new_articles_equipe("https://www.lequipe.fr/rss/")
    for url in list_url:
        soup_url = utils.recovery_flux_url_rss(url)
        items = soup_url.find_all("item")
        article_equipe = []

        # We're picking up every new article in a list
        for item in items:
            article_equipe.append(re.search(r"<link/>(.*)", str(item))[1])
        # Each article is analized one by one
        for article in article_equipe:
            new_article = recovery_information_equipe(article)
            if utils.is_empty(new_article) is False:
                file_json.append(recovery_information_equipe(article))
            i += 1
        if i == 20:
            utils.create_json(file_target, file_json, "Equipe_rss/",
                              "equi")
            i = 0
            file_json = []

    utils.create_json(file_target, file_json, "Equipe_rss/",
                      "equi")


if __name__ == '__main__':
    recovery_new_articles_equipe()
