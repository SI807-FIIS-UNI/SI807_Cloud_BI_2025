CREATE TABLE dw.fact_facturacion_mensual AS
SELECT
    -- 1. Claves surrogate (FK al DW)
    dcli.cliente_sk,
    dsumi.suministro_sk,
    dmed.medidor_sk,
    dtar.tarifa_sk,
    dubi.ubicacion_sk,
    dtime.tiempo_sk,

    -- 2. Claves de negocio (para trazabilidad)
    f.id_cliente,
    f.id_suministro,
    f.id_medidor,
    f.id_tarifa,
    f.id_ubicacion,
    f.anio,
    f.mes,
    f.anio_mes,

    -- 3. Métricas principales
    f.energia_valle,
    f.energia_pico,
    f.energia_media,
    f.energia_total,
    f.monto_facturado,

    -- 4. Flags de calidad / condición
    f.es_nulo_energia,
    f.es_nulo_monto,
    f.es_energia_negativa,
    f.es_monto_negativo,
    f.es_energia_cero

FROM staging.fact_facturacion_mensual f
LEFT JOIN dw.dim_cliente     dcli  ON dcli.id_cliente     = f.id_cliente
LEFT JOIN dw.dim_suministro  dsumi ON dsumi.id_suministro = f.id_suministro
LEFT JOIN dw.dim_medidor     dmed  ON dmed.id_medidor     = f.id_medidor
LEFT JOIN dw.dim_tarifa      dtar  ON dtar.id_tarifa      = f.id_tarifa
LEFT JOIN dw.dim_ubicacion   dubi  ON dubi.id_ubicacion   = f.id_ubicacion
LEFT JOIN dw.dim_tiempo      dtime ON dtime.anio          = f.anio
                                  AND dtime.mes           = f.mes;