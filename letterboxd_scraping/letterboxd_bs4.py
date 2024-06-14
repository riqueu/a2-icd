"""Módulo da extração de dados com o Beautiful Soup"""

from bs4 import BeautifulSoup
import re
import requests
import pandas as pd
import functions_scrapping as f

def get_data(url, pages = 0):
    # Atribui o input a variaveis locais
    url_base = url
    page_ammount = pages
    page_count = 1

    headers = ["Username", "Date", "Score", "Review"] #dps..., "coiso legal", "outro coiso legal", "bleblebleh"]
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
            row_data = {'Username': user_name, 'Date': date, 'Score': score, 'Review': review}
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
            break
        page_count += 1
    
    # Remove linhas não avaliadas ou que a data não é accessível
    df = df[df["Score"] != "Unrated"]
    df = df[df["Date"]  != "Date Not Accessible"]
    # Cria a Coluna da diferença entre elemento e média e arredonda para 2 casas decimais
    df["Deviation from the Mean"] = abs(df["Score"] - df["Score"].mean())
    df['Deviation from the Mean'] = df['Deviation from the Mean'].astype(float).round(2)
    
    return df

def create_csv(url, df):
    # Encontra o nome do filme na URL para criar o .csv
    match = re.search(r"/film/([^/]+)/", url)
    if match:
        film_name = match.group(1)
        # Troca - para _ para nomear o .csv
        film_name = re.sub(r"-", "_", film_name)

    df.to_csv(f"dados_{film_name}.csv")
    print(f"CSV criado em dados_{film_name}.csv!")