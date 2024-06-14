"""Módulo Principal"""

import sys
import letterboxd_bs4 as letterboxd

# Pega a url e a quantidade de páginas para analisar da linha de comando
try:
    url = sys.argv[1]
    # Valor padrão (todas) caso não seja um inteiro positivo ou seja vazio o argv[2].
    page_ammount = 0
    if len(sys.argv) >= 3:
        if int(sys.argv[2]) >= 1:
            page_ammount = int(sys.argv[2])
except:
    print("Erro de execução:")
    print("Uso: python main.py [url do filme] [paginas a ler] (opcional, padrão = todas)")
    exit()

# Função para pegar dataframe com dados
df = letterboxd.get_data(url, page_ammount)
# Função que cria o arquivo csv com os dados
letterboxd.create_csv(url, df)