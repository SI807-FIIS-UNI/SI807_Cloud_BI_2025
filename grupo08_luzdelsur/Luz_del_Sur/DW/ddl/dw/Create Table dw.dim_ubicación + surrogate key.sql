CREATE TABLE dw.dim_ubicacion AS
SELECT
    row_number() OVER (ORDER BY id_ubicacion) AS ubicacion_sk,  -- surrogate key
    s.*
FROM (
    SELECT DISTINCT *
    FROM staging.dim_ubicacion
) s;