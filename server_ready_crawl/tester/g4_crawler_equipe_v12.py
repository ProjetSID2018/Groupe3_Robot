# Group 4
# Realized by DELOEUVRE Noémie, BENJEBRIA Sofian

import g4_utils_v40 as utils
import re


def recovery_information_equi(url_article):
    """
        Arguments:
            - url of one article
        Returns:
            - informations of the article
    """
    try:
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
        date_p = ""
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

    except:
        article = utils.recovery_article('', 'Equipe',
                                         '', '', '', '')
    return(article)


def recovery_link_old_articles_equi(url_rss):
    """
        Argument:
            url_rss : string
        Return:
            link_article = list
        Retrieving links of new articles thanks to the rss feed
    """
    list_category = ["Athletisme", "Aussi/Aviron", "Auto-moto",
                     "Aussi/Badminton", "Aussi/Baseball", "Basket",
                     "Aussi/Biathlon", "Aussi/Boxe", "Aussi/Canoe-kayak",
                     "Cyclisme", "Aussi/Equitation", "Aussi/Escrime",
                     "Adrenaline/Escalade", "Football",
                     "Aussi/Football-americain", "Formule-1", "Golf",
                     "Aussi/Gymnastique", "Aussi/Halterophilie",
                     "Handball", "Hippisme", "Aussi/Hockey-sur-gazon",
                     "Aussi/Judo", "Natation", "Basket/NBA",
                     "Aussi/Pentathlon-moderne", "Rugby", "Sports-de-combat",
                     "Sports-us", "Aussi/Squash", "Adrenaline/Surf", "Tennis",
                     "Aussi/Tennis-de-table", "Aussi/Tir", "Aussi/Tir-a-l-arc",
                     "Aussi/Triathlon", "Aussi/Mma", "Voile",
                     "Aussi/Volley-ball", "Natation/Water-polo",
                     "Aussi/Jeux-paralympiques"]

    # We retrieve the URL feeds for each page of category
    link_article = []
    for cat in list_category:
        url_rss_cat = url_rss + cat + "/"
        soup = utils.recovery_flux_url_rss(url_rss_cat)
        # We retrieve all the articles for a given page
        for div in soup.find_all('div'):
            if div.get("class") == ['home__colead__split']:
                new_article = "https://www.lequipe.fr" + div.a.get("href")
                link_article.append(new_article)
    return(link_article)


def recovery_old_article_equi(file_target="data/clean/robot/"):
    file_json = []
    url_rss = "https://www.lequipe.fr/"
    links_article = recovery_link_old_articles_equi(url_rss)

    i = 0
    for link in links_article:
        new_article = recovery_information_equi(link)
        if utils.is_empty(new_article) is False:
            file_json.append(new_article)
            i += 1
        if i == 20:
            utils.create_json(file_target, file_json, "Equip_old/", "equi")
            i = 0
            file_json = []
    utils.create_json(file_target, file_json, "Equip_old/", "equi")


if __name__ == '__main__':
    recovery_old_article_equi()
    # /var/www/html/projet2018/data/clean/robot/
