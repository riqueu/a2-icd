"""Módulo com funções utilizadas no scrapping"""

from datetime import datetime
from bs4 import BeautifulSoup
import re

def get_score(atribuicao):
    """Função que transforma string da nota em float (ex: "★★★½" -> 3.5)

    Args:
        atribuicao (str): nota em estrelinhas

    Returns:
        float: nota em float
    """
    estrela = atribuicao.find("span").text.strip()
    score = 0.0
    score += estrela.count("★")
    score += estrela.count("½") * 0.5
    return score if score > 0 else "Unrated"


def get_review(review_entrada):
    """Função para tratar a string

    Args:
        review_entrada (str): string bagunçada

    Returns:
        str: string tratada
    """
    # Troca line breaks e paragrafos por um espaço e transforma de volta em um objeto do Beautiful Soup
    review_div_soup = BeautifulSoup(re.sub(r'<\/?p>|<br\s?\/?>', ' ', review_entrada), "lxml")
    review = review_div_soup.text.strip()
    
    # Se a review tiver o aviso de spoilers do Letterboxd, remove aviso (de 60 caracteres).
    spoilers_string = "This review may contain spoilers. I can handle the truth.   "
    if spoilers_string in review:
        review = review[60::]
    return review


def convert_date(date_str):
    """Função que converte a data do formato em string
    (ex: 26 Jan 2017) para o formato YYYY/MM/DD

    Args:
        date_str (str): data em string (ex: 19 May 2023)

    Returns:
        str: data em YYYY/MM/DD
    """
    try:
        date_obj = datetime.strptime(date_str, "%d %b %Y")
        return date_obj.strftime("%Y/%m/%d")
    except:
        return "Date Not Accessible"
