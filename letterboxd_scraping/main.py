"""Módulo Principal"""

import pandas as pd
import letterboxd_bs4 as scrape
from gpt import summary_based_on_reviews, summary_public_opinion, keywords_for_movie

while True:
    # Pega input com nome, ano (opcional), e quantidades de pagina a ler (opcional)
    try:
        film_input = input("Film Name: ").strip()
        
        # Se input vazio, ano é None, se tiver algo, converte pra inteiro
        year_input = input("Release Year (optional): ")
        if year_input.strip() == '':
            year_input = None
        else:
            year_input = int(year_input)
        
        # Mesma coisa para quantidade de páginas a ler
        # Máximo de 23 páginas por conta do limite de contexto do GPT 3.5 Turbo
        page_ammount = input("Pages to read (defaults to 15) (max: 23): ")
        if page_ammount.strip() == '':
            page_ammount = 15
        # Valida quantidade de paginas, se invalida, itera novamente
        elif int(page_ammount) >= 24 or int(page_ammount <= 0):
            print("Invalid page ammount")
            continue
        else:
            page_ammount = int(page_ammount)
        # Caso tudo dê certo, quebra o loop e segue o código
        break
    
    # Caso haja erro de conversão dos valores de ano/páginas, avisa usuario e itera novamente
    except ValueError:
        print("Erro de conversão! Escolha valores inteiros positivos")

# Chama função para pegar o link do filme no Letterboxd
url = scrape.get_film_url(film_input, year_input)
if not url:
    print("Filme não encontrado, verifique a sintaxe do que foi escrito")
    exit()

# Função para pegar dataframe com dados
df_reviews = scrape.get_data_reviews(url, page_ammount)

print("Analisando dados...")

# Pega reviews e coloca em lista para passa-las para o GPT
reviews = df_reviews["Review"].tolist()

general_info = scrape.get_movie_info(url)
movie_data = []

# Pega informações sobre o filme, incluindo algumas geradas pelo GPT, baseando-se nas reviews
name, year, director, runtime = general_info[0], general_info[1], general_info[2], general_info[3]
mean = round(df_reviews["Score"].mean(), 2)
deviation = round(df_reviews["Score"].std(), 2)
summary = summary_based_on_reviews(name, reviews)
public_opinion = summary_public_opinion(name, mean, reviews)
keywords = keywords_for_movie(name, reviews)
data_dict = {'Name': name, 'Year': year, 'Director': director, 'Runtime (mins)': runtime, 'Mean': mean, 
            'Standard Deviation': deviation, 'Summary': summary, 'Public Opinion': public_opinion, 'Keywords': keywords}
movie_data.append(data_dict)

# Cria dataframe com as informações do filme, incluindo analises do GPT
headers_film = ["Name", "Year", "Director", "Runtime (mins)", "Mean", "Standard Deviation", "Summary", "Public Opinion", "Keywords"]
df_film = pd.DataFrame(movie_data, columns=headers_film)

# Função que cria os arquivos csv com os dados e informações do filme
scrape.create_xlsx(df_reviews, "reviews")
scrape.create_xlsx(df_film, "movie_info")
