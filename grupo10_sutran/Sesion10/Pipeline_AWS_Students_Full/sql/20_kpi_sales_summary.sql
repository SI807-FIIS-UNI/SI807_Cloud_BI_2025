
SELECT 
  category,
  SUM(sales) AS total_sales,
  SUM(profit) AS total_profit,
  ROUND(SUM(profit)/SUM(sales)*100,2) AS margen_pct
FROM analytics_db.sales_curated
GROUP BY category
ORDER BY total_profit DESC;
