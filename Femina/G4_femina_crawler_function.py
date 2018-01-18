# Group 4
# DELOEUVRE Noémie

import g4_utils_v40 as utils
import re
import datetime as date


def recovery_information_fem(url_article):
    """
        Arguments:
            - url of one article
        Returns:
            - informations of the article
    """
    soup_article = utils.recovery_flux_url_rss(url_article)

    title = soup_article.title.get_text()
    title = title.split(" - ")
    title = title[0]

    for meta in soup_article.find_all('meta'):
        if meta.get("property") == 'article:published_time':
            raw_date = meta.get("content")
            date_p = raw_date[0:10]

    author = []
    for meta in soup_article.find_all('meta'):
        if meta.get("property") == 'article:author':
            author.append(meta.get("content"))

    theme = ""
    for link in soup_article.find_all('link'):
        if link.get("rel") == ['Index']:
            link_theme = link.get("href")
            part_link = link_theme.split("/")
            theme = part_link[3]

    contents = ""
    for div in soup_article.find_all('div'):
        if div.get("class") == ['chapo']:
            for p in div.find_all('p'):
                contents += p.get_text() + " "
        if div.get("class") == ['contenu']:
            for p in div.find_all('p'):
                contents += p.get_text() + " "
        if div.get("class") == ['diaporama']:
            for p in div.find_all('p'):
                contents += p.get_text() + " "
    contents = re.sub(r"\s\s+", " ", contents)

    article = utils.recovery_article(title, 'Femina',
                                     author, date_p, contents, theme)
    return(article)


def recovery_link_new_articles_fem():
    """
        Arguments:
            - url of the page containing feed links for
            the different categories
        Returns :
            - list of urls of the different categories
    """

    list_category = ["Beaute/Coiffure", "Beaute/Beaute-People",
                     "Beaute/Parfums", "Beaute/Soins-visage-et-corps",
                     "Beaute/Maquillage", "Mode/Tendances", "Mode/Defiles",
                     "Mode/Lingerie", "Mode/Mode-People",
                     "Cuisine/Recettes-de-chefs",
                     "Cuisine/Shopping-et-conseils",
                     "Cuisine/Idees-de-recettes-par-theme",
                     "Psychologie/Psycho", "Psychologie/Societe",
                     "Psychologie/Argent-Droit", "People/Vie-des-people",
                     "Culture/Series", "Culture/Musique",
                     "Culture/Cinema-et-DVD", "Culture/Sorties",
                     "Loisirs/Jardinage", "Loisirs/Voyages",
                     "Loisirs/Tendace-deco", "Sexo/Sexualite", "Sexo/Amour",
                     "Sante-Forme/Bien-etre", "Sante-Forme/Sport",
                     "Sante-Forme/Regimes-Nutrition", "Sante-Forme/Sante",
                     "Famille/Grossesse", "Famille/Bebe", "Famille/Enfant",
                     "Famille/Adolescent"]
    article_fem = []
    for category in list_category:
        for i in range(2, 5):
            url_rss_fem = "http://www.femina.fr/" +\
                category + "/page-" + str(i)
            soup_url = utils.recovery_flux_url_rss(url_rss_fem)

            for h2 in soup_url.find_all('h2'):
                for a in h2.find_all('a'):
                    article_fem.append(a.get("href"))
            for h3 in soup_url.find_all('h3'):
                for a in h3.find_all('a'):
                    article_fem.append(a.get("href"))

    return(article_fem)


def recovery_new_articles_fem(file_target="data/clean/robot/" +
                              str(date.datetime.now().date()) + "/"):
    """
        Returns:
            - creation of a json for each new article
    """
    file_json = []
    i = 0
    article_fem = recovery_link_new_articles_fem()
    for article in article_fem:
        new_article = recovery_information_fem(article)
        if utils.is_empty(new_article) is False:
            file_json.append(new_article)
            i += 1
        if i == 20:
            utils.create_json(file_target, file_json, "Femina_crawler/",
                              "fem")
            i = 0
            file_json = []

    utils.create_json(file_target, file_json, "Femina_crawler/",
                      "fem")


if __name__ == '__main__':
    recovery_new_articles_fem()
