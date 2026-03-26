import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

plt.style.use("seaborn-v0_8-whitegrid")
sns.set_palette("crest")

# === 1. RESUMEN GENERAL ===
def resumen_general(df):
    print("📊 Dimensiones:", df.shape)
    print("\n📋 Tipos de datos:")
    print(df.dtypes)
    print("\n🔍 Valores nulos por columna:")
    print(df.isnull().sum())
    print("\n🧮 Duplicados:", df.duplicated().sum())
    return df.describe(include="all").T


# === 2. DISTRIBUCIÓN DE VARIABLES NUMÉRICAS ===
def distribucion_numericas(df, cols=None):
    if cols is None:
        cols = df.select_dtypes(include=np.number).columns
    if len(cols) == 0:
        print("⚠️ No hay columnas numéricas para graficar.")
        return
    n = len(cols)
    fig, axes = plt.subplots(nrows=(n+2)//3, ncols=3, figsize=(15, 4*((n+2)//3)))
    axes = axes.flatten()
    for i, col in enumerate(cols):
        sns.histplot(df[col].dropna(), bins=30, ax=axes[i], kde=True, color="skyblue")
        axes[i].set_title(f"Distribución de {col}")
    plt.tight_layout()
    plt.show()


# === 3. VALORES FALTANTES ===
def plot_missing(df):
    missing = df.isnull().mean() * 100
    missing = missing[missing > 0].sort_values(ascending=False)
    if not missing.empty:
        plt.figure(figsize=(10,4))
        sns.barplot(x=missing.index, y=missing.values, palette="flare")
        plt.xticks(rotation=45, ha="right")
        plt.title("Porcentaje de valores faltantes")
        plt.ylabel("%")
        plt.show()
    else:
        print("✅ No hay valores faltantes.")


# === 4. MAPA DE CORRELACIONES ===
def plot_correlaciones(df):
    num_df = df.select_dtypes(include=np.number)
    if num_df.shape[1] < 2:
        print("⚠️ No hay suficientes variables numéricas para calcular correlaciones.")
        return
    corr = num_df.corr()
    plt.figure(figsize=(10,8))
    sns.heatmap(corr, annot=True, fmt=".2f", cmap="YlGnBu", square=True)
    plt.title("Mapa de correlación numérica")
    plt.show()


# === 5. ANÁLISIS DE VENTAS ===
def analisis_ventas(df):
    if "Amount" not in df.columns:
        print("⚠️ No se encontró la columna 'Amount'.")
        return
    plt.figure(figsize=(8,4))
    sns.histplot(df["amount"], bins=30, kde=True, color="mediumseagreen")
    plt.title("Distribución de Montos de Venta (Amount)")
    plt.xlabel("Monto de Venta")
    plt.ylabel("Frecuencia")
    plt.show()

    print("💰 Total vendido:", df["amount"].sum())
    print("📦 Total de órdenes:", df["Order ID"].nunique())


# === 6. TOP CATEGORÍAS ===
def top_categorias(df, group_field="Category", metric="Amount", n=10):
    if group_field not in df.columns or metric not in df.columns:
        print(f"⚠️ No existen las columnas '{group_field}' o '{metric}'.")
        return
    top = (df.groupby(group_field)[metric]
           .sum()
           .sort_values(ascending=False)
           .head(n))
    plt.figure(figsize=(8,4))
    sns.barplot(x=top.index, y=top.values, hue=top.index, legend=False, palette="crest")
    plt.title(f"Top {n} {group_field} por {metric}")
    plt.ylabel(metric)
    plt.xlabel(group_field)
    plt.xticks(rotation=45, ha="right")
    plt.show()
    return top
