# Este bloque de codigo también sirve para limpiar la data pero este está ubicado en un solo bloque

import pandas as pd
import os

def clean_titanic_data():
    train = pd.read_csv("../data/raw/train.csv")
    test = pd.read_csv("../data/raw/test.csv")
    gender = pd.read_csv("../data/raw/gender_submission.csv")

    for df in [train, test]:
        df.drop(columns=["Cabin", "Ticket"], inplace=True)
        df["Age"].fillna(df["Age"].median(), inplace=True)
        if "Fare" in df.columns:
            df["Fare"].fillna(df["Fare"].median(), inplace=True)
        df["Sex"] = df["Sex"].map({"male": 0, "female": 1})
        df["Embarked"].fillna("S", inplace=True)
        df["Embarked"] = df["Embarked"].map({"S": 0, "C": 1, "Q": 2})

    train.to_csv("../data/processed/train_clean.csv", index=False)
    test.to_csv("../data/processed/test_clean.csv", index=False)
    gender.to_csv("../data/processed/gender_submission.csv", index=False)
    print("✅ Datos limpios exportados correctamente")

clean_titanic_data()
