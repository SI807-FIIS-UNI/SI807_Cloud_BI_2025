import os

class Config:

    # Carpeta temporal para uploads
    UPLOAD_FOLDER = os.path.join(os.path.dirname(os.path.abspath(__file__)), "uploads_tmp")

    # --------------------------------------------------------
    # 🔵 Variables de entorno — Azure PostgreSQL
    # --------------------------------------------------------
    DB_HOST = os.environ.get("DB_HOST")
    DB_PORT = os.environ.get("DB_PORT")
    DB_USER = os.environ.get("DB_USER")
    DB_PASSWORD = os.environ.get("DB_PASSWORD")

    DB_NAME = os.environ.get("DB_NAME")

    # --------------------------------------------------------
    # 🔵 Cadenas de conexión PostgreSQL
    # --------------------------------------------------------
    # Se unifica a una sola base de datos. La distinción se hace por vistas, no por BD.
    DB_CONN_STRING = (
        f"host={DB_HOST} port={DB_PORT} dbname={DB_NAME} "
        f"user={DB_USER} password={DB_PASSWORD} sslmode=require"
    ) if DB_HOST and DB_NAME else None