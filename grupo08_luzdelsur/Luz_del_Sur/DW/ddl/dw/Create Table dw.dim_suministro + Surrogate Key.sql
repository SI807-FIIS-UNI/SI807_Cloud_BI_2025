CREATE TABLE dw.dim_suministro AS
SELECT
    row_number() OVER (ORDER BY id_suministro) AS suministro_sk,  -- surrogate key
    s.*
FROM (
    SELECT DISTINCT *
    FROM staging.dim_suministro
) s;