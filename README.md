# Analise de Dados: Letterboxd e Box Office
Trabalho 02 de Introdução à Ciência de Dados - Análise de Avaliações e Comentários.

## Grupo:
- [Carlos Daniel de Souza Lima](https://github.com/G4me0ver23)
- [Henrique Coelho Beltrão](https://github.com/riqueu)
- [Jaime Willian Carneiro da Silva](https://github.com/JaimeWillianCarneiro)
- [Luís Filipe Novaes de Souza](https://github.com/Filipe-Novaes)
- [Walléria Simões Correia](https://github.com/WalleriaSimoes)

# Resumo

Realizamos o scrapping de dados do site [Letterboxd](https://letterboxd.com/) (para coletar reviews de usuários) e [Box Office](https://www.boxofficemojo.com/) (para coletar informações monetárias dos filmes). Coletando 10 páginas de reviews para cada filme, 5 filmes para cada gênero de filme, e 16 gêneros no total. (80 filmes)

# Excel

### Peça 1:

Informações sobre os filmes mais populares de cada gênero no Letterboxd. Com uma analise sobre a relação entre bilheteria e avaliações dos usuários para esses filmes e um gráfico com a quantidade filmes populares lançados por ano.

### Peça 2:

Visualização da bilheteria regional (coletada no Box Office), com um mapa apresentando a bilheteria por país dado filme e gênero. Além de uma sinópse do filme, gerada pela API do ChatGPT com base nas análises de usuários coletadas no Letterboxd.

### Peça 3:

Análise de critérios avaliativos (ex: Efeitos Visuais) entre diferentes gêneros, apontando a importância de cada critério para certos tipos de filme. Cada critério recebeu uma nota, gerada pela API do ChatGPT com base nas reviews feitas no Letterboxd sobre o filme.

Além de um gráfico apresentando a distribuição das notas (atribuidas às reviews coletadas) dos filmes mais populares do site.


---


### Bibliotecas Usadas:

Utilizamos as seguintes bibliotecas:
- bs4
- pandas
- requests
- re
- datetime
- openai
- os
- dotenv
