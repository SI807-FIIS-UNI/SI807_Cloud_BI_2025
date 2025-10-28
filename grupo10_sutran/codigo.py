# -*- coding: utf-8 -*-
import argparse
import re
import sys
import unicodedata
from pathlib import Path  # Asegúrate de que esta línea esté aquí
from typing import Optional, List

import pandas as pd  # Asegúrate de que esta línea esté aquí
import numpy as np

RAW_DEFAULT = Path("data/raw")
OUT_DEFAULT = Path("data/processed")


# ----------------------------- Debug -----------------------------
def _norm_name(s: str) -> str:
    """Normaliza unicode, quita espacios invisibles y pone en minúsculas."""
    if s is None:
        return ""
    s = unicodedata.normalize("NFC", s)
    # quita espacios comunes e invisibles (NBSP, zero-width)
    s = s.strip().strip("\u200b").strip("\u00A0")
    return s.lower()


def find_file(raw_dir: Path, candidate_names: List[str]) -> Optional[Path]:
    """
    Busca recursivamente en raw_dir un archivo cuyo nombre normalizado
    (minúsculas, sin espacios invisibles) coincida con cualquiera de candidate_names.
    """
    if not raw_dir.exists():
        return None

    # 1) intento directo (no recursivo) por nombre exacto
    for n in candidate_names:
        p = raw_dir / n
        if p.exists() and p.is_file():
            return p

    # 2) búsqueda recursiva tolerante
    wanted = {_norm_name(n): n for n in candidate_names}
    for p in raw_dir.rglob("*"):
        if p.is_file():
            if _norm_name(p.name) in wanted:
                return p

    return None


def _debug_list_raw(raw_dir: Path) -> None:
    print(f"[DEBUG] Verificando la ruta de data/raw: {raw_dir.resolve()}")
    
    # Verifica que la ruta de la carpeta sea correcta
    if not raw_dir.exists():
        print("[DEBUG] ¡La carpeta NO existe!")
        return
    
    print("[DEBUG] Archivos encontrados en data/raw:")
    found_any = False
    for p in raw_dir.rglob("*"):
        if p.is_file():
            found_any = True
            print(f" - {p.relative_to(raw_dir)} (archivo encontrado: {p.name})")
    if not found_any:
        print("[DEBUG] ¡No se encontraron archivos!")
    print("-" * 40)


def missing_report(df_: pd.DataFrame) -> pd.DataFrame:
    miss = df_.isna().sum()
    pct = (df_.isna().mean() * 100).round(2)
    r = pd.DataFrame({"missing": miss, "missing_%": pct})
    return r[r["missing"] > 0].sort_values("missing_%", ascending=False)


def extract_title(name: str) -> str:
    m = re.search(r",\s*([^\.]+)\.", name or "")
    return m.group(1).strip() if m else "Unknown"


# ----------------------------- limpieza -----------------------------
def clean_concat(df: pd.DataFrame) -> pd.DataFrame:
    # 1) strings -> trim
    for col in df.select_dtypes(include=["object"]).columns:
        df[col] = df[col].astype(str).str.strip()

    # 2) tipos numéricos
    for col in ["Age", "SibSp", "Parch", "Fare"]:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors="coerce")

    # 3) Title desde Name (y agrupar raros)
    if "Name" in df.columns:
        df["Title"] = df["Name"].apply(extract_title)
        df["Title"] = df["Title"].replace({
            "Mlle": "Miss", "Ms": "Miss", "Mme": "Mrs",
            "Lady": "Royalty", "Countess": "Royalty", "Sir": "Royalty",
            "Don": "Royalty", "Dona": "Royalty", "Jonkheer": "Royalty",
            "Capt": "Officer", "Col": "Officer", "Major": "Officer",
            "Dr": "Officer", "Rev": "Officer",
        })
        rare = df["Title"].value_counts()
        df["Title"] = df["Title"].where(rare.ge(10), "Other")

    # 4) Deck desde Cabin
    if "Cabin" in df.columns:
        df["Deck"] = df["Cabin"].fillna("U").astype(str).str[0]
        df.loc[df["Deck"].isna() | (df["Deck"] == "n"), "Deck"] = "U"
    else:
        df["Deck"] = "U"

    # 5) Ticket limpio: prefijo y largo numérico
    if "Ticket" in df.columns:
        t = (df["Ticket"].astype(str)
             .str.replace(r"[./]", "", regex=True)
             .str.replace(r"\s+", " ", regex=True)
             .str.strip())
        df["Ticket_Clean"] = t
        df["Ticket_Prefix"] = t.str.extract(r"^([A-Za-z]+)")[0].fillna("NONE")
        df["Ticket_Len"] = t.str.replace(r"\D", "", regex=True).str.len().fillna(0).astype(int)
    else:
        df["Ticket_Prefix"] = "NONE"
        df["Ticket_Len"] = 0

    # 6) Familia
    if {"SibSp", "Parch"}.issubset(df.columns):
        df["FamilySize"] = df["SibSp"].fillna(0) + df["Parch"].fillna(0) + 1
        df["IsAlone"] = (df["FamilySize"] == 1).astype(int)

    # 7) Embarked (moda)
    if "Embarked" in df.columns:
        mode = df["Embarked"].dropna().mode()
        df["Embarked"] = df["Embarked"].fillna(mode.iloc[0] if len(mode) else "S")

    # 8) Fare (mediana por Pclass+Embarked; fallback global)
    if "Fare" in df.columns:
        grp = df.groupby(["Pclass", "Embarked"])["Fare"].transform(lambda s: s.fillna(s.median()))
        df["Fare"] = df["Fare"].fillna(grp).fillna(df["Fare"].median())

    # 9) Age (mediana por Title+Sex+Pclass; fallback global)
    grp_cols = [c for c in ["Title", "Sex", "Pclass"] if c in df.columns]
    if "Age" in df.columns and grp_cols:
        med = df.groupby(grp_cols)["Age"].transform("median")
        df["Age"] = df["Age"].fillna(med).fillna(df["Age"].median())

    # 10) Sex normalizado y bandera
    if "Sex" in df.columns:
        df["Sex"] = df["Sex"].str.lower()
        df["IsFemale"] = (df["Sex"] == "female").astype(int)

    # 11) Bins de edad
    if "Age" in df.columns:
        df["AgeBin"] = pd.cut(
            df["Age"], bins=[0, 12, 18, 35, 50, 80],
            labels=["child", "teen", "young", "adult", "senior"],
            include_lowest=True
        )

    # 12) trim final
    for col in df.select_dtypes(include=["object"]).columns:
        df[col] = df[col].astype(str).str.strip()

    return df


