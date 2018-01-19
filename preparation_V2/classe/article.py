from unidecode import unidecode
from hashlib import md5

class Article:
    def __init__(self,_title,_newspaper,_authors,_date_publi,_content,_theme):
        self._set_title(_title)
        self._set_newspaper(_newspaper)
        self._set_authors(_authors)
        self._set_date_publi(_date_publi)
        self._set_content(_content)
        self._set_theme(_theme)

    def _get_title(self):
        return unidecode(self._title)
    
    def _get_newspaper(self):
        return unidecode(self._newspaper)
    
    def _get_authors(self):
        return self._authors

    def _get_date_publi(self):
        return unidecode(self._date_publi)

    def _get_content(self):
        return unidecode(self._content)

    def _get_theme(self):
        return unidecode(self._theme)

    def _set_title(self,_title):
        self._title=_title
    
    def _set_newspaper(self,_newspaper):
        self._newspaper=_newspaper

    def _set_authors(self,_authors):
        for i in range(len(_authors)):
            _authors[i]=unidecode(_authors[i])
        self._authors=_authors

    def _set_date_publi(self,_date_publi):
        self._date_publi=_date_publi

    def _set_content(self,_content):
        self._content=_content

    def _set_theme(self,_theme):
        self._theme=_theme


    def get_hash(self):
        hash=md5("{} {} {}".format(self.date_publi,self.title,self.newspaper).encode())
        return hash.hexdigest()
    
    def to_json(self):
        return {
            "id_art" : self.id_art,
            "title" : self.title,
            "newspaper" : self.newspaper,
            "authors" : self.authors,
            "date_publi" : self.date_publi,
            "content" : self.content,
            "theme" : self.theme
        }    

    @property
    def id_art(self):
        return self.get_hash()

    def __str__(self):
        return self._title

    title=property(_get_title,_set_title)
    newspaper=property(_get_newspaper,_set_newspaper)
    authors=property(_get_authors,_set_authors)
    date_publi=property(_get_date_publi,_set_date_publi)
    content=property(_get_content,_set_content)
    theme=property(_get_theme,_set_theme)

