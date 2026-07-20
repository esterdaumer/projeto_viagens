CREATE DATABASE IF NOT EXISTS viagens;

USE viagens;


-- TABELA PRINCIPAL DE VIAGENS

CREATE TABLE silver_viagem (
    id_viagem VARCHAR(20) PRIMARY KEY,
    nome_orgao_superior VARCHAR(255) NOT NULL,
    data_inicio DATE,
    data_fim DATE,
    destinos VARCHAR(4000),
    valor_diarias DECIMAL(10,2) CHECK(valor_diarias >= 0),
    valor_passagens DECIMAL(10,2),
    valor_devolucao DECIMAL(10,2),
    valor_outros_gastos DECIMAL(10,2),
    valor_total DECIMAL(12,2),
    duracao_dias INT
);


-- PAGAMENTOS

CREATE TABLE silver_pagamento (
    id_pagamento INT AUTO_INCREMENT PRIMARY KEY,
    id_viagem VARCHAR(20) NOT NULL,
    tipo_pagamento VARCHAR(50) NOT NULL,
    valor DECIMAL(10,2) CHECK(valor >= 0),

    FOREIGN KEY(id_viagem)
    REFERENCES silver_viagem(id_viagem)
);


-- PASSAGENS

CREATE TABLE silver_passagem (
    id_passagem INT AUTO_INCREMENT PRIMARY KEY,
    id_viagem VARCHAR(20) NOT NULL,
    meio_transporte VARCHAR(50),
    valor_passagem DECIMAL(10,2) CHECK(valor_passagem >= 0),
    taxa_servico DECIMAL(10,2) CHECK(taxa_servico >= 0),

    FOREIGN KEY(id_viagem)
    REFERENCES silver_viagem(id_viagem)
);


-- TRECHOS

CREATE TABLE silver_trecho (
    id_trecho INT AUTO_INCREMENT PRIMARY KEY,
    id_viagem VARCHAR(20) NOT NULL,
    destino_uf VARCHAR(40),
    meio_transporte VARCHAR(50),
    numero_diarias DECIMAL(10,2) CHECK(numero_diarias >= 0),

    UNIQUE(id_viagem),

    FOREIGN KEY(id_viagem)
    REFERENCES silver_viagem(id_viagem)
);