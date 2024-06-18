"""Módulo Principal"""

import sys
import pandas as pd
import letterboxd_bs4 as letterboxd
from gpt import summary_based_on_reviews, summary_public_opinion, keywords_for_movie

# Pega a url e a quantidade de páginas para analisar da linha de comando
try:
    url = sys.argv[1]
    # Valor padrão (25 páginas) caso não seja um inteiro positivo ou seja vazio o argv[2].
    page_ammount = 25
    if len(sys.argv) >= 3:
        if int(sys.argv[2]) >= 0:
            page_ammount = int(sys.argv[2])
except:
    print("Erro de execução:")
    print("Uso: python main.py [url do filme] [paginas a ler] (opcional, padrão = 25 pags; '0' para todas (não recomendado))")
    exit()

# Função para pegar dataframe com dados
df_reviews = letterboxd.get_data_reviews(url, page_ammount)

print("Analisando dados...")

# Pega reviews e coloca em lista para passa-las para o GPT
reviews = df_reviews["Review"].tolist()

mean = round(df_reviews["Score"].mean(), 2)
general_info = letterboxd.get_movie_info(url)
movie_data = []

# Pega informações sobre o filme, incluindo algumas geradas pelo GPT, baseando-se nas reviews
name, year, director = general_info[0], general_info[1], general_info[2]
summary = summary_based_on_reviews(name, reviews)
public_opinion = summary_public_opinion(name, mean, reviews)
keywords = keywords_for_movie(name, reviews)
data_dict = {'Name': name, 'Year': year, 'Director': director, 'Mean': mean,
            'Summary': summary, 'Public Opinion': public_opinion, 'Keywords': keywords}
movie_data.append(data_dict)

# Cria dataframe com as informações do filme, incluindo analises do GPT
headers_film = ["Name", "Year", "Director", "Mean", "Summary", "Public Opinion", "Keywords"]
df_film = pd.DataFrame(movie_data, columns=headers_film)

# Função que cria os arquivos csv com os dados e informações do filme
letterboxd.create_csv(df_reviews, "reviews")
letterboxd.create_csv(df_film, "movie_info")