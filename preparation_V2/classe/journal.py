from article import Article
from journal_exception import JournalException
from abc import ABC, abstractmethod
from bs4 import BeautifulSoup
from requests import get as get_request


class Journal(ABC):

    def __init__(self, _name_journal, _abbreviation, _base_url=""):
        self.list_article=[]
        self.name_journal=_name_journal
        self._abbreviation=_abbreviation
        #self.source=source
        self._base_url=_base_url

    def __str__(self):
        return self.name_journal
    def add_article(self, article):
        """
        Arguments:
            article : Article 
        Return :
            void
            La méthode peut lever une execption si l'objet à ajouter n'est pas une article
        """
        if isinstance(article,Article):
            self.list_article.append(article)
        else:
            raise JournalException("Error")

    def find_list_article(self,new):
        """
        Arguments:
            new : boolean
            True si on veut récuperer les nouvelles articles 
            False si on veut récuperer les anciennes articles
        Return :
            [Article]
            La méthode peut lever une execption si l'objet à ajouter n'est pas une article
        """        
        urls=self.find_links(new)
        for url in urls:
            if not new :
                for article in self.find_articles(url):
                    self.add_article(article)
            else :
                self.add_article(self.find_article(url))
        return self.list_article
    

    def recovery_flux_url(self,url):
        """
        Arguments:
            url : string containing the url of the rss feed
        Return :
            BeautifulSoup
        """
        req = get_request(url)
        data = req.text
        soup = BeautifulSoup(data, "lxml")
        return(soup)

    def _get_abbreviation(self):
        return self._abbreviation

    def _set_abbreviation(self,_abbreviation):
        self._abbreviation=_abbreviation

    def _get_base_url(self):
        return self._base_url

    def _set_base_url(self,_base_url):
        self._base_url=_base_url

    @abstractmethod
    def find_article(self,url):
        """
        Arguments:
            url : string 
        Return :
            Article
        """
        pass

    @abstractmethod
    def find_articles(self,url):
        """
        Arguments:
            url : string 
        Return :
            [Article] 
        """
        pass

    @abstractmethod
    def find_links(self,new):
        """
        Arguments:
            new : boolean 
            True si on veut récuperer l'url des nouvelles articles 
            False si on veut récuperer l'url des anciennes articles
        Return :
            [string] : tableau d'url des articles
        """
        pass

    abbreviation=property(_get_abbreviation,_set_abbreviation)
    base_url=property(_get_base_url,_set_base_url)