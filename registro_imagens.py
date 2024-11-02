import mysql.connector  
from mysql.connector import Error  
import datetime  
  
def get_conexao():  
  try:  
    conexao = mysql.connector.connect(  
    host='localhost',  
    database='imagens',  
    user='gustavo',  
    password='Carmelita.1963'  
    )  
    return conexao  
  except Error as err:  
    print(f"Erro ao conectar ao banco de dados: {err}")  
    return None  
  
def fechar_conexao(conexao):  
  if conexao.is_connected():  
    conexao.close()  
  
def inserir_imagem(cursor, cnx, blob_data):  
  try:  
    data_registro = datetime.datetime.now()  
    cursor.execute("INSERT INTO imagens (imagem_blob, data_registro) VALUES (%s, %s)", (blob_data, data_registro))  
    cnx.commit()  
  except Error as err:  
    print(f"Erro ao inserir imagem: {err}")
