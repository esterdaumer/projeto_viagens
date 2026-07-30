# 1_extrair.py
#
# Esse script faz a parte 1 do trabalho (camada RAW):
# - baixa o zip com os dados do Google Drive
# - abre o zip e pega os 4 arquivos CSV de dentro
# - le cada CSV e joga os dados dentro das tabelas raw_* do banco
#
# Não mexo no conteúdo dos dados aqui, só copio pro banco do jeito que veio.

import zipfile
import pandas as pd
import requests

from config import PASTA_DADOS, ARQUIVOS, DRIVE_FILE_ID, TAMANHO_BLOCO, CSV_SEPARADOR, CSV_ENCODING
from banco import conectar, executar, inserir_em_lote


# --- passo 1: baixar o zip do Google Drive -----------------------------

def baixar_zip(id_arquivo, caminho_para_salvar):
    print("Baixando o arquivo do Google Drive...")

    link = "https://docs.google.com/uc?export=download"
    sessao = requests.Session()

    resposta = sessao.get(link, params={"id": id_arquivo}, stream=True)

    # o Drive as vezes pede uma confirmação pra arquivos grandes
    token = None
    for nome_cookie, valor_cookie in sessao.cookies.items():
        if nome_cookie.startswith("download_warning"):
            token = valor_cookie

    if token:
        resposta = sessao.get(link, params={"id": id_arquivo, "confirm": token}, stream=True)

    caminho_para_salvar.parent.mkdir(parents=True, exist_ok=True)

    with open(caminho_para_salvar, "wb") as arquivo:
        for pedaco in resposta.iter_content(chunk_size=32768):
            arquivo.write(pedaco)

    print("Download concluído!")


# --- passo 2: extrair o zip ---------------------------------------------

def extrair_zip(caminho_zip, pasta_destino):
    print("Extraindo o zip...")
    with zipfile.ZipFile(caminho_zip, "r") as zip_ref:
        zip_ref.extractall(pasta_destino)
    print("Extração concluída!")


# --- passo 3: carregar um CSV numa tabela raw ---------------------------

def carregar_csv(conexao, caminho_csv, nome_tabela):
    print(f"\nCarregando {caminho_csv.name} na tabela {nome_tabela}...")

    # limpa a tabela antes de carregar de novo (assim não duplica se rodar 2x)
    executar(conexao, f"TRUNCATE TABLE {nome_tabela};")

    linhas_lidas = 0

    # le o csv em pedacos, porque o arquivo é grande
    pedacos = pd.read_csv(
        caminho_csv,
        sep=CSV_SEPARADOR,
        encoding=CSV_ENCODING,
        dtype=str,
        keep_default_na=False,
        chunksize=TAMANHO_BLOCO,
    )

    for pedaco in pedacos:
        # tira espaço extra do nome das colunas (o csv de Trecho vem com espaço sobrando)
        pedaco.columns = [coluna.strip() for coluna in pedaco.columns]

        marcadores = ", ".join(["%s"] * len(pedaco.columns))
        sql = f"INSERT INTO {nome_tabela} VALUES ({marcadores})"

        lista_de_linhas = [tuple(linha) for linha in pedaco.itertuples(index=False, name=None)]
        inserir_em_lote(conexao, sql, lista_de_linhas)

        linhas_lidas += len(lista_de_linhas)
        print(f"  {linhas_lidas} linhas carregadas...")

    print(f"Pronto! {nome_tabela} ficou com {linhas_lidas} linhas.")


# --- programa principal --------------------------------------------------

if __name__ == "__main__":

    caminho_do_zip = PASTA_DADOS / "viagens_2025_6meses.zip"

    # verifica se os 4 CSVs já estão soltos na pasta data/
    # (nesse caso, não precisa baixar nem extrair nada)
    csvs_ja_existem = all(
        (PASTA_DADOS / item["csv"]).exists() for item in ARQUIVOS.values()
    )

    try:
        if csvs_ja_existem:
            print("Os 4 CSVs já estão na pasta data/, não vou baixar nem extrair nada.")
        else:
            # se o zip já estiver na pasta data/, não precisa baixar de novo
            if not caminho_do_zip.exists():
                baixar_zip(DRIVE_FILE_ID, caminho_do_zip)
            else:
                print("O zip já está na pasta data/, não vou baixar de novo.")

            extrair_zip(caminho_do_zip, PASTA_DADOS)

        conexao = conectar()

        # carrega os 4 csvs, um de cada vez
        for item in ARQUIVOS.values():
            caminho_csv = PASTA_DADOS / item["csv"]
            carregar_csv(conexao, caminho_csv, item["tabela_raw"])

        conexao.close()
        print("\nExtração terminada com sucesso!")

    except Exception as erro:
        print(f"\nDeu erro durante a extração: {erro}")