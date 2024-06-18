"""Módulo da extração de dados do Letterboxd"""

from bs4 import BeautifulSoup
import requests
import pandas as pd
import functions_scrapping as f

def get_film_url(film_name, year_release = None):
    """Função que recebe string com nome do filme (e ano, opcionalmente) e retorna seu link no letterboxd

    Args:
        film_name (str): Nome do Filme
        year_release (Union[int, None], optional): Ano do filme (para filmes que tem nome de outro filme). Defaults to None.

    Returns:
        str: url do filme no site Letterboxd
    """
    search_query = f"{film_name} {year_release}" if year_release else film_name
    search_query = search_query.replace(" ", "+")
    search_url = f"https://letterboxd.com/search/{search_query}/"

    # Requisição HTTP para a página de resultados de busca
    page = requests.get(search_url)
    soup = BeautifulSoup(page.text, "html.parser")

    # Encontrando o link para o primeiro filme na lista de resultados
    film_title_wrappers = soup.find_all("span", class_="film-title-wrapper")

    if film_title_wrappers:
        # Acessando o primeiro elemento da lista de resultados
        first_film = film_title_wrappers[0]
        
        # Encontrando o link (href) dentro do elemento do filme
        film_link = first_film.find("a", href=True)
        
        if film_link:
            # Construindo o URL completo do filme
            url_film = "https://letterboxd.com" + film_link.get("href")
            return url_film
    
    # Caso nenhum link seja encontrado, retorna None
    return None

def get_data_reviews(url, pages):
    """_summary_

    Args:
        url (str): url da pagina do filme no Letterboxd
        pages (int): quantidade de paginas a serem analisadas.

    Returns:
        DataFrame: dataframe com as informações das reviews analisadas
    """
    # Atribui o input a variaveis locais
    url_base = url
    page_ammount = pages
    page_count = 1

    headers = ["Username", "Date", "Score", "Review", "Length"]
    df = pd.DataFrame(columns=headers)

    while True:
        print(f"Escaneando página {page_count}")
        # Cada Iteração é uma pagina com várias reviews (mais engajadas -> menos engajadas)
        url_page = url_base + "reviews/by/activity/page/" + str(page_count)
        page = requests.get(url_page)
        soup = BeautifulSoup(page.text, "lxml")
        
        page_data = []
        table = soup.find_all("li", class_="film-detail")

        for each_review in table:
            user_name = each_review.find(class_="name").text.strip()
            
            # Chama a função para pegar data em formato YYYY/MM/DD
            date = f.convert_date(each_review.find(class_="_nobr").text.strip())
            
            # Chama função em functions_scrapping.py para conseguir o número da nota
            score = f.get_score(each_review.find(class_="attribution"))
            
            # Chama função com uma string do HTML da classe da review para conseguir a review tratada
            review = f.get_review(str(each_review.find(class_="body-text -prose collapsible-text")))
            
            if not user_name:
                user_name = "Unnamed"
            
            # Cria row_data e dá append dessa review na lista de reviews da pagina
            row_data = {'Username': user_name, 'Date': date, 'Score': score, 'Review': review, 'Length': len(review)}
            page_data.append(row_data)
        
        # Cria o dataframe temporário com as reviews dessa pagina e o concatena no principal
        df_temp = pd.DataFrame(page_data, columns=headers)
        # Caso o df principal não exista ainda, coloca-o com as informações da primeira pagina
        if df.empty:
             # Evitar FutureWarning (p/ concatenação de dataframes vazios)
            df = df_temp
        else:
            df = pd.concat([df, df_temp], ignore_index=True)
        
        # Se não há próxima página ou chegou no limite dado, quebra o loop.
        if not soup.find("a", class_="next") or page_count == page_ammount:
            print("Dados coletados")
            break
        page_count += 1
    
    # Remove linhas não avaliadas ou que a data não é accessível
    df = df[df["Score"] != "Unrated"]
    df = df[df["Date"]  != "Date Not Accessible"]
    # Cria a Coluna da diferença entre elemento e média e arredonda para 2 casas decimais
    # OBJETIVO: Verificar se análise está com a nota acima ou abaixo da média geral das reviews analisadas.
    df["Deviation from the Mean"] = df["Score"] - df["Score"].mean()
    df["Deviation from the Mean"] = df["Deviation from the Mean"].astype(float).round(2)
    
    return df

def create_xlsx(df, tipo):
    """Função que cria arquivos Excel

    Args:
        df (DataFrame): dataframe de entrada
        tipo (str): df das informações do filme ou das reviews dele
    """
    if tipo == "reviews":
        df.to_excel("reviews.xlsx") 
        print("Arquivo Excel criado em reviews.xlsx!")
    elif tipo == "movie_info":
        df.to_excel("filme.xlsx")
        print("Arquivo Excel criado em filme.xlsx!")
    else:
        print("Tipo de arquivo não encontrado.")

def get_movie_info(url):
    """Função para conseguir nome, ano, diretor, e duração do filme

    Args:
        url (str): url do filme Letterboxd

    Returns:
        list: lista com essas informações
    """
    page = requests.get(url)
    soup = BeautifulSoup(page.text, "lxml")
    
    page_data = []
    page_data.append(soup.find(class_="headline-1 filmtitle").text.strip())
    page_data.append(soup.find(class_="releaseyear").text.strip())
    page_data.append(soup.find(class_="contributor").text.strip())
    runtime = soup.find(class_="text-link text-footer").text.strip()
    page_data.append(int(''.join([c for c in runtime if c.isdigit()])))
    return page_data
