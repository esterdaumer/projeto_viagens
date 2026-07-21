# 📊 Análise de Dados com Python - Viagens a Serviço

## Sobre o Projeto

Este projeto foi desenvolvido para a disciplina de **Análise de Dados com Python** e tem como objetivo trabalhar com dados públicos de **Viagens a Serviço do Portal da Transparência do Governo Federal**.

A proposta foi organizar dados brutos, realizar tratamentos necessários e preparar as informações para análises, utilizando conceitos de **ETL (Extração, Transformação e Análise de Dados)**.

O projeto utiliza Python, SQL e banco de dados para transformar informações desorganizadas em dados mais preparados para gerar insights.

---

# 🎯 Objetivo

O objetivo principal foi criar um fluxo de dados onde fosse possível:

* Extrair os dados disponibilizados em arquivos CSV;
* Organizar e preparar as informações;
* Realizar tratamentos nos dados;
* Estruturar o banco de dados;
* Desenvolver análises utilizando Python e SQL.

Com isso, o projeto busca responder perguntas relacionadas aos gastos públicos com viagens, como:

* Quais órgãos possuem maiores gastos?
* Quais destinos apresentam maiores custos?
* Qual viagem teve maior duração?
* Quais tipos de pagamento possuem maiores valores?
* Quais meios de transporte são mais utilizados?

---

# 🛠️ Tecnologias Utilizadas

* Python
* Pandas
* SQL
* MySQL/PostgreSQL
* Jupyter Notebook
* Git e GitHub

---

# 📂 Estrutura do Projeto

O projeto foi organizado seguindo uma sequência de execução:

```
projeto_viagens/

├── 0_criar_banco.sql
├── 1_extrair.py
├── 2_transformar.py
├── 3_analise.ipynb
├── banco.py
├── config.py
├── .env.example
├── requirements.txt
└── README.md
```

---

# 🔄 Processos do Projeto

## 0_criar_banco.sql

Este arquivo é responsável pela criação da estrutura do banco de dados.

Nele são definidas as tabelas utilizadas no projeto e a organização necessária para armazenar os dados.

---

## banco.py

Responsável pela conexão com o banco de dados.

Ele possui as configurações necessárias para que os scripts Python consigam acessar e trabalhar com as informações armazenadas.

---

## config.py

Arquivo destinado às configurações do projeto.

Ele centraliza informações utilizadas pelos scripts, facilitando a organização do código.

---

## 1_extrair.py - Extração dos Dados

Nesta etapa acontece a primeira parte do pipeline.

O processo realiza a extração dos arquivos disponibilizados em formato ZIP e prepara os dados para serem utilizados nas próximas etapas.

Principais atividades:

* Leitura dos arquivos;
* Extração dos dados;
* Organização inicial das informações.

---

## 2_transformar.py - Tratamento dos Dados

Nesta etapa os dados passam por uma preparação utilizando Python e Pandas.

São realizadas atividades como:

* Leitura dos arquivos CSV;
* Organização das informações;
* Padronização dos dados;
* Preparação para utilização no banco.

Essa etapa tem como objetivo deixar os dados mais adequados para análise.

---

## 3_analise.ipynb - Análise dos Dados

O notebook é utilizado para explorar os dados e gerar análises.

Nesta etapa são realizadas:

* Consultas;
* Análises exploratórias;
* Criação de gráficos;
* Interpretação dos resultados encontrados.

O objetivo é transformar os dados tratados em informações que possam auxiliar na tomada de decisão.

---

# 📌 Organização dos Dados

O projeto segue o conceito da arquitetura Medallion:

## Raw

Representa os dados originais, mantendo as informações próximas ao formato disponibilizado pela fonte.

## Silver

Representa os dados organizados e preparados após os tratamentos necessários.

## Gold

Representa a etapa de análise, onde os dados são utilizados para gerar informações e indicadores.

---

# ▶️ Como Executar

Instalar as dependências:

```bash
pip install -r requirements.txt
```

Executar a extração:

```bash
python 1_extrair.py
```

Executar a transformação:

```bash
python 2_transformar.py
```

Executar as análises:

Abrir o arquivo:

```
3_analise.ipynb
```

---

# ✅ Conclusão

Este projeto possibilitou aplicar conhecimentos de análise de dados, tratamento de informações, banco de dados e programação em Python.

Através do desenvolvimento do pipeline, foi possível organizar dados públicos de viagens e preparar as informações para análises mais claras e eficientes.
