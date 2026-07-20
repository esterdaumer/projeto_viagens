import mysql.connector

conexao = mysql.connector.connect(
    host="localhost",
    port=3307,
    user="root",
    password="Projeto2026!",
    database="viagens"
)

print("Conexão com MySQL realizada com sucesso!")

conexao.close()