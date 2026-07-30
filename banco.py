# banco.py

import mysql.connector

from config import DB_CONFIG


def conectar():
    """Cria a conexão com o banco de dados."""

    conexao = mysql.connector.connect(
        host=DB_CONFIG["host"],
        port=DB_CONFIG["port"],
        user=DB_CONFIG["user"],
        password=DB_CONFIG["password"],
        database=DB_CONFIG["database"]
    )

    return conexao


def executar(conexao, sql, parametros=None):
    """Executa um comando SQL."""

    cursor = conexao.cursor()

    try:
        cursor.execute(sql, parametros or ())
        conexao.commit()
    finally:
        cursor.close()


def inserir_em_lote(conexao, sql, dados):
    """Insere várias linhas no banco de uma vez."""

    if not dados:
        return

    cursor = conexao.cursor()

    try:
        cursor.executemany(sql, dados)
        conexao.commit()
    finally:
        cursor.close() 