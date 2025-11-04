
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

plt.style.use("seaborn-v0_8-whitegrid")
sns.set_palette("crest")

def resumen_general(df):
    print("📊 Dimensiones:", df.shape)
    print("\n📋 Tipos de datos:")
    print(df.dtypes)
    print("\n🔍 Valores nulos por columna:")
    print(df.isnull().sum())
    print("\n🧮 Duplicados:", df.duplicated().sum())
    return df.describe(include="all").T

def distribucion_numericas(df, cols=None):
    if cols is None:
        cols = df.select_dtypes(include=np.number).columns
    n = len(cols)
    fig, axes = plt.subplots(nrows=(n+2)//3, ncols=3, figsize=(15, 4*((n+2)//3)))
    axes = axes.flatten()
    for i, col in enumerate(cols):
        sns.histplot(df[col], bins=30, ax=axes[i], kde=True, color="skyblue")
        axes[i].set_title(f"Distribución de {col}")
    plt.tight_layout()
    plt.show()

def plot_missing(df):
    missing = df.isnull().mean() * 100
    missing = missing[missing > 0].sort_values(ascending=False)
    if not missing.empty:
        plt.figure(figsize=(10,4))
        sns.barplot(x=missing.index, y=missing.values, palette="flare")
        plt.xticks(rotation=45)
        plt.title("Porcentaje de valores faltantes")
        plt.ylabel("%")
        plt.show()
    else:
        print("✅ No hay valores faltantes.")

def plot_correlaciones(df):
    num_df = df.select_dtypes(include=np.number)
    corr = num_df.corr()
    plt.figure(figsize=(10,8))
    sns.heatmap(corr, annot=True, fmt=".2f", cmap="YlGnBu", square=True)
    plt.title("Mapa de correlación numérica")
    plt.show()

def analisis_ventas_profit(df):
    fig, ax = plt.subplots(1,2, figsize=(12,4))
    sns.histplot(df["Sales"], bins=30, ax=ax[0], kde=True, color="skyblue")
    ax[0].set_title("Distribución de Ventas")
    sns.histplot(df["Profit"], bins=30, ax=ax[1], kde=True, color="salmon")
    ax[1].set_title("Distribución de Ganancia")
    plt.show()

def top_categorias(df, group_field="Category", metric="Profit", n=10):
    top = (df.groupby(group_field)[metric]
           .sum()
           .sort_values(ascending=False)
           .head(n))
    plt.figure(figsize=(8,4))
    sns.barplot(x=top.index, y=top.values, palette="crest")
    plt.title(f"Top {n} {group_field} por {metric}")
    plt.ylabel(metric)
    plt.xlabel(group_field)
    plt.xticks(rotation=45)
    plt.show()
    return top
