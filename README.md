# 📊 Análise de Dados com Python - Viagens a Serviço

## Contextualização

Este projeto tem como objetivo transformar dados públicos de Viagens a Serviço do Portal da Transparência do Governo Federal em informações organizadas e úteis para análise.

Os dados disponibilizados originalmente possuem grande volume e necessitam passar por etapas de extração, tratamento e análise para gerar informações confiáveis para tomada de decisão.

## Objetivo do Projeto

Construir um pipeline de dados utilizando Python e SQL, seguindo a arquitetura Medallion, realizando as etapas de extração, armazenamento dos dados brutos, tratamento e geração de análises.

O projeto busca responder perguntas de negócio relacionadas aos gastos públicos com viagens, como:

- Quais são os 5 órgãos com maior custo total?
- Quais são os 3 destinos com maior custo médio por viagem?
- Qual foi a viagem de maior duração e seu custo total?
- Qual tipo de pagamento possui maior valor médio?
- Qual meio de transporte é mais utilizado nos trechos?
- Qual UF de destino aparece em mais trechos?
- Qual órgão realizou o maior gasto total?

## Tecnologias Utilizadas

- Python
- Pandas
- SQL
- MySQL/PostgreSQL
- Jupyter Notebook

## Arquitetura do Projeto

O projeto segue a arquitetura Medallion, organizada em três camadas:

### Raw

Camada responsável pelo armazenamento dos dados originais extraídos dos arquivos CSV, mantendo as informações sem alterações para garantir rastreabilidade.

Tabelas:

- raw_viagem
- raw_pagamento
- raw_passagem
- raw_trecho


### Silver

Camada responsável pelo tratamento e organização dos dados.

Nesta etapa são realizadas:

- Conversão de tipos de dados;
- Tratamento de datas;
- Conversão de valores numéricos;
- Criação de chaves primárias e estrangeiras;
- Aplicação de constraints para garantir integridade dos dados.

Tabelas:

- silver_viagem
- silver_pagamento
- silver_passagem
- silver_trecho


### Gold

Camada destinada às análises de negócio, utilizando consultas SQL, agregações e visualizações gráficas para gerar informações estratégicas.

## Estrutura do Projeto
projeto_viagens/

├── 0_criar_banco.sql
├── 1_extrair.py
├── 2_transformar.py
├── 3_analise.ipynb
├── banco.py
├── config.py
├── .env.example
├── requirements.txt
├── README.md
│
└── data/


## Etapas de Desenvolvimento

### 1 - Extração dos Dados

Foi realizada a extração automatizada dos dados disponibilizados em formato ZIP.

O processo realiza:

- Leitura dos arquivos CSV;
- Preservação dos dados originais;
- Tratamento de exceções para evitar falhas durante a execução.


### 2 - Transformação dos Dados

Nesta etapa os dados passam pelo processo de limpeza e preparação.

Foram realizadas:

- Leitura dos arquivos CSV utilizando Pandas;
- Padronização dos dados;
- Conversão de formatos;
- Preparação para carregamento na camada Silver.


### 3 - Análise dos Dados

Na camada Gold são realizadas análises utilizando SQL e Python para responder perguntas de negócio e gerar visualizações.

## Como Executar o Projeto

Instale as dependências:
  
  pip install -r requirements.txt

  
Execute a extração dos dados:

python 1_extrair.py

Execute as análises:
python 2_transformar.py

Execute as análises:
3_analise.ipynb

## Resultados Esperados

Ao final do pipeline, os dados brutos do Portal da Transparência são transformados em informações organizadas, permitindo análises sobre gastos, órgãos, destinos, pagamentos e transportes relacionados às viagens a serviço.

## Conclusão

O desenvolvimento deste projeto permitiu aplicar conceitos de Engenharia e Análise de Dados, utilizando técnicas de ETL, tratamento de dados, modelagem relacional e análise exploratória.

Através do pipeline construído, dados públicos em grande volume são transformados em informações mais claras e úteis para apoio à tomada de decisão. 
