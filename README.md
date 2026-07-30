# 📊 Análise de Dados com Python — Viagens a Serviço

## Sobre o Projeto

Este projeto foi desenvolvido para a disciplina de **Análise de Dados com Python**, utilizando dados públicos de **Viagens a Serviço do Portal da Transparência do Governo Federal**.

A proposta foi construir um fluxo completo de dados, desde a extração dos arquivos disponibilizados em CSV até o tratamento, organização, análise e apresentação dos resultados.

Durante o desenvolvimento foram utilizados **Python, Pandas, SQL, MySQL e Matplotlib**, seguindo uma organização em camadas **RAW, SILVER e GOLD**.

---

## 🎯 Objetivo

O principal objetivo do projeto foi transformar uma grande quantidade de dados brutos em informações organizadas e úteis para análise.

A partir dos dados foram desenvolvidas perguntas de negócio relacionadas a:

* Gastos dos órgãos públicos;
* Custos médios das viagens;
* Duração das viagens;
* Tipos de pagamento;
* Meios de transporte;
* Destinos e UFs mais frequentes.

---

## 🛠️ Tecnologias utilizadas

* Python
* Pandas
* SQL
* MySQL
* Jupyter Notebook
* Matplotlib

---

## 📁 Estrutura do Projeto

```text
projeto_viagens/

├── 0_criar_banco.sql
├── 1_extrair.py
├── 2_transformar.py
├── 3_gold.py
├── 3_analise.ipynb
├── banco.py
├── config.py
├── .env.example
├── requirements.txt
├── README.md
│
└── data/
    ├── 2025_Viagem.csv
    ├── 2025_Pagamento.csv
    ├── 2025_Passagem.csv
    └── 2025_Trecho.csv
```

---

## 🔄 Pipeline de dados

O projeto foi desenvolvido em etapas, seguindo uma estrutura semelhante à arquitetura **Medallion**.

### 1. Criação do banco — `0_criar_banco.sql`

Este arquivo cria o banco de dados e as tabelas utilizadas no projeto.

São criadas quatro tabelas na camada RAW e quatro tabelas na camada SILVER, com seus respectivos relacionamentos e tipos de dados.

### 2. Extração — `1_extrair.py`

Nesta etapa são lidos os arquivos disponibilizados em formato CSV e os dados são carregados para as tabelas da camada **RAW**.

A camada RAW mantém os dados próximos ao formato original, servindo como base para as etapas seguintes.

### 3. Transformação — `2_transformar.py`

Nesta etapa os dados passam por tratamentos utilizando Python e Pandas.

Entre as atividades realizadas estão:

* Organização dos dados;
* Limpeza e tratamento das informações;
* Conversão e padronização de tipos;
* Preparação dos dados para análise;
* Carregamento dos dados tratados na camada **SILVER**.

### 4. Camada GOLD — `3_gold.py`

Depois do tratamento dos dados, foram criadas tabelas agregadas na camada **GOLD**, preparadas para facilitar análises e geração de indicadores.

Foram criadas:

* `gold_orgao`
* `gold_transporte`
* `gold_mensal`

### 5. Análise — `3_analise.ipynb`

No notebook foram realizadas consultas SQL utilizando os dados tratados e agregados.

Foram desenvolvidas **6 perguntas de negócio**, com tabelas e gráficos para facilitar a interpretação dos resultados.

As análises abordaram:

1. Os órgãos com maior custo total;
2. Os destinos com maior custo médio por viagem;
3. A viagem com maior duração e seu custo;
4. Os tipos de pagamento com maior valor médio;
5. Os meios de transporte mais utilizados;
6. As UFs de destino que aparecem com maior frequência.

---

## 📌 Organização das camadas

### RAW

Armazena os dados brutos, mantendo as informações próximas ao formato disponibilizado pela fonte.

### SILVER

Armazena os dados tratados, organizados e tipados, deixando as informações mais adequadas para consultas e análises.

### GOLD

Armazena informações agregadas e indicadores preparados para facilitar a análise dos dados.

---

## 📊 Principais resultados

A análise permitiu identificar alguns resultados relevantes.

O **Ministério da Justiça e Segurança Pública** apresentou o maior custo total entre os órgãos analisados, com aproximadamente **R$ 486,9 milhões** registrados na camada SILVER.

Na análise das passagens, o **transporte aéreo** apresentou forte predominância, com **160.578 registros**, enquanto os transportes rodoviário e fluvial apresentaram quantidades significativamente menores.

Também foi identificada uma viagem com duração de **384 dias**, pertencente ao Ministério da Previdência Social, com valor total registrado de **R$ 0,00**. Esse resultado demonstra a importância de analisar os dados com atenção, pois alguns registros podem apresentar situações que precisam de uma verificação mais detalhada.

Os demais resultados podem ser consultados no notebook `3_analise.ipynb`, onde estão disponíveis as tabelas, gráficos e análises realizadas.

---

## ▶️ Como executar

### Instalar as dependências

```bash
pip install -r requirements.txt
```

### Criar o banco

Executar o arquivo:

```text
0_criar_banco.sql
```

### Extrair os dados

```bash
python 1_extrair.py
```

### Transformar os dados

```bash
python 2_transformar.py
```

### Criar a camada GOLD

```bash
python 3_gold.py
```

### Realizar as análises

Abrir o arquivo:

```text
3_analise.ipynb
```

---

## 💭 Minha experiência com o projeto

Desenvolver este projeto foi uma experiência importante para colocar em prática os conhecimentos que fui aprendendo durante o curso. No início, algumas partes pareceram bastante confusas, principalmente a organização do banco de dados, as consultas SQL e a separação entre as camadas **RAW, SILVER e GOLD**.

Durante o desenvolvimento, também encontrei alguns erros e precisei entender o que estava acontecendo para conseguir corrigi-los. Isso acabou sendo uma das partes mais importantes do aprendizado, porque percebi que um projeto de dados nem sempre funciona de primeira e que entender e resolver os problemas também faz parte do processo.

Ao longo do projeto, fui entendendo melhor a função de cada etapa. Os dados começam de uma forma mais bruta, passam por tratamentos e organização e, depois, podem ser utilizados para gerar análises e informações mais fáceis de interpretar.

Uma das partes que mais me chamou atenção foi poder visualizar os resultados depois de trabalhar com uma quantidade tão grande de dados. Ver as tabelas e os gráficos sendo gerados fez com que todo o processo de programação, SQL e tratamento dos dados fizesse mais sentido.

No final, considero que o projeto me ajudou não apenas a praticar **Python, Pandas, SQL e MySQL**, mas também a desenvolver mais autonomia para identificar erros, testar soluções e entender o caminho que os dados percorrem até chegar a uma análise.

Apesar das dificuldades encontradas durante o desenvolvimento, fiquei satisfeita com o resultado, principalmente por conseguir acompanhar o projeto desde os dados brutos até a criação das análises e dos resultados finais. Foi uma experiência que me ajudou a entender melhor, na prática, como funciona um projeto completo de análise de dados.
