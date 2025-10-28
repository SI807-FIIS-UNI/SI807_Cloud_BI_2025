from pathlib import Path
import pandas as pd

# limpieza.py
# Cargar el archivo gender_submission.csv en un DataFrame


DEFAULT_PATH = Path(r"data\raw\gender_submission.csv")

FILE_PATHS = {
    "gender_submission": DEFAULT_PATH,
    "test": Path(r"data\raw\test.csv"),
    "train": Path(r"data\raw\train.csv"),
}


def load_gender_submission(path: Path | str | None = None) -> pd.DataFrame:
    """
    Lee gender_submission.csv y devuelve un pandas DataFrame.
    Si no se entrega path, usa DEFAULT_PATH.
    """
    p = Path(path) if path is not None else DEFAULT_PATH
    if not p.exists():
        raise FileNotFoundError(f"Archivo no encontrado: {p}")
    return pd.read_csv(p)

if __name__ == "__main__":
    df = load_gender_submission()
    print(f"Leído {len(df)} filas, {len(df.columns)} columnas")
    print(df.head())