import pandas as pd
import os

# ===============================
# Configuración de rutas
# ===============================
BASE_PATH = os.path.dirname(os.path.dirname(__file__))
INPUT_PATH = os.path.join(BASE_PATH, "bronce", "raw", "SuperMarket Analysis.csv")
DIM_PATH = os.path.join(BASE_PATH, "plata", "dim")
FACT_PATH = os.path.join(BASE_PATH, "plata", "fact")

os.makedirs(DIM_PATH, exist_ok=True)
os.makedirs(FACT_PATH, exist_ok=True)

# ===============================
# Lectura del dataset
# ===============================
df = pd.read_csv(INPUT_PATH)

# ===============================
# Dimensiones
# ===============================

# Dim Tiempo
df["Date"] = pd.to_datetime(df["Date"])
dim_tiempo = df[["Date"]].drop_duplicates().reset_index(drop=True)
dim_tiempo["tiempo_key"] = dim_tiempo.index + 1
dim_tiempo["year"] = dim_tiempo["Date"].dt.year
dim_tiempo["month"] = dim_tiempo["Date"].dt.month
dim_tiempo["month_name"] = dim_tiempo["Date"].dt.month_name()

# Dim Sucursal
dim_sucursal = df[["Branch", "City"]].drop_duplicates().reset_index(drop=True)
dim_sucursal["sucursal_key"] = dim_sucursal.index + 1

# Dim Producto
dim_producto = df[["Product line", "Unit price"]].drop_duplicates().reset_index(drop=True)
dim_producto["producto_key"] = dim_producto.index + 1

# Dim Cliente
dim_cliente = df[["Customer type", "Gender"]].drop_duplicates().reset_index(drop=True)
dim_cliente["cliente_key"] = dim_cliente.index + 1

# Dim Pago
dim_pago = df[["Payment"]].drop_duplicates().reset_index(drop=True)
dim_pago["pago_key"] = dim_pago.index + 1

# ===============================
# Tabla de Hechos
# ===============================
fact_ventas = df.merge(dim_tiempo, on="Date") \
                .merge(dim_sucursal, on=["Branch", "City"]) \
                .merge(dim_producto, on=["Product line", "Unit price"]) \
                .merge(dim_cliente, on=["Customer type", "Gender"]) \
                .merge(dim_pago, on="Payment")

fact_ventas = fact_ventas[[
    "tiempo_key",
    "sucursal_key",
    "producto_key",
    "cliente_key",
    "pago_key",
    "Quantity",
    "Sales",
    "Tax 5%",
    "cogs",
    "gross income",
    "Rating"
]]

# ===============================
# Guardado
# ===============================
dim_tiempo.to_csv(os.path.join(DIM_PATH, "dim_tiempo.csv"), index=False)
dim_sucursal.to_csv(os.path.join(DIM_PATH, "dim_sucursal.csv"), index=False)
dim_producto.to_csv(os.path.join(DIM_PATH, "dim_producto.csv"), index=False)
dim_cliente.to_csv(os.path.join(DIM_PATH, "dim_cliente.csv"), index=False)
dim_pago.to_csv(os.path.join(DIM_PATH, "dim_pago.csv"), index=False)

fact_ventas.to_csv(os.path.join(FACT_PATH, "fact_ventas.csv"), index=False)

print("Modelo estrella generado correctamente (PLATA).")
