-- =============================================================================
-- 0_criar_banco.sql
-- Cria o banco de dados "transparencia" e as 8 tabelas do pipeline:
--   - 4 tabelas RAW  (cópia fiel do CSV, tudo VARCHAR, sem constraints)
--   - 4 tabelas SILVER (tipadas, com PK, FK e constraints extras)
-- Compatível com MySQL 8.x
-- =============================================================================

CREATE DATABASE IF NOT EXISTS transparencia
    CHARACTER SET utf8mb4
    COLLATE utf8mb4_unicode_ci;

USE transparencia;

-- Reexecução segura (idempotência do script de criação)
DROP TABLE IF EXISTS silver_trecho;
DROP TABLE IF EXISTS silver_passagem;
DROP TABLE IF EXISTS silver_pagamento;
DROP TABLE IF EXISTS silver_viagem;
DROP TABLE IF EXISTS raw_trecho;
DROP TABLE IF EXISTS raw_passagem;
DROP TABLE IF EXISTS raw_pagamento;
DROP TABLE IF EXISTS raw_viagem;

-- =============================================================================
-- CAMADA RAW
-- Todas as colunas VARCHAR, sem PK/FK/constraints, refletindo fielmente o CSV.
-- =============================================================================

CREATE TABLE raw_viagem (
    id_viagem                VARCHAR(30),
    num_proposta              VARCHAR(30),
    situacao                  VARCHAR(50),
    viagem_urgente             VARCHAR(10),
    justificativa_urgencia     VARCHAR(255),
    cod_orgao_superior         VARCHAR(20),
    nome_orgao_superior        VARCHAR(255),
    cod_orgao_solicitante      VARCHAR(20),
    nome_orgao_solicitante     VARCHAR(255),
    cpf_viajante               VARCHAR(20),
    nome_viajante              VARCHAR(255),
    cargo                      VARCHAR(255),
    funcao                     VARCHAR(255),
    descricao_funcao           VARCHAR(255),
    data_inicio                VARCHAR(20),
    data_fim                   VARCHAR(20),
    destinos                   VARCHAR(4000),
    motivo                     VARCHAR(4000),
    valor_diarias              VARCHAR(30),
    valor_passagens            VARCHAR(30),
    valor_devolucao            VARCHAR(30),
    valor_outros_gastos        VARCHAR(30)
) ENGINE=InnoDB;

CREATE TABLE raw_pagamento (
    id_viagem                 VARCHAR(30),
    num_proposta               VARCHAR(30),
    cod_orgao_superior          VARCHAR(20),
    nome_orgao_superior         VARCHAR(255),
    cod_orgao_pagador           VARCHAR(20),
    nome_orgao_pagador          VARCHAR(255),
    cod_ug_pagadora              VARCHAR(20),
    nome_ug_pagadora             VARCHAR(255),
    tipo_pagamento               VARCHAR(50),
    valor                        VARCHAR(30)
) ENGINE=InnoDB;

CREATE TABLE raw_passagem (
    id_viagem                 VARCHAR(30),
    num_proposta               VARCHAR(30),
    meio_transporte             VARCHAR(50),
    pais_origem_ida             VARCHAR(60),
    uf_origem_ida                VARCHAR(40),
    cidade_origem_ida            VARCHAR(80),
    pais_destino_ida             VARCHAR(60),
    uf_destino_ida                VARCHAR(40),
    cidade_destino_ida            VARCHAR(80),
    pais_origem_volta              VARCHAR(60),
    uf_origem_volta                 VARCHAR(40),
    cidade_origem_volta              VARCHAR(80),
    pais_destino_volta                VARCHAR(60),
    uf_destino_volta                   VARCHAR(40),
    cidade_destino_volta                VARCHAR(80),
    valor_passagem                      VARCHAR(30),
    taxa_servico                         VARCHAR(30),
    data_emissao                          VARCHAR(20),
    hora_emissao                           VARCHAR(20)
) ENGINE=InnoDB;

