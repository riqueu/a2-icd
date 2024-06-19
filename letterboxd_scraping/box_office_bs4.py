from bs4 import BeautifulSoup
import requests

url_base = "https://www.boxofficemojo.com"

# Funcao para converter o nome do filme para o formato de busca do site
def convert(name):
    return name.replace(" ", "+")

def get_release_info(name, year = 0):
    """Função que pega relações monetárias e outras informações do filme do site Box Office Mojo

    Args:
        name (str): Nome do filme
        year (int, optional): Ano de lançamento. Defaults to 0.

    Returns:
        dict: Dicionário com informações monetárias, generos, distribuidora, etc.
    """
    converted_name = convert(name)

    url_page = url_base + "/search/?q=" + converted_name + " " + str(year)
    page = requests.get(url_page)
    soup = BeautifulSoup(page.text, "lxml")
    links = []
    todos_links = soup.find_all("a", class_ = "a-size-medium a-link-normal a-text-bold")
    
    # Pega somente filmes que têm o nome que buscamos, se não houver nenhum, retorna None
    for link in todos_links:
        if link.text.strip() == name:
            links.append(link)
    if not links:
        return None

    # Se não houver ano especificado, pega o primeiro filme
    lim = 1 if not year else len(links)
    # Busca nos links o link certo (tem o ano igual ao ano esperado)
    for link in links[:lim]:
        url_movie = url_base + link.get('href')
        page_movie = requests.get(url_movie)
        movie_soup = BeautifulSoup(page_movie.text, "lxml")
        
        #Coleta o ano do filme e verifica se ele é o buscado
        movie_year = movie_soup.find("span", class_ = "a-color-secondary").text.strip()
        movie_year = int(movie_year[1:5]) # remove parenteses. Ex: "(2005)" -> 2005
        # se é o ano que procuramos, quebramos o loop
        if movie_year == year:
            break

    #Com a pagina do filme certo, coleto os valores (bilheteria e orçamento) e as informacoes relevantes da producao
    info_table = movie_soup.find("div", class_ = "a-section a-spacing-none mojo-gutter mojo-summary-table")

    keys = ["domestic", "international", "worldwide", "domestic_oppening", "budget", "distributor", "mpaa", "genres"]
    dict_movie = {}
    count = 0


    #Bilheteria
    box_offices = info_table.find_all(class_ = "money")

    for box_office in box_offices:
        value = box_office.text.strip()
        # Converte valores monetários para int. Ex: "$182,200,000" -> 182200000
        value = ''.join([c for c in value if c.isdigit()])
        dict_movie[keys[count]] = int(value)
        count += 1
        
    #Producao
    infos_field = info_table.find("div", class_="a-section a-spacing-none mojo-summary-values mojo-hidden-from-mobile")
    infos = infos_field.find_all("span")

    condition = 0
    for info in infos:
        data = info.text.strip()
        if data in ["Domestic Distributor", "MPAA", "Genres"]:
            condition = 1
        elif condition:
            cleaned_data = ' '.join(data.split()) # Evitar espaço vazio e line breaks nos generos
            dict_movie[keys[count]] = cleaned_data
            condition = 0
            count += 1
    
    return dict_movie
    
# Testes: print(get_release_info("Planet of the Apes", 2001))
# print(get_release_info("Planet of the Apes"))
# print(get_release_info("Planet of the Apes", 1968))