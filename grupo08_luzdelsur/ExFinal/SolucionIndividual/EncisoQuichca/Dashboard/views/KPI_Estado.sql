CREATE OR REPLACE VIEW vw_dataexfinal_accidents_by_state AS
SELECT
  state,
  accident_cnt,
  avg_severity
FROM kpi_accidents_by_state;
