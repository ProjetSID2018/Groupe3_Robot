# Group 4 Robot - Lea Besnard, Laetitia Krumeich, Noemie Deloeuvre

import g4_utils_v40 as utils
import re
from datetime import datetime
import datetime as date

def recovery_information_lt(url_article):
    """
    Arguments:
        - url of one article
    Returns:
        - informations of the article
    """
    soup_article = utils.recovery_flux_url_rss(url_article)

    # Retrieve the title
    title = soup_article.title.string

    # Retrieve the theme
    theme = ""
    for li in soup_article.find_all('li'):
        if li.get("itemprop") == 'itemListElement':
            theme = li.a.span.get_text()

    # Retrieve the author
    author = []
    for span in soup_article.find_all('span'):
        if span.get("class") == ['author-name']:
            author.append(span.a.span.get_text())

    # Retrieve the publication date
    date_p = ""
    for time in soup_article.find_all('time'):
        date_p = time.get("datetime")
        for valeur in re.finditer('[0-9]{4}\-[0-9]{2}\-[0-9]{2}', str(time)):
            date_p = valeur.group(0)

    # Retrieve the content
    contents = ""
    for div in soup_article.find_all('div'):
        if div.get("itemprop") == 'articleBody':
            for p in div.find_all('p'):
                contents += p.get_text() + " "

    article = utils.recovery_article(title, 'LaTribune',
                                     author, date_p, contents, theme)
    return(article)

def recovery_new_articles_lt(file_target="C:/Users/lea/Desktop/PROJET/" + str(date.datetime.now().date()) + "/"):

    list_category = ["actualites/economie/economie", "Entreprises-secteurs",
                     "media-telecom-entreprise", "finance-patrimoine-investir",
                     "opinions", "regions/economie-en-region"]
    file_json = []
    articles_latribune = []
    # We retrieve the URL feeds for each page of article
    for cat in list_category:
        url_latribune = "https://www.latribune.fr/" + cat + ".html"
        soup_url = utils.recovery_flux_url_rss(url_latribune)

        for ul in soup_url.find_all("ul"):
            if ul.get("class") == ['pagination-archive', 'pages']:
                for li in ul.find_all("li"):
                    for a in li.find_all("a"):
                        link = a.get("href")
                        link2 = "https://www.latribune.fr" + link
                        soup_url = utils.recovery_flux_url_rss(link2)

                        for div in soup_url.find_all("div"):
                            for valeur in re.finditer('title-river', str(div.get("class"))):
                                for a in div.find_all('a'):
                                    articles_latribune.append(a.get("href"))

    # Each article is analized one by one
    for article in articles_latribune:
        new_article = recovery_information_lt(article)
        if utils.is_empty(new_article) is False:
            file_json.append(new_article)

    utils.create_json(file_target, file_json, "latribune_crawler/", "lt")

if __name__ == '__main__': 
    recovery_new_articles_lt()
