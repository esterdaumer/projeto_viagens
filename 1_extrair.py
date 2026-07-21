import zipfile
import os


# Arquivo ZIP dos dados
arquivo_zip = "data/viagens_2025_6meses (1).zip"

# Pasta onde os arquivos serão extraídos
pasta_destino = "data"


try:
    print("Iniciando extração...")

    with zipfile.ZipFile(arquivo_zip, "r") as zip_ref:
        zip_ref.extractall(pasta_destino)

    print("Arquivos extraídos com sucesso!")

    print("\nArquivos encontrados:")
    for arquivo in os.listdir(pasta_destino):
        print("-", arquivo)

except Exception as erro:
    print("Erro durante a extração:")
    print(erro)