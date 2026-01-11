CREATE OR REPLACE VIEW bi.dim_tarifa AS
SELECT
    tarifa_sk,
    id_tarifa,
    codigo_tarifa,
    cod_tarifa,
    descripcion,
    nivel_tension,
    segmento_objetivo,
    tipo_cliente,
    cargo_fijo,
    cargo_energia,
    cargo_hp,
    cargo_fp,
    incluye_demanda,
    estado_tarifa,
    fecha_inicio_vigencia
FROM dw.dim_tarifa;