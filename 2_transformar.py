# 2_transformar.py
#
# Camada SILVER:
# - lê as tabelas RAW em blocos
# - limpa textos
# - transforma números e datas
# - cria valor_total e duracao_dias
# - mantém integridade referencial entre as tabelas

from datetime import datetime

from banco import conectar, executar, inserir_em_lote


TAMANHO_BLOCO = 10000

TEXTOS_VAZIOS = [
    "",
    "sem informação",
    "sem informacao",
    "-1",
    "nan"
]


def texto_para_numero(texto):
    if texto is None:
        return None

    texto = str(texto).strip()

    if texto.lower() in TEXTOS_VAZIOS:
        return None

    try:
        texto = texto.replace(".", "").replace(",", ".")
        return float(texto)
    except ValueError:
        return None


def texto_para_data(texto):
    if texto is None:
        return None

    texto = str(texto).strip()

    if texto.lower() in TEXTOS_VAZIOS:
        return None

    try:
        return datetime.strptime(texto, "%d/%m/%Y").date()
    except ValueError:
        return None


def limpar_texto(texto):
    if texto is None:
        return None

    texto = str(texto).strip()

    if texto.lower() in TEXTOS_VAZIOS:
        return None

    return texto


def transformar_viagem(conexao):
    print("Transformando silver_viagem...")

    executar(conexao, "SET FOREIGN_KEY_CHECKS = 0;")
    executar(conexao, "TRUNCATE TABLE silver_viagem;")
    executar(conexao, "SET FOREIGN_KEY_CHECKS = 1;")

    # Conexão separada para leitura da RAW.
    # Isso evita o erro "Unread result found".
    conexao_leitura = conectar()
    cursor = conexao_leitura.cursor(dictionary=True)
    cursor.execute("SELECT * FROM raw_viagem")

    ids_validos = set()
    linhas_prontas = []
    total_lido = 0
    total_inserido = 0

    sql = """
        INSERT INTO silver_viagem (
            id_viagem,
            num_proposta,
            situacao,
            viagem_urgente,
            cod_orgao_superior,
            nome_orgao_superior,
            nome_viajante,
            cargo,
            data_inicio,
            data_fim,
            destinos,
            motivo,
            valor_diarias,
            valor_passagens,
            valor_devolucao,
            valor_outros_gastos,
            valor_total,
            duracao_dias
        )
        VALUES (
            %s,%s,%s,%s,%s,%s,%s,%s,%s,%s,
            %s,%s,%s,%s,%s,%s,%s,%s
        )
    """

    while True:
        bloco = cursor.fetchmany(TAMANHO_BLOCO)

        if not bloco:
            break

        total_lido += len(bloco)

        for linha in bloco:
            id_viagem = limpar_texto(linha["id_viagem"])
            nome_orgao = limpar_texto(linha["nome_orgao_superior"])

            if not id_viagem or not nome_orgao:
                continue

            if id_viagem in ids_validos:
                continue

            diarias = texto_para_numero(linha["valor_diarias"]) or 0
            passagens = texto_para_numero(linha["valor_passagens"]) or 0
            devolucao = texto_para_numero(linha["valor_devolucao"]) or 0
            outros_gastos = texto_para_numero(linha["valor_outros_gastos"]) or 0

            if diarias < 0:
                continue

            valor_total = round(
                diarias + passagens + outros_gastos - devolucao,
                2
            )

            data_inicio = texto_para_data(linha["data_inicio"])
            data_fim = texto_para_data(linha["data_fim"])

            duracao_dias = None

            if data_inicio and data_fim:
                duracao_dias = (data_fim - data_inicio).days + 1

            ids_validos.add(id_viagem)

            linhas_prontas.append((
                id_viagem,
                limpar_texto(linha["num_proposta"]),
                limpar_texto(linha["situacao"]),
                limpar_texto(linha["viagem_urgente"]),
                limpar_texto(linha["cod_orgao_superior"]),
                nome_orgao,
                limpar_texto(linha["nome_viajante"]),
                limpar_texto(linha["cargo"]),
                data_inicio,
                data_fim,
                limpar_texto(linha["destinos"]),
                limpar_texto(linha["motivo"]),
                diarias,
                passagens,
                devolucao,
                outros_gastos,
                valor_total,
                duracao_dias
            ))

        if len(linhas_prontas) >= TAMANHO_BLOCO:
            inserir_em_lote(conexao, sql, linhas_prontas)

            total_inserido += len(linhas_prontas)
            linhas_prontas = []

            print(
                f"  {total_inserido} linhas silver_viagem carregadas..."
            )

    if linhas_prontas:
        inserir_em_lote(conexao, sql, linhas_prontas)
        total_inserido += len(linhas_prontas)

    cursor.close()
    conexao_leitura.close()

    print(f"  RAW lida: {total_lido} linhas.")
    print(f"  silver_viagem pronta com {total_inserido} linhas.")

    return ids_validos


