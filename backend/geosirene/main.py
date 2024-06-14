import psycopg2
from fastapi import FastAPI
from dotenv import load_dotenv
import os
import pandas as pd

load_dotenv()

'''
app = FastAPI()

@app.get("/")
def read_root():
    return {"Hello": "World"}

'''

db_settings = {
    'dbname': os.getenv('DATABASE'),
    'user': os.getenv('USER'),
    'password': os.getenv('PASSWORD'),
    'host': os.getenv('HOST')
}

# Conectar ao banco de dados
conn = psycopg2.connect(**db_settings)

print("conectado com sucesso")

# Criar um cursor
cursor = conn.cursor()

# Consulta SQL
consulta_sql = """
    SELECT
    p.comunidades as comunidade,
    p.locais_apoio as local_apoio,
    p.endereco as sirene_adress,
    b.nome as bairro,
    ST_AsText(p.geometry) as geom_pontos,
    ST_AsText(b.geom) as geom_bairros
FROM
    pontos_de_apoio2 p
JOIN
    bairros b ON ST_Within(p.geometry, b.geom)
WHERE
    b.nome <> 'Centro' and  b.nome <> 'Sepetiba';
"""

# Executar a consulta
cursor.execute(consulta_sql)

# Recuperar os resultados
resultados = cursor.fetchall()

# Fechar a conexão
cursor.close()
conn.close()

# Criar um DataFrame do Pandas com os resultados
df = pd.DataFrame(resultados, columns=['Comunidade', 'Local de Apoio', 'Endereço', 'Bairro', 'GeomPontos', 'GeomBairros'])

print('Dataframe criado com sucesso')

print(df)



'''
vendas = {
    1: {"item": "lata", "preco_unitario": 4, "quantidade": 5},
    2: {"item": "garrafa 2L", "preco_unitario": 15, "quantidade": 5},
    3: {"item": "garrafa 750ml", "preco_unitario": 10, "quantidade": 5},
    4: {"item": "lata mini", "preco_unitario": 2, "quantidade": 5},
}

@app.get("/")
def home():
    return {"vendas":len(vendas)}

'''