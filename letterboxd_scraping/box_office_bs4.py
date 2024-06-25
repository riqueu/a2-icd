"""Módulo da extração de dados do Box Office"""

from bs4 import BeautifulSoup
import pandas as pd
import requests

url_base = "https://www.boxofficemojo.com"

# Funcao para converter o nome do filme para o formato de busca do site
def convert(name):
    return name.replace(" ", "+")


def get_box_url(name, year = 0):
    """Função que recebe o nome e o ano de um filme e retorna a URL do filme

    Args:
        name (str): Nome do filme
        year (int, optional): Ano de lançamento do filme. Defaults to 0. (Pega o primeiro caso 0)

    Returns:
        str: URL do filme no Box Office
    """
    converted_name = convert(name)

    url_page = url_base + "/search/?q=" + converted_name # + " " + str(year)
    page = requests.get(url_page)
    soup = BeautifulSoup(page.text, "lxml")
    for film in soup.find_all('div', class_='a-fixed-left-grid'):
        film_name = film.find('a', class_='a-size-medium a-link-normal a-text-bold').text.strip()
        film_year = film.find('span', class_='a-color-secondary').text.strip()
        film_year = int(film_year[1:5]) # remove parenteses. Ex: "(2005)" -> 2005
        if name == film_name:
            if year != 0 and year == film_year:
                return url_base + film.find('a', class_='a-size-medium a-link-normal a-text-bold').get('href')         
    return None


def get_release_info(url):
    """Função que pega relações monetárias e outras informações do filme do site Box Office Mojo

    Args:
        url (str): URL do filme no box office

    Returns:
        DataFrame: dataframe com as informações monetárias
    """
    page_movie = requests.get(url)
    movie_soup = BeautifulSoup(page_movie.text, "lxml")
    #Com a pagina do filme certo, coleto os valores (bilheteria e orçamento) e as informacoes relevantes da producao
    info_table = movie_soup.find("div", class_ = "a-section a-spacing-none mojo-gutter mojo-summary-table")

    keys = ["Domestic", "International", "Worldwide", "Domestic Oppening", "Distributor", "MPAA", "Genre"]
    dict_movie = {}
    count = 0

    #Bilheteria
    box_offices = info_table.find_all(class_ = "money")

    for box_office in box_offices[:4]:
        value = box_office.text.strip()
        # Converte valores monetários para int. Ex: "$182,200,000" -> 182200000
        value = ''.join([charac for charac in value if charac.isdigit()])
        dict_movie[keys[count]] = int(value)
        count += 1
        
    #Producao
    infos_field = info_table.find("div", class_="a-section a-spacing-none mojo-summary-values mojo-hidden-from-mobile")
    infos = infos_field.find_all("span")

    condition = 0
    for info in infos:
        data = info.text.strip()
        if data in ["Domestic Distributor", "MPAA", "Genre"]:
            condition = 1
        elif condition:
            cleaned_data = ' '.join(data.split()) # Evitar espaço vazio e line breaks nos generos
            dict_movie[keys[count]] = cleaned_data
            condition = 0
            count += 1
    return dict_movie


def get_regional_info(url):
    page = requests.get(url)
    soup = BeautifulSoup(page.text, "lxml")
    tables = soup.find_all('table')
    # Remove a primeira tabela (tabela "By Release")
    tables = tables[1::]
    headers = ["Region", "Releases", "Lifetime Gross", "Rank"]
    df = pd.DataFrame(columns=headers)
    
    # Pega o ano do filme e remove o ano da string
    movie_name = soup.find("h1", class_="a-size-extra-large").text.strip()
    movie_name = movie_name[:-7:]

    # Para cada tabela continental, pega as informações dos países dessa tabela
    for table in tables:
        rows = []
        # Extrai as linhas da tabela
        for each_tr in table.find_all('tr')[1:]:  # Pula a primeira linha que contém os cabeçalhos
            cells = each_tr.find_all('td')
            row = [cell.text.strip() for cell in cells]
            # Pega o valor inteiro monetário, ex: $250,000 -> 250000
            row[2] = ''.join([charac for charac in row[2] if charac.isdigit()])
            rows.append(row)

        # Converte para um DataFrame do Pandas
        df_temp = pd.DataFrame(rows, columns=headers)
        
        if not df.empty:
            df = pd.concat([df, df_temp], ignore_index=True)
            continue
        df = df_temp
    
    df['Movie'] = [movie_name for i in range(len(df.index))]
    return df 
