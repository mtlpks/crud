import mysql
import mysql.connector
import os
import pandas as pd

os.chdir('C:\\Users\\Matheus\\Github\\repos\\crud')

conn = mysql.connector.connect(
    host='localhost',
    user='root',
    password='Mla205766*'
)
cur = conn.cursor(buffered=True)

cur.execute("""DROP DATABASE IF EXISTS CRUD""")
cur.execute("""CREATE DATABASE CRUD""")

conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="Mla205766*",
    database="CRUD"
)
curr = conn.cursor()
curr.execute("""CREATE TABLE marca
(idMarca INT AUTO_INCREMENT PRIMARY KEY, nomeMarca VARCHAR(50) UNIQUE)""")
curr.execute("""CREATE TABLE produto
(idProduto INT AUTO_INCREMENT PRIMARY KEY, nomeProduto VARCHAR(50), valor DOUBLE(10, 2), idMarca INT, porcLucro DOUBLE(10, 2), lucroPorItem DOUBLE(10, 2), CONSTRAINT marcaFK  FOREIGN KEY (idMarca) REFERENCES marca(idMarca))""")
curr.close()

def create(nome_produto, nome_marca, valor, porc_lucro):
    curr = conn.cursor(buffered=True)
    curr.execute("INSERT IGNORE INTO marca(nomeMarca) VALUES(%s)", (nome_marca, ))
    curr.execute("INSERT INTO produto(nomeProduto, idMarca, valor, porcLucro, lucroPorItem) VALUES (%s, (SELECT idMarca FROM marca WHERE nomeMarca = %s), %s, %s, (%s * (%s / 100)))", (nome_produto, nome_marca, valor, porc_lucro, valor, porc_lucro))
    print(f'Produto {nome_produto} da marca {nome_marca} inserido com sucesso.')
    curr.close()

def read(opcao, nome_a_pesquisar=None):
    curr = conn.cursor(buffered=True)
    if opcao == '1':
        query = "SELECT nomeProduto, valor, porcLucro marca.nomeMarca FROM produto LEFT JOIN marca ON produto.idMarca = marca.idMarca AND nomeProduto = %s"
        curr.execute(query, (nome_a_pesquisar, ))
    if opcao == '2':
        query = "SELECT nomeProduto, valor, porcLucro marca.nomeMarca FROM produto LEFT JOIN marca ON produto.idMarca = marca.idMarca AND nomeMarca = %s"
        curr.execute(query, (nome_a_pesquisar, ))
    else:
        query = "SELECT nomeProduto, valor, porcLucro, lucroPorItem, marca.nomeMarca FROM produto LEFT JOIN marca ON produto.idMarca = marca.idMarca"
    df = pd.read_sql(query, con=conn)
    df.columns = ['Nome do produto', 'Valor', 'Porcentagem de lucro', 'Lucro por unidade', 'Marca do produto']
    print(df.to_markdown())
    curr.close()

def update(opcao, value_to_search, new_value):
    curr = conn.cursor(buffered=True)
    if opcao == 1:
        curr.execute("UPDATE produto SET nomeProduto = %s WHERE nomeProduto = %s", (new_value, value_to_search))
    if opcao == 2:
        curr.execute("UPDATE produto SET valor = %s WHERE nomeProduto = %s", (new_value, value_to_search))
    if opcao == 3:
        curr.execute("INSERT IGNORE INTO marca(nomeMarca) VALUES(%s)", (new_value, ))
        curr.execute("UPDATE produto SET idMarca = (SELECT idMarca FROM marca WHERE nomeMarca = %s) WHERE nomeMarca = %s ", (new_value, value_to_search))

def delete(opcao, value_to_delete):
    curr = conn.cursor(buffered=True)
    if opcao == 1:
        curr.execute("DELETE FROM produto WHERE nomeProduto = %s", (value_to_delete, ))
    if opcao == 2:
        curr.execute("DELETE FROM produto WHERE idMarca = (SELECT idMarca FROM marca WHERE %s = nomeMarca)", (value_to_delete, ))
        curr.execute("DELETE FROM marca WHERE nomeMarca = %s", (value_to_delete, ))
create('Meia', 'Lupo', 8, 13)
create('Calcinha', 'Lupo', 8, 12)
read(3)
update(1, 'Meia', 'Cueca')
read(3)

