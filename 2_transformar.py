import pandas as pd
import os


pasta = "data"

try:
    print("Iniciando transformação...")

    arquivos = [
        "2025_Viagem.csv",
        "2025_Pagamento.csv",
        "2025_Passagem.csv",
        "2025_Trecho.csv"
    ]

    for arquivo in arquivos:
        caminho = os.path.join(pasta, arquivo)

        df = pd.read_csv(
            caminho,
            sep=";",
            encoding="latin-1",
            decimal=",",
            low_memory=False
        )

        print(f"\n{arquivo}")
        print("Linhas:", len(df))
        print(df.head())

    print("\nTransformação concluída!")

except Exception as erro:
    print("Erro:")
    print(erro)