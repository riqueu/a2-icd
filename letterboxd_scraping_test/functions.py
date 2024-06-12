"""Módulo com funções utilizadas em outros módulos"""

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