# ----------------------------- main -----------------------------
def main(raw_dir: Path, out_dir: Path) -> None:
    out_dir.mkdir(parents=True, exist_ok=True)

    # DEBUG: muestra lo que realmente ve el script
    _debug_list_raw(raw_dir)

    # Verificación exacta de los archivos
    print("[DEBUG] Verificando si train.csv y test.csv están en la carpeta...")
    train_path = find_file(raw_dir, ["train.csv"])
    test_path = find_file(raw_dir, ["test.csv"])

    # Si no encuentra los archivos, muestra un mensaje de ayuda
    if not train_path or not test_path:
        print("\n[AYUDA] No se hallaron 'train.csv' y/o 'test.csv'. Prueba esto:")
        print("  1) Verifica que los archivos estén en la carpeta correcta.")
        print("  2) Si usas VS Code, asegúrate de que el 'cwd' sea la raíz del repo.")
        print("  3) Ejecuta con rutas explícitas:")
        print("       python codigo.py --raw \"./data/raw\" --out \"./data/processed\"")
        print("  4) Si usas el depurador de VS Code, asegúrate de que el 'cwd' sea la raíz del repo.\n")
        sys.exit(f"[ERROR] No encontré 'train.csv' y/o 'test.csv' en {raw_dir.resolve()}")

    # Continuar con el flujo de procesamiento...
    print(f"[DEBUG] Archivos encontrados: {train_path}, {test_path}")

    # Limpiar y crear los datasets
    train = pd.read_csv(train_path)
    test = pd.read_csv(test_path)

    train_raw, test_raw = train.copy(), test.copy()

    # Unir los archivos para procesarlos juntos
    train["__dataset__"] = "train"
    test["__dataset__"] = "test"
    if "Survived" not in test.columns:
        test["Survived"] = np.nan
    df = pd.concat([train, test], ignore_index=True)

    # Limpiar datos
    df = clean_concat(df)

    # Guardar los resultados
    train_clean_basic = df[df["__dataset__"] == "train"].drop(columns="__dataset__").reset_index(drop=True)
    test_clean_basic = df[df["__dataset__"] == "test"].drop(columns=["__dataset__", "Survived"]).reset_index(drop=True)

    train_clean_basic.to_csv(out_dir / "train_clean_basic.csv", index=False)
    test_clean_basic.to_csv(out_dir / "test_clean_basic.csv", index=False)

    print(f"[OK] Archivos escritos en {out_dir.resolve()}")
    for f in ["train_clean_basic.csv", "test_clean_basic.csv"]:
        print(f" - {f}")


if __name__ == "__main__":
    ap = argparse.ArgumentParser(description="Limpieza Titanic: data/raw -> data/processed")
    ap.add_argument("--raw", type=Path, default=RAW_DEFAULT, help="Carpeta de entrada (por defecto: data/raw)")
    ap.add_argument("--out", type=Path, default=OUT_DEFAULT, help="Carpeta de salida (por defecto: data/processed)")
    args = ap.parse_args()
    main(args.raw, args.out)
