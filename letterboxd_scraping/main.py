"""Módulo Principal"""

import pandas as pd
import letterboxd_bs4 as letter
import box_office_bs4 as box


# TODOS GENEROS:
"""genres = ["action", "adventure", "animation", "comedy", "crime", "drama",
          "family", "fantasy", "history", "horror", "music", "mystery", "romance",
          "science-fiction", "thriller", "war"]"""

genres = ["animation", "war", "science-fiction", "music"]

# Verificando se é o primeiro loop de genero.
flag_2 = True

for genre in genres:
    print(f"\nAveriguando gênero: {genre.capitalize()}")

    letterboxd_urls = letter.get_letterboxd_urls(genre)

    # Cria DataFrames vazios com as headers.
    headers_reviews = ["Username", "Date", "Score", "Review", "Length", "Movie"]
    headers_films = ['Name', 'Year', 'Director', 'Runtime (mins)', 'Mean', 'Standard Deviation', 'Summary', 
                    'Script', 'VFX', 'Casting', 'SFX', 'Editing', 'Directing', 'Keywords', 'Domestic',
                    'International', 'Worldwide', 'Domestic Oppening', 'Distributor', 'MPAA', 'Genre']
    df_reviews = pd.DataFrame(columns=headers_reviews)
    df_films = pd.DataFrame(columns=headers_films)

    # Para cada filme, coleta informações das reviews e do filme
    for film in letterboxd_urls:
        
        df_reviews_temp = letter.get_data_reviews(film, 5)
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
    # Coloca a coluna genre com o genero da iteração para filtrar no Excel
    df_regional["Genre"] = [genre for i in range(len(df_regional.index))]
    df_films["Genre"] = [genre for i in range(len(df_films.index))]
    df_reviews["Genre"] = [genre for i in range(len(df_reviews.index))]
    
    # Se for a primeira iteração (primeiro genero), cria os dfs, caso não, concatena-os no dataframe com todos generos
    if flag_2:
        df_regional_all = df_regional
        df_films_all = df_films
        df_reviews_all = df_reviews
        flag_2 = False
        continue
    df_regional_all = pd.concat([df_regional_all, df_regional], ignore_index=True)
    df_films_all = pd.concat([df_films_all, df_films], ignore_index=True)
    df_reviews_all = pd.concat([df_reviews_all, df_reviews], ignore_index=True)
    
    # Deleta coluna Genres (substituida por Genre)
    df_films_all = df_films_all.drop('Genres', axis=1)


# Função que cria os arquivos csv com os dados e informações do filme
letter.create_xlsx(df_reviews_all, "reviews")
letter.create_xlsx(df_films_all, "movie_info")
letter.create_xlsx(df_regional_all, "regional_info")
