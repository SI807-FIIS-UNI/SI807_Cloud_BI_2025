-- ============================================================================
-- CREACIÓN DE DATASET EN BIGQUERY
-- Proyecto: grupo09_retail_analytics
-- Autor: Grupo 9
-- ============================================================================

-- Crear dataset principal
CREATE SCHEMA IF NOT EXISTS `etl-retail-analytics.dataset_si807_g9`
OPTIONS (
    location = 'us-central1',
    description = 'Dataset para ETL Retail Analytics - Capas RAW, CURATED y ANALYTICS'
);