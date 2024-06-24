"""Módulo Principal"""

import pandas as pd
import letterboxd_bs4 as letter
import box_office_bs4 as box
from export_excel import update_tables

# TODO: Pegar todos generos

genres = ["action", "adventure", "animation", "comedy", "crime", "documentary", "drama",
          "family", "fantasy", "history", "horror", "music", "mystery", "romance",
          "science-fiction", "thriller", "tv-movie", "war", "western"]
letterboxd_urls = letter.get_letterboxd_urls(genres)

# Cria DataFrames vazios com as headers.
headers_reviews = ["Username", "Date", "Score", "Review", "Length", "Movie"]
headers_films = ['Name', 'Year', 'Director', 'Runtime (mins)', 'Mean', 'Standard Deviation', 'Summary', 
                'Public Opinion', 'Keywords', 'Domestic', 'International', 'Worldwide', 
                'Domestic Oppening', 'Distributor', 'MPAA', 'Genres']
df_reviews = pd.DataFrame(columns=headers_reviews)
df_films = pd.DataFrame(columns=headers_films)

# Para cada filme, coleta informações das reviews e do filme
for film in letterboxd_urls:
    
    df_reviews_temp = letter.get_data_reviews(film, 2)
    print("Analisando dados do filme.")
    df_films_temp = letter.get_movie_info(film, df_reviews_temp)
    
    # Caso seja a primeira iteração, cria os dataframes, caso contrário, contacena-os
    if not df_reviews.empty:
        df_reviews = pd.concat([df_reviews, df_reviews_temp], ignore_index=True)
        df_films = pd.concat([df_films, df_films_temp], ignore_index=True)
    else:
        df_reviews, df_films = df_reviews_temp, df_films_temp

# Remove a string "See full company information" da Distribuidora do Filme
df_films["Distributor"] = df_films["Distributor"].str.replace("See full company information", "", regex=False).str.strip()

# Pega os URLs do Box Office para pegar informações monetárias
box_office_urls = []
names = df_films["Name"].tolist()
years = df_films["Year"].tolist()
for i in range(len(names)):
    box_office_urls.append(box.get_box_url(names[i], years[i]))

# Para cada filme, coleta informações monetárias e coloca no dataframe df_regional
flag = True
for film in box_office_urls:
    df_regional_temp = box.get_regional_info(film)
    # Caso seja a primeira iteração, cria os dataframes, caso contrário, contacena-os
    if flag:
        df_regional = df_regional_temp
        flag = False
        continue
    df_regional = pd.concat([df_regional, df_regional_temp], ignore_index=True)

# Troca o nome de "Domestic" para "United States" -> Box Office toma Domestic como os EUA, não o local de lançamento do filme
df_regional["Region"] = df_regional["Region"].str.replace("Domestic", "United States", regex=False).str.strip()

# Função que cria os arquivos csv com os dados e informações do filme
letter.create_xlsx(df_reviews, "reviews")
letter.create_xlsx(df_films, "movie_info")
letter.create_xlsx(df_regional, "regional_info")