def transformar_pagamento(conexao, ids_validos):
    print("Transformando silver_pagamento...")

    executar(conexao, "TRUNCATE TABLE silver_pagamento;")

    conexao_leitura = conectar()
    cursor = conexao_leitura.cursor(dictionary=True)
    cursor.execute("SELECT * FROM raw_pagamento")

    total_lido = 0
    total_inserido = 0
    linhas_prontas = []

    sql = """
        INSERT INTO silver_pagamento (
            id_viagem,
            num_proposta,
            nome_orgao_pagador,
            nome_ug_pagadora,
            tipo_pagamento,
            valor
        )
        VALUES (%s,%s,%s,%s,%s,%s)
    """

    while True:
        bloco = cursor.fetchmany(TAMANHO_BLOCO)

        if not bloco:
            break

        total_lido += len(bloco)

        for linha in bloco:
            id_viagem = limpar_texto(linha["id_viagem"])

            if id_viagem not in ids_validos:
                continue

            tipo_pagamento = limpar_texto(linha["tipo_pagamento"])
            valor = texto_para_numero(linha["valor"])

            if not tipo_pagamento:
                continue

            if valor is None or valor < 0:
                continue

            linhas_prontas.append((
                id_viagem,
                limpar_texto(linha["num_proposta"]),
                limpar_texto(linha["nome_orgao_pagador"]),
                limpar_texto(linha["nome_ug_pagadora"]),
                tipo_pagamento,
                valor
            ))

        if len(linhas_prontas) >= TAMANHO_BLOCO:
            inserir_em_lote(conexao, sql, linhas_prontas)

            total_inserido += len(linhas_prontas)
            linhas_prontas = []

            print(
                f"  {total_inserido} linhas silver_pagamento carregadas..."
            )

    if linhas_prontas:
        inserir_em_lote(conexao, sql, linhas_prontas)
        total_inserido += len(linhas_prontas)

    cursor.close()
    conexao_leitura.close()

    print(f"  RAW lida: {total_lido} linhas.")
    print(f"  silver_pagamento pronta com {total_inserido} linhas.")


def transformar_passagem(conexao, ids_validos):
    print("Transformando silver_passagem...")

    executar(conexao, "TRUNCATE TABLE silver_passagem;")

    conexao_leitura = conectar()
    cursor = conexao_leitura.cursor(dictionary=True)
    cursor.execute("SELECT * FROM raw_passagem")

    total_lido = 0
    total_inserido = 0
    linhas_prontas = []

    sql = """
        INSERT INTO silver_passagem (
            id_viagem,
            meio_transporte,
            pais_origem_ida,
            uf_origem_ida,
            cidade_origem_ida,
            pais_destino_ida,
            uf_destino_ida,
            cidade_destino_ida,
            valor_passagem,
            taxa_servico,
            data_emissao
        )
        VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
    """

    while True:
        bloco = cursor.fetchmany(TAMANHO_BLOCO)

        if not bloco:
            break

        total_lido += len(bloco)

        for linha in bloco:
            id_viagem = limpar_texto(linha["id_viagem"])

            if id_viagem not in ids_validos:
                continue

            valor_passagem = texto_para_numero(
                linha["valor_passagem"]
            )

            taxa_servico = texto_para_numero(
                linha["taxa_servico"]
            ) or 0

            if valor_passagem is None or valor_passagem < 0:
                continue

            if taxa_servico < 0:
                continue

            linhas_prontas.append((
                id_viagem,
                limpar_texto(linha["meio_transporte"]),
                limpar_texto(linha["pais_origem_ida"]),
                limpar_texto(linha["uf_origem_ida"]),
                limpar_texto(linha["cidade_origem_ida"]),
                limpar_texto(linha["pais_destino_ida"]),
                limpar_texto(linha["uf_destino_ida"]),
                limpar_texto(linha["cidade_destino_ida"]),
                valor_passagem,
                taxa_servico,
                texto_para_data(linha["data_emissao"])
            ))

        if len(linhas_prontas) >= TAMANHO_BLOCO:
            inserir_em_lote(conexao, sql, linhas_prontas)

            total_inserido += len(linhas_prontas)
            linhas_prontas = []

            print(
                f"  {total_inserido} linhas silver_passagem carregadas..."
            )

    if linhas_prontas:
        inserir_em_lote(conexao, sql, linhas_prontas)
        total_inserido += len(linhas_prontas)

    cursor.close()
    conexao_leitura.close()

    print(f"  RAW lida: {total_lido} linhas.")
    print(f"  silver_passagem pronta com {total_inserido} linhas.")


