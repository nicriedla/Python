# 01 - Exploração Inicial do Dataset

import pandas as pd

df = pd.read_csv('tmdb_5000_movies.csv')

print(df.head())
print(df.info())
print(df.describe())
print(df.isnull().sum())

df['release_date'] = pd.to_datetime(df['release_date'], errors='coerce')
print(df.dtypes)

# 02 - Top 10 Filmes por Receita

import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv('tmdb_5000_movies.csv')
top_10 = df.sort_values('revenue', ascending=False).head(10)

print(top_10[['title', 'budget', 'revenue']])

plt.figure(figsize=(12, 6))
plt.bar(top_10['title'], top_10['revenue'])
plt.xticks(rotation=45, ha='right')
plt.title('Top 10 Filmes por Receita')
plt.xlabel('Filme')
plt.ylabel('Receita')
plt.tight_layout()
plt.show()

# 03 - ROI (Retorno sobre Investimento)

import pandas as pd

df = pd.read_csv('tmdb_5000_movies.csv')
df = df[df['budget'] > 0]
df['roi'] = (df['revenue'] - df['budget']) / df['budget']

print(df[['title', 'roi']].sort_values(by='roi', ascending=False).head(10))

# 04 - Lançamentos por Ano

import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv('tmdb_5000_movies.csv')
df['release_date'] = pd.to_datetime(df['release_date'], errors='coerce')
df['year'] = df['release_date'].dt.year

count_by_year = df['year'].value_counts().sort_index()

count_by_year.plot(kind='line', figsize=(10, 6), title='Filmes lançados por ano')
plt.xlabel('Ano')
plt.ylabel('Quantidade de filmes')
plt.grid(True)
plt.show()

# 05 - Duração dos Filmes (Runtime)

import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv('tmdb_5000_movies.csv')

plt.hist(df['runtime'].dropna(), bins=30)
plt.title('Distribuição da Duração dos Filmes')
plt.xlabel('Minutos')
plt.ylabel('Frequência')
plt.show()

# 06 - Filmes Mais Populares e Mais Votados

import pandas as pd

df = pd.read_csv('tmdb_5000_movies.csv')

print("Top 10 por Popularidade:")
print(df[['title', 'popularity']].sort_values(by='popularity', ascending=False).head(10))

print("\nTop 10 por Número de Votos:")
print(df[['title', 'vote_count']].sort_values(by='vote_count', ascending=False).head(10))

# 07 - Média de Avaliação por Idioma

import pandas as pd

df = pd.read_csv('tmdb_5000_movies.csv')

avg_by_lang = df.groupby('original_language')['vote_average'].mean().sort_values(ascending=False)
print(avg_by_lang)

# 08 - Análise de Gêneros

import pandas as pd
import ast
from collections import Counter

df = pd.read_csv('tmdb_5000_movies.csv')
df['genres'] = df['genres'].apply(lambda x: [d['name'] for d in ast.literal_eval(x)] if pd.notnull(x) else [])

all_genres = sum(df['genres'], [])
genre_counts = Counter(all_genres)

print(genre_counts.most_common(10))

# 09 - Palavras-chave Mais Frequentes

import pandas as pd
import ast
from collections import Counter

df = pd.read_csv('tmdb_5000_movies.csv')
df['keywords'] = df['keywords'].apply(lambda x: [d['name'] for d in ast.literal_eval(x)] if pd.notnull(x) else [])

all_keywords = sum(df['keywords'], [])
keyword_counts = Counter(all_keywords)

print(keyword_counts.most_common(10))

# 10 - Produtoras Mais Ativas

import pandas as pd
import ast
from collections import Counter

df = pd.read_csv('tmdb_5000_movies.csv')
df['production_companies'] = df['production_companies'].apply(lambda x: [d['name'] for d in ast.literal_eval(x)] if pd.notnull(x) else [])

all_companies = sum(df['production_companies'], [])
company_counts = Counter(all_companies)

print(company_counts.most_common(10))

# 11 - Correlação entre Variáveis Numéricas

import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

df = pd.read_csv('tmdb_5000_movies.csv')

num_cols = ['budget', 'revenue', 'popularity', 'vote_average', 'vote_count']
corr = df[num_cols].corr()

sns.heatmap(corr, annot=True, cmap='coolwarm')
plt.title('Correlação entre Variáveis Numéricas')
plt.show()

# 12 - Países de Produção Mais Ativos

import pandas as pd
import ast
from collections import Counter

df = pd.read_csv('tmdb_5000_movies.csv')
df['production_countries'] = df['production_countries'].apply(lambda x: [d['name'] for d in ast.literal_eval(x)] if pd.notnull(x) else [])

all_countries = sum(df['production_countries'], [])
country_counts = Counter(all_countries)

print(country_counts.most_common(10))

# 13 - Taglines Mais Criativas

import pandas as pd

df = pd.read_csv('tmdb_5000_movies.csv')

df['tagline_len'] = df['tagline'].fillna('').apply(len)
print(df[['title', 'tagline', 'tagline_len']].sort_values(by='tagline_len', ascending=False).head(10))

# 14 - Orçamento vs Nota Média

import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv('tmdb_5000_movies.csv')
df = df[df['budget'] > 0]

plt.scatter(df['budget'], df['vote_average'])
plt.xlabel('Orçamento')
plt.ylabel('Nota Média')
plt.title('Orçamento vs Nota Média')
plt.xscale('log')
plt.show()

# 15 - Ranking Ponderado Estilo IMDb

import pandas as pd

df = pd.read_csv('tmdb_5000_movies.csv')

C = df['vote_average'].mean()
m = df['vote_count'].quantile(0.90)

qualified = df[df['vote_count'] >= m].copy()
qualified['score'] = qualified.apply(lambda x: (x['vote_count'] / (x['vote_count'] + m) * x['vote_average']) + (m / (m + x['vote_count']) * C), axis=1)

print(qualified[['title', 'vote_count', 'vote_average', 'score']].sort_values(by='score', ascending=False).head(10))