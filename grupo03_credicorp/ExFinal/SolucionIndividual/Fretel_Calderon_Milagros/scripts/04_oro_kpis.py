import pandas as pd
import os

# ===============================
# Rutas
# ===============================
BASE_PATH = os.path.dirname(os.path.dirname(__file__))
FACT_PATH = os.path.join(BASE_PATH, "plata", "fact", "fact_ventas.csv")
ORO_KPIS = os.path.join(BASE_PATH, "oro", "kpis")

os.makedirs(ORO_KPIS, exist_ok=True)

# ===============================
# Lectura fact (PLATA)
# ===============================
df = pd.read_csv(FACT_PATH)

# ===============================
# KPIs principales (tarjetas)
# ===============================
ventas_total = df["Sales"].sum()
cantidad_total = df["Quantity"].sum()
ticket_promedio = df["Sales"].mean()
margen = (df["gross income"].sum() / df["Sales"].sum()) if df["Sales"].sum() != 0 else 0

kpis_resumen = pd.DataFrame([{
    "ventas_total": ventas_total,
    "margen": margen,
    "ticket_promedio": ticket_promedio,
    "cantidad_total": cantidad_total
}])

kpis_resumen.to_csv(os.path.join(ORO_KPIS, "kpis_resumen.csv"), index=False)

# ===============================
# Series para líneas (por tiempo_key)
# Nota: si quieres “mes-a-mes”, lo más fácil es unir con dim_tiempo en Power BI.
# Igual generamos un resumen por tiempo_key para gráficos.
# ===============================
ventas_tiempo = df.groupby("tiempo_key", as_index=False).agg(
    ventas=("Sales", "sum"),
    cantidad=("Quantity", "sum"),
    utilidad=("gross income", "sum")
)
ventas_tiempo.to_csv(os.path.join(ORO_KPIS, "ventas_mensuales.csv"), index=False)

# ===============================
# Por género (para tus líneas y tabla por género)
# Requiere join a dim_cliente en Power BI para convertir cliente_key -> Gender.
# Aquí agregamos por cliente_key (lo resuelves en Power BI con relaciones).
# ===============================
ventas_genero = df.groupby(["tiempo_key", "cliente_key"], as_index=False).agg(
    ventas=("Sales", "sum"),
    cantidad=("Quantity", "sum"),
    utilidad=("gross income", "sum")
)
ventas_genero.to_csv(os.path.join(ORO_KPIS, "ventas_genero_mensual.csv"), index=False)

cantidad_genero = df.groupby(["tiempo_key", "cliente_key"], as_index=False).agg(
    cantidad=("Quantity", "sum")
)
cantidad_genero.to_csv(os.path.join(ORO_KPIS, "cantidad_genero_mensual.csv"), index=False)

# ===============================
# Top líneas de producto
# (producto_key se resuelve con dim_producto en Power BI)
# ===============================
top_producto = df.groupby("producto_key", as_index=False).agg(
    ventas=("Sales", "sum"),
    utilidad=("gross income", "sum"),
    cantidad=("Quantity", "sum")
).sort_values("ventas", ascending=False)

top_producto.to_csv(os.path.join(ORO_KPIS, "top_producto.csv"), index=False)

print("KPIs generados correctamente (ORO). Archivos en oro/kpis/")
