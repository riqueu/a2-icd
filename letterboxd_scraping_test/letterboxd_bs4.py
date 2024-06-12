"""Módulo da extração de dados com o Beautiful Soup"""

from bs4 import BeautifulSoup
import re
import requests
import pandas as pd
import functions as f

# URL da página do filme
url_base = "https://letterboxd.com/film/hermanoteu-in-the-land-of-godah/"

page_count = 1

headers = ["Username", "Score", "Review"] #dps... , "coiso legal", "outro coiso legal", "bleblebleh"]
df = pd.DataFrame(columns=headers)

while True:
    # Cada Iteração é uma pagina com várias reviews
    url_page = url_base + "reviews/page/" + str(page_count)
    page = requests.get(url_page)
    soup = BeautifulSoup(page.text, "lxml")
    
    page_data = []
    table = soup.find_all("li", class_="film-detail")
    
    print(f"Scanneando página {page_count}")
    for each_review in table:
        user_name = each_review.find(class_="name").text.strip()
        # Chama função em functions.py para conseguir o número da nota
        score = f.get_score(each_review.find(class_="attribution"))
        
        # Transforma div da review em string para trata-la
        review_div = str(each_review.find(class_="body-text -prose collapsible-text"))
        # Troca line breaks e paragrafos por um espaço e transforma de volta em um objeto do Beautiful Soup
        review_div_soup = BeautifulSoup(re.sub(r'<\/?p>|<br\s?\/?>', ' ', review_div), "lxml")
        review = review_div_soup.text.strip()
        # Se a review tiver o aviso de spoilers do Letterboxd, remove aviso (60 caracteres).
        spoilers_string = "This review may contain spoilers. I can handle the truth.   "
        if spoilers_string in review:
            review = review[60::]
        
        # Caso não haja username ou review
        if not user_name:
            user_name = "Unnamed"
        if not review:
            review = "Unreviewed"
        
        # Cria row_data e dá append dessa review na lista de reviews da pagina
        row_data = {'Username': user_name, 'Score': score, 'Review': review}
        page_data.append(row_data)
     
    # Cria o dataframe temporário com as reviews dessa pagina e o concatena no principal
    df_temp = pd.DataFrame(page_data, columns=headers)
    if not df.empty:
        # Evitar FutureWarning (p/ concatenação de dataframes vazios)
        df = pd.concat([df, df_temp], ignore_index=True)
    # Caso o df principal não exista ainda, coloca-o com as informações da primeira pagina
    else:
        df = df_temp
    
    # Se não há próxima página, quebra o loop. Caso haja, soma 1 no contador e itera novamente.
    if not soup.find("a", class_="next"):
        break
    page_count += 1

# Encontra o nome do filme na URL para criar o .csv
match = re.search(r"/film/([^/]+)/", url_base)
if match:
    film_name = match.group(1)
    # Troca - para _ para nomear o .csv
    film_name = re.sub(r"-", "_", film_name)

df.to_csv(f"dados_{film_name}.csv")
print(f"CSV criado em dados_{film_name}.csv!")
