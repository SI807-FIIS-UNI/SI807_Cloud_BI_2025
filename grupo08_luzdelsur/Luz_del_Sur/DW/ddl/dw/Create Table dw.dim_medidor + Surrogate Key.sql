CREATE TABLE dw.dim_medidor AS
SELECT
    row_number() OVER (ORDER BY id_medidor) AS medidor_sk,  -- surrogate key
    s.*
FROM (
    SELECT DISTINCT *
    FROM staging.dim_medidor
) s;