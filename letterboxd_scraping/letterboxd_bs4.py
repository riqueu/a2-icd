"""Módulo da extração de dados do Letterboxd"""

from bs4 import BeautifulSoup
import requests
import pandas as pd
import functions_scrapping as f
import box_office_bs4 as box_office
from gpt import summary_based_on_reviews, summary_public_opinion, keywords_for_movie


def get_topics(public_opinion):
    """Função que trata a string da opinião pública, gerada pelo gpt,
    deixando-a em um formato adequado para o dataframe

    Args:
        public_opinion (string): String com os topicos e notas, separados por virgula, gerados pelo gpt

    Returns:
        dict: Dicionario com os topicos suas respectivas notas
    """
    public_opinion = public_opinion.replace(" ", "")
    arr_topics = public_opinion.split(",")
    arr_dict = {arr_element.split(":")[0].lower() : float(arr_element.split(":")[1]) for arr_element in arr_topics}
    return arr_dict
    
def get_letterboxd_urls(genres):
    """Função que recebe um genero e retorna uma lista 
    com os 5 urls dos 5 filmes mais populares desse genero

    Args:
        genres (List): combinação de generos (2), ou (1)
        
    Returns:
        List: lista com o url dos 5 filmes
    """
    genres = genres[0:2]
    search_query = "+".join(genres)
    url = f"https://letterboxd.com/films/ajax/popular/genre/{search_query}/"

    page = requests.get(url)
    soup = BeautifulSoup(page.text, "lxml")

    tags = soup.find_all('div', attrs={'data-target-link': True})
    
    urls = []
    
    for i in range(5):
        url = "https://letterboxd.com" + tags[i]['data-target-link']
        urls.append(url)
    
    return urls


def get_data_reviews(url, pages):
    """Função que, dada url e quantidade de paginas a analisar, pega informações das reviews

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

    headers = ["Username", "Date", "Score", "Review", "Length", "Movie"]
    df = pd.DataFrame(columns=headers)

    while True:
        print(f"Escaneando página {page_count}/{pages}")
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
            row_data = {'Username': user_name, 'Date': date, 'Score': score, 'Review': review, 'Length': len(review), 'Movie': url}
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
    df.to_excel(f"{tipo}.xlsx")
    print(f"Arquivo Excel criado em {tipo}.xlsx")


def get_movie_info(url_letter, df_reviews):
    """Função para conseguir informações gerais sobre o filme

    Args:
        url (str): url do filme Letterboxd

    Returns:
        list: lista com essas informações
    """
    page_letter = requests.get(url_letter)
    soup_letter = BeautifulSoup(page_letter.text, "lxml")
    
    name = soup_letter.find(class_="headline-1 filmtitle").text.strip()
    year = int(soup_letter.find(class_="releaseyear").text.strip())
    director = soup_letter.find(class_="contributor").text.strip()
    runtime = soup_letter.find(class_="text-link text-footer").text.strip()
    runtime = int(''.join([c for c in runtime if c.isdigit()]))
    
    reviews = df_reviews["Review"].tolist()
    
    mean = round(df_reviews["Score"].mean(), 2)
    deviation = round(df_reviews["Score"].std(), 2)
    summary = summary_based_on_reviews(name, reviews)
    public_opinion = summary_public_opinion(name, reviews)
    topics = get_topics(public_opinion)
    keywords = keywords_for_movie(name, reviews)
    
    url_box = box_office.get_box_url(name, year)
    release_dict = box_office.get_release_info(url_box)
    
    page_data = []
    
    row_data = {'Name': name, 'Year': year, 'Director': director, 'Runtime (mins)': runtime,
                'Mean': mean, 'Standard Deviation': deviation,'Summary': summary,
                'Script' : topics['script'], 'VFX' : topics['vfx'], 'Casting' : topics['casting'], 'SFX' : topics['sfx'], 
                'Editing' : topics['editing'], 'Directing' : topics['directing'], 'Keywords': keywords}

    row_data.update(release_dict)
    
    headers = ['Name', 'Year', 'Director', 'Runtime (mins)', 'Mean', 'Standard Deviation', 'Summary', 
               'Script', 'VFX', 'Casting', 'SFX', 'Editing', 'Directing', 'Keywords', 'Domestic', 'International',
               'Worldwide', 'Domestic Oppening', 'Distributor', 'MPAA', 'Genres']
    
    page_data.append(row_data)
    df = pd.DataFrame(page_data, columns=headers)
    
    return df
