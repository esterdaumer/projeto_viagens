# 3_gold.py
#
# Camada GOLD:
# Cria tabelas resumidas para responder às perguntas de negócio.

from banco import conectar, executar


def criar_gold(conexao):
    print("Criando camada GOLD...")

    # ---------------------------------------------------------
    # GOLD 1 - gastos por órgão
    # ---------------------------------------------------------
    executar(conexao, "DROP TABLE IF EXISTS gold_orgao")

    executar(conexao, """
        CREATE TABLE gold_orgao AS
        SELECT
            nome_orgao_superior,
            COUNT(*) AS quantidade_viagens,
            ROUND(SUM(valor_total), 2) AS gasto_total,
            ROUND(AVG(valor_total), 2) AS gasto_medio
        FROM silver_viagem
        GROUP BY nome_orgao_superior
        ORDER BY gasto_total DESC
    """)

    print("  gold_orgao criada.")

    # ---------------------------------------------------------
    # GOLD 2 - gastos por meio de transporte
    # ---------------------------------------------------------
    executar(conexao, "DROP TABLE IF EXISTS gold_transporte")

    executar(conexao, """
        CREATE TABLE gold_transporte AS
        SELECT
            meio_transporte,
            COUNT(*) AS quantidade_passagens,
            ROUND(SUM(valor_passagem), 2) AS valor_total_passagens,
            ROUND(AVG(valor_passagem), 2) AS valor_medio_passagem
        FROM silver_passagem
        GROUP BY meio_transporte
        ORDER BY valor_total_passagens DESC
    """)

    print("  gold_transporte criada.")

    # ---------------------------------------------------------
    # GOLD 3 - gastos por mês
    # ---------------------------------------------------------
    executar(conexao, "DROP TABLE IF EXISTS gold_mensal")

    executar(conexao, """
        CREATE TABLE gold_mensal AS
        SELECT
            YEAR(data_inicio) AS ano,
            MONTH(data_inicio) AS mes,
            COUNT(*) AS quantidade_viagens,
            ROUND(SUM(valor_total), 2) AS gasto_total,
            ROUND(AVG(valor_total), 2) AS gasto_medio
        FROM silver_viagem
        WHERE data_inicio IS NOT NULL
        GROUP BY YEAR(data_inicio), MONTH(data_inicio)
        ORDER BY ano, mes
    """)

    print("  gold_mensal criada.")

    print("\nCamada GOLD criada com sucesso!")


if __name__ == "__main__":
    conexao = conectar()

    try:
        criar_gold(conexao)
    except Exception as erro:
        print(f"\nDeu erro ao criar GOLD: {erro}")
    finally:
        conexao.close() 