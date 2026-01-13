import functions_framework
import pandas as pd
from google.cloud import bigquery
from google.cloud import storage
import os

# --- CONFIGURACIÓN ---
PROJECT_ID = "final-sin-andrade-saavedra"
DATASET_SILVER = "ds_silver"
DATASET_GOLD = "ds_gold"


@functions_framework.cloud_event
def procesar_etl(cloud_event):
    data = cloud_event.data
    bucket_name = data["bucket"]
    file_name = data["name"]

    print(f"🚀 INICIO STAR SCHEMA (3 DIMENSIONES): Archivo {file_name}")

    if "bronce/raw/" not in file_name:
        print("⚠️ Archivo fuera de ruta raw. Ignorando.")
        return

    try:
        # 1. LEER DATOS
        uri = f"gs://{bucket_name}/{file_name}"
        try:
            df = pd.read_csv(uri, encoding="utf-8")
        except:
            df = pd.read_csv(uri, encoding="latin1")

        # 2. LIMPIEZA GENERAL
        df.columns = [
            x.lower().strip().replace(" ", "_").replace("-", "_") for x in df.columns
        ]

        for col in ["order_date", "ship_date"]:
            if col in df.columns:
                df[col] = pd.to_datetime(df[col], dayfirst=True, errors="coerce")

        if "sales" in df.columns:
            if df["sales"].dtype == "object":
                df["sales"] = (
                    df["sales"].astype(str).str.replace("$", "").str.replace(",", "")
                )
            df["sales"] = pd.to_numeric(df["sales"], errors="coerce")

        # Limpieza de nulos en Postal Code para poder agrupar bien
        if "postal_code" in df.columns:
            df["postal_code"] = df["postal_code"].fillna(0).astype(int)

        # 3. CONSTRUCCIÓN DEL MODELO ESTRELLA (CAPA PLATA)
        print("⭐ Construyendo Modelo Estrella con DIM_UBICACION...")

        # --- PASO CRÍTICO: GENERAR ID PARA UBICACIÓN ---
        # Agrupamos por todas las columnas geográficas para crear un ID único
        cols_geo = ["country", "city", "state", "postal_code", "region"]
        # Validamos que existan
        cols_geo_existentes = [c for c in cols_geo if c in df.columns]

        # Creamos el ID sintético 'id_ubicacion'
        df["id_ubicacion"] = df.groupby(cols_geo_existentes).ngroup()

        # --- A. TABLA DIMENSIÓN UBICACIÓN (NUEVA) ---
        dim_ubicacion = (
            df[["id_ubicacion"] + cols_geo_existentes]
            .drop_duplicates(subset=["id_ubicacion"])
            .copy()
        )

        dim_ubicacion = dim_ubicacion.rename(
            columns={
                "country": "pais",
                "city": "ciudad",
                "state": "estado",
                "postal_code": "codigo_postal",
                "region": "region",
            }
        )

        dim_ubicacion.to_gbq(
            f"{PROJECT_ID}.{DATASET_SILVER}.dim_ubicacion",
            project_id=PROJECT_ID,
            if_exists="replace",
        )
        print("   -> Dimensión Ubicación cargada.")

        # --- B. TABLA DIMENSIÓN CLIENTE ---
        cols_cliente = ["customer_id", "customer_name", "segment"]
        dim_cliente = df[cols_cliente].drop_duplicates(subset=["customer_id"]).copy()

        dim_cliente = dim_cliente.rename(
            columns={
                "customer_id": "id_cliente",
                "customer_name": "nombre_cliente",
                "segment": "segmento",
            }
        )

        dim_cliente.to_gbq(
            f"{PROJECT_ID}.{DATASET_SILVER}.dim_cliente",
            project_id=PROJECT_ID,
            if_exists="replace",
        )
        print("   -> Dimensión Cliente cargada.")

        # --- C. TABLA DIMENSIÓN PRODUCTO ---
        cols_producto = ["product_id", "product_name", "category", "sub_category"]
        dim_producto = df[cols_producto].drop_duplicates(subset=["product_id"]).copy()

        dim_producto = dim_producto.rename(
            columns={
                "product_id": "id_producto",
                "product_name": "nombre_producto",
                "category": "categoria",
                "sub_category": "sub_categoria",
            }
        )

        dim_producto.to_gbq(
            f"{PROJECT_ID}.{DATASET_SILVER}.dim_producto",
            project_id=PROJECT_ID,
            if_exists="replace",
        )
        print("   -> Dimensión Producto cargada.")

        # --- D. TABLA DE HECHOS (FACT TABLE) ---
        # Ahora incluimos 'id_ubicacion' y borramos los textos de geografía
        cols_excluir = [
            "customer_name",
            "segment",
            "product_name",
            "category",
            "sub_category",
            "country",
            "city",
            "state",
            "postal_code",
            "region",
        ]  # Borramos region texto porque ya está en la dim

        fact_ventas = df.drop(
            columns=[c for c in cols_excluir if c in df.columns]
        ).copy()

        fact_ventas = fact_ventas.rename(
            columns={
                "order_id": "id_orden",
                "order_date": "fecha_orden",
                "ship_date": "fecha_envio",
                "ship_mode": "modo_envio",
                "customer_id": "id_cliente",
                "product_id": "id_producto",
                "sales": "ventas",
            }
        )

        fact_ventas.to_gbq(
            f"{PROJECT_ID}.{DATASET_SILVER}.fact_ventas",
            project_id=PROJECT_ID,
            if_exists="replace",
        )
        print("   -> Tabla de Hechos cargada (con FK Ubicación).")

        # 4. CAPA ORO (KPIs Agregados)
        print("📊 Calculando KPIs (Capa Oro)...")
        # Usamos el DF original que aún tiene 'region' y 'category' en memoria
        df_kpi = (
            df.groupby(["region", "category"])
            .agg(total_ventas=("sales", "sum"), total_pedidos=("order_id", "count"))
            .reset_index()
        )

        df_kpi["ticket_promedio"] = (
            df_kpi["total_ventas"] / df_kpi["total_pedidos"]
        ).round(2)
        df_kpi["total_ventas"] = df_kpi["total_ventas"].round(2)

        df_kpi = df_kpi.rename(columns={"category": "categoria", "region": "region"})

        df_kpi.to_gbq(
            f"{PROJECT_ID}.{DATASET_GOLD}.kpi_regional_gold",
            project_id=PROJECT_ID,
            if_exists="replace",
        )
        print("🏆 KPIs cargados.")

        # 5. MOVER ARCHIVO
        storage_client = storage.Client()
        bucket = storage_client.bucket(bucket_name)
        blob = bucket.blob(file_name)
        new_name = file_name.replace("bronce/raw/", "bronce/processed/")
        bucket.rename_blob(blob, new_name)

        print("🏁 PROCESO ESTRELLA FINALIZADO.")

    except Exception as e:
        print(f"❌ ERROR: {str(e)}")
        raise e
