from telerama import Telerama as Tera
from minutes import Minutes as Minu
from equipe import Equipe as Equi
from femina import Femina as Femi
from figaro import Figaro as Figa
from futuramaSciences import FuturamaSciences as FS
from humanite import Humanite as Huma
from laDepeche import LaDepeche as LDP
from laTribune import LaTribune as LTR
from leGorafi import LeGorafi as LGR
from lePoint import LePoint as LPT
from liberation import Liberation as Libe
from nouvelObs import NouvelObs as NBS
from journal_exception import JournalException
from journal_manager import JournalManager as JM
import datetime as date
from article import Article

try:
    tera=Tera("Telerama","tera","http://www.telerama.fr")
    """minu=Minu("20 minutes","minu","http://www.20minutes.fr")
    equi=Equi("Equipe","equi","https://www.lequipe.fr")
    femi=Femi("Femina","femi","http://www.femina.fr")
    figa=Figa("Figaro","figa","http://www.lefigaro.fr")
    fs=FS("Futurama Sciences","fs","https://www.futura-sciences.com")
    huma=Huma("Humanite","huma","https://humanite.fr")
    ldp=LDP("La depeche","ldp","https://www.ladepeche.fr")
    ltr=LTR("La Tribune","ltr","http://www.latribune.fr")
    lgr=LGR("Le Gorafi","lgr","http://www.legorafi.fr")
    lpt=LPT("Le Point","lpt","http://www.lepoint.fr")
    libe=Libe("Liberation","libe","http://www.liberation.fr")
    nbs=NBS("Nouvel Obs","nbs","http://www.nouvelobs.com")"""
    #tera.add_article("se")
    # ok print(len(tera.get_list_article()))
    jm=JM(tera,"/home/etudiant/Documents/ProjetSID/objet/Art/" + str(date.datetime.now().date()) +"/","telerama")
    #jm=JM(minu,"/home/etudiant/Documents/ProjetSID/objet/Art/" + str(date.datetime.now().date()) +"/","minutes")
    # okart=Article("title","test",["Mr"],"12-1-2017","irem","cin")
    # ok print(art.id_art)
    # ok print(jm.already_exists(art))
    jm.create_json(new=False)

except JournalException as je:
    print(je)
    