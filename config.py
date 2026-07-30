import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

DB_CONFIG = {
    "host": os.getenv("DB_HOST"),
    "port": os.getenv("DB_PORT"),
    "user": os.getenv("DB_USER"),
    "password": os.getenv("DB_PASSWORD"),
    "database": os.getenv("DB_NAME")
}

PASTA_DADOS = Path(__file__).resolve().parent / "data"

ARQUIVOS = {
    "viagem": {
        "csv": "2025_Viagem.csv",
        "tabela_raw": "raw_viagem"
    },
    "pagamento": {
        "csv": "2025_Pagamento.csv",
        "tabela_raw": "raw_pagamento"
    },
    "passagem": {
        "csv": "2025_Passagem.csv",
        "tabela_raw": "raw_passagem"
    },
    "trecho": {
        "csv": "2025_Trecho.csv",
        "tabela_raw": "raw_trecho"
    }
}

DRIVE_FILE_ID = ""
TAMANHO_BLOCO = 10000
CSV_SEPARADOR = ";"
CSV_ENCODING = "latin1"