def transformar_trecho(conexao, ids_validos):
    print("Transformando silver_trecho...")

    executar(conexao, "TRUNCATE TABLE silver_trecho;")

    conexao_leitura = conectar()
    cursor = conexao_leitura.cursor(dictionary=True)
    cursor.execute("SELECT * FROM raw_trecho")

    total_lido = 0
    total_inserido = 0
    linhas_prontas = []
    combinacoes_ja_usadas = set()

    sql = """
        INSERT INTO silver_trecho (
            id_viagem,
            sequencia_trecho,
            origem_data,
            origem_uf,
            origem_cidade,
            destino_data,
            destino_uf,
            destino_cidade,
            meio_transporte,
            numero_diarias
        )
        VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
    """

    while True:
        bloco = cursor.fetchmany(TAMANHO_BLOCO)

        if not bloco:
            break

        total_lido += len(bloco)

        for linha in bloco:
            id_viagem = limpar_texto(linha["id_viagem"])

            if id_viagem not in ids_validos:
                continue

            try:
                sequencia = int(
                    float(str(linha["sequencia_trecho"]).strip())
                )
            except (ValueError, TypeError):
                continue

            chave = (id_viagem, sequencia)

            if chave in combinacoes_ja_usadas:
                continue

            combinacoes_ja_usadas.add(chave)

            numero_diarias = texto_para_numero(
                linha["numero_diarias"]
            ) or 0

            if numero_diarias < 0:
                continue

            linhas_prontas.append((
                id_viagem,
                sequencia,
                texto_para_data(linha["origem_data"]),
                limpar_texto(linha["origem_uf"]),
                limpar_texto(linha["origem_cidade"]),
                texto_para_data(linha["destino_data"]),
                limpar_texto(linha["destino_uf"]),
                limpar_texto(linha["destino_cidade"]),
                limpar_texto(linha["meio_transporte"]),
                numero_diarias
            ))

        if len(linhas_prontas) >= TAMANHO_BLOCO:
            inserir_em_lote(conexao, sql, linhas_prontas)

            total_inserido += len(linhas_prontas)
            linhas_prontas = []

            print(
                f"  {total_inserido} linhas silver_trecho carregadas..."
            )

    if linhas_prontas:
        inserir_em_lote(conexao, sql, linhas_prontas)
        total_inserido += len(linhas_prontas)

    cursor.close()
    conexao_leitura.close()

    print(f"  RAW lida: {total_lido} linhas.")
    print(f"  silver_trecho pronta com {total_inserido} linhas.")


if __name__ == "__main__":
    conexao = conectar()

    try:
        ids_validos = transformar_viagem(conexao)

        transformar_pagamento(conexao, ids_validos)

        transformar_passagem(conexao, ids_validos)

        transformar_trecho(conexao, ids_validos)

        print("\nTransformação terminada com sucesso!")

    except Exception as erro:
        print(f"\nDeu erro durante a transformação: {erro}")

    finally:
        conexao.close()   