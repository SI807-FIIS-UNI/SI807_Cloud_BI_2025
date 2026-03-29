CREATE SCHEMA IF NOT EXISTS dw;

CREATE TABLE dw.dim_cliente
(
    cliente_sk BIGINT IDENTITY(1,1),  -- surrogate key

    -- copia todos los campos de staging.dim_cliente con sus tipos originales
    LIKE staging.dim_cliente
);