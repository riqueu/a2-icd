"""Módulo com funções utilizadas no scrapping"""

from bs4 import BeautifulSoup
import re

def get_score(atribuicao):
    estrela = atribuicao.find("span").text.strip()
    score = 0.0
    score += estrela.count("★")
    score += estrela.count("½") * 0.5
    return score if score > 0 else "Unrated"


def get_review(review_entrada):
    # Troca line breaks e paragrafos por um espaço e transforma de volta em um objeto do Beautiful Soup
    review_div_soup = BeautifulSoup(re.sub(r'<\/?p>|<br\s?\/?>', ' ', review_entrada), "lxml")
    review = review_div_soup.text.strip()
    
    # Se a review tiver o aviso de spoilers do Letterboxd, remove aviso (de 60 caracteres).
    spoilers_string = "This review may contain spoilers. I can handle the truth.   "
    if spoilers_string in review:
        review = review[60::]
    return review