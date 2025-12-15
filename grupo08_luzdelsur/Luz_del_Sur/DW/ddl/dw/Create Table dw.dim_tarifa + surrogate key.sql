CREATE TABLE dw.dim_tarifa AS
SELECT
    row_number() OVER (ORDER BY id_tarifa) AS tarifa_sk,  -- surrogate key
    s.*
FROM (
    SELECT DISTINCT *
    FROM staging.dim_tarifa
) s;