CREATE TABLE raw_trecho (
    id_viagem            VARCHAR(30),
    num_proposta          VARCHAR(30),
    sequencia_trecho       VARCHAR(20),
    origem_data             VARCHAR(20),
    origem_pais              VARCHAR(60),
    origem_uf                 VARCHAR(40),
    origem_cidade              VARCHAR(80),
    destino_data                 VARCHAR(20),
    destino_pais                  VARCHAR(60),
    destino_uf                     VARCHAR(40),
    destino_cidade                  VARCHAR(80),
    meio_transporte                  VARCHAR(50),
    numero_diarias                     VARCHAR(30),
    missao                               VARCHAR(10)
) ENGINE=InnoDB;

-- =============================================================================
-- CAMADA SILVER
-- Dados limpos e tipados, com PK, FK e constraints (NOT NULL / CHECK / UNIQUE).
-- =============================================================================

CREATE TABLE silver_viagem (
    id_viagem            VARCHAR(20)   NOT NULL,
    num_proposta          VARCHAR(20),
    situacao               VARCHAR(50),
    viagem_urgente          VARCHAR(5),
    cod_orgao_superior       VARCHAR(20),
    nome_orgao_superior       VARCHAR(255) NOT NULL,
    nome_viajante              VARCHAR(255),
    cargo                       VARCHAR(255),
    data_inicio                  DATE,
    data_fim                      DATE,
    destinos                      VARCHAR(4000),
    motivo                         VARCHAR(4000),
    valor_diarias                   DECIMAL(10,2) CHECK (valor_diarias >= 0),
    valor_passagens                  DECIMAL(10,2),
    valor_devolucao                   DECIMAL(10,2),
    valor_outros_gastos                DECIMAL(10,2),
    valor_total                          DECIMAL(12,2),
    duracao_dias                          INT,
    PRIMARY KEY (id_viagem)
) ENGINE=InnoDB;

CREATE TABLE silver_pagamento (
    id_pagamento          INT AUTO_INCREMENT,
    id_viagem               VARCHAR(20) NOT NULL,
    num_proposta              VARCHAR(20),
    nome_orgao_pagador          VARCHAR(255),
    nome_ug_pagadora              VARCHAR(255),
    tipo_pagamento                  VARCHAR(50) NOT NULL,
    valor                             DECIMAL(10,2) CHECK (valor >= 0),
    PRIMARY KEY (id_pagamento),
    FOREIGN KEY (id_viagem) REFERENCES silver_viagem(id_viagem)
) ENGINE=InnoDB;

CREATE TABLE silver_passagem (
    id_passagem           INT AUTO_INCREMENT,
    id_viagem               VARCHAR(20) NOT NULL,
    meio_transporte           VARCHAR(50),
    pais_origem_ida             VARCHAR(60),
    uf_origem_ida                 VARCHAR(40),
    cidade_origem_ida              VARCHAR(80),
    pais_destino_ida                 VARCHAR(60),
    uf_destino_ida                     VARCHAR(40),
    cidade_destino_ida                  VARCHAR(80),
    valor_passagem                       DECIMAL(10,2) CHECK (valor_passagem >= 0),
    taxa_servico                           DECIMAL(10,2) CHECK (taxa_servico >= 0),
    data_emissao                             DATE,
    PRIMARY KEY (id_passagem),
    FOREIGN KEY (id_viagem) REFERENCES silver_viagem(id_viagem)
) ENGINE=InnoDB;

CREATE TABLE silver_trecho (
    id_trecho             INT AUTO_INCREMENT,
    id_viagem                VARCHAR(20) NOT NULL,
    sequencia_trecho           INT,
    origem_data                  DATE,
    origem_uf                      VARCHAR(40),
    origem_cidade                    VARCHAR(80),
    destino_data                       DATE,
    destino_uf                           VARCHAR(40),
    destino_cidade                        VARCHAR(80),
    meio_transporte                        VARCHAR(50),
    numero_diarias                           DECIMAL(10,2) CHECK (numero_diarias >= 0),
    PRIMARY KEY (id_trecho),
    FOREIGN KEY (id_viagem) REFERENCES silver_viagem(id_viagem),
    UNIQUE (id_viagem, sequencia_trecho)
) ENGINE=InnoDB;
