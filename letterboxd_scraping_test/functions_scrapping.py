"""Módulo com funções utilizadas no scrapping"""

from bs4 import BeautifulSoup
import re

def get_score(atribuicao):
    estrela = atribuicao.find("span").text.strip()
    if estrela == "★★★★★":
        return 5
    if estrela == "★★★★½":
        return 4.5
    if estrela == "★★★★":
        return 4
    if estrela == "★★★½":
        return 3.5
    if estrela == "★★★":
        return 3
    if estrela == "★★½":
        return 2.5
    if estrela == "★★":
        return 2
    if estrela == "★½":
        return 1.5
    if estrela == "★":
        return 1
    if estrela == "½":
        return 0.5
    return "Unrated"


def get_review(review_entrada):
    # Troca line breaks e paragrafos por um espaço e transforma de volta em um objeto do Beautiful Soup
    review_div_soup = BeautifulSoup(re.sub(r'<\/?p>|<br\s?\/?>', ' ', review_entrada), "lxml")
    review = review_div_soup.text.strip()
    
    # Se a review tiver o aviso de spoilers do Letterboxd, remove aviso (de 60 caracteres).
    spoilers_string = "This review may contain spoilers. I can handle the truth.   "
    if spoilers_string in review:
        review = review[60::]
    return review