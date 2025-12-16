import os
import time
import requests
import logging

logging.basicConfig(level=logging.INFO)

# ================================
# CONFIGURACIÓN DATABRICKS (ENV VARS)
# ================================
DATABRICKS_WORKSPACE_URL = os.environ.get("DATABRICKS_WORKSPACE_URL")
DATABRICKS_TOKEN = os.environ.get("DATABRICKS_TOKEN")
AZURE_STORAGE_CONNECTION_STRING = os.environ.get("AZURE_STORAGE_CONNECTION_STRING")

if not DATABRICKS_WORKSPACE_URL:
    raise RuntimeError("❌ ERROR: La variable DATABRICKS_WORKSPACE_URL no está definida en las variables de entorno.")

if not DATABRICKS_TOKEN:
    raise RuntimeError("❌ ERROR: La variable DATABRICKS_TOKEN no está definida en las variables de entorno.")

if not AZURE_STORAGE_CONNECTION_STRING:
    raise RuntimeError("❌ ERROR: La variable AZURE_STORAGE_CONNECTION_STRING no está definida en las variables de entorno.")


HEADERS = {
    "Authorization": f"Bearer {DATABRICKS_TOKEN}",
    "Content-Type": "application/json"
}

# Extraer el endpoint del storage account de la connection string
def get_adls_endpoint_from_conn_str(conn_str):
    if not conn_str:
        return None
    parts = {p.split('=', 1)[0].lower(): p.split('=', 1)[1] for p in conn_str.split(';') if '=' in p}
    account_name = parts.get('accountname')
    return f"{account_name}.dfs.core.windows.net"

ADLS_ENDPOINT = get_adls_endpoint_from_conn_str(AZURE_STORAGE_CONNECTION_STRING)

# ================================
# NOTEBOOK PATHS EN DATABRICKS
# ================================
NOTEBOOKS = {
    "flight_delays": [
        "/Workspace/Shared/Apps/FlightDelays/Limpiar",
        "/Workspace/Shared/Apps/FlightDelays/Transformar",
        "/Workspace/Shared/Apps/FlightDelays/Vista"
    ]
}


# ================================
# Ejecutar notebook como Job temporal
# ================================
def run_notebook(notebook_path: str, params: dict):
    logging.info(f"▶️ Ejecutando notebook: {notebook_path}")
    logging.info(f"📝 Parámetros: {params}")
    
    payload = {
        "run_name": f"Pipeline - {notebook_path.split('/')[-1]}",
        "tasks": [
            {
                "task_key": "main",
                "new_cluster": {
                    "spark_version": "15.4.x-scala2.12",
                    "node_type_id": "Standard_DS3_v2",
                    "num_workers": 0, # Clúster de nodo único
                    "spark_conf": {
                        "spark.databricks.cluster.profile": "singleNode"
                    }
                },
                "notebook_task": {
                    "notebook_path": notebook_path,
                    "base_parameters": params
                }
            }
        ],
        "timeout_seconds": 3600  # 1 hora de timeout
    }
    
    url = f"{DATABRICKS_WORKSPACE_URL}/api/2.1/jobs/runs/submit"
    
    try:
        response = requests.post(url, headers=HEADERS, json=payload)
        
        if response.status_code != 200:
            logging.error(f"❌ Response status: {response.status_code}")
            logging.error(f"❌ Response body: {response.text}")
            raise Exception(
                f"❌ Error lanzando notebook '{notebook_path}': {response.text}"
            )
        
        run_id = response.json()["run_id"]
        logging.info(f"✔ Notebook lanzado correctamente. Run ID: {run_id}")
        
        return run_id
        
    except Exception as e:
        logging.error(f"❌ Excepción lanzando notebook: {str(e)}")
        raise


# ================================
# Esperar a que un run termine
# ================================
def wait_for_run(run_id: int, timeout: int = 900):
    logging.info(f"⏳ Esperando ejecución del Run ID: {run_id}")
    
    url = f"{DATABRICKS_WORKSPACE_URL}/api/2.1/jobs/runs/get"
    start = time.time()
    
    while True:
        try:
            response = requests.get(url, headers=HEADERS, params={"run_id": run_id})
            
            if response.status_code != 200:
                logging.error(f"❌ Error consultando estado del run: {response.text}")
                time.sleep(5)
                continue
            
            state = response.json().get("state", {})
            life = state.get("life_cycle_state")
            result = state.get("result_state")
            
            logging.info(f"   → Estado actual: {life} / {result}")
            
            if life == "TERMINATED":
                if result == "SUCCESS":
                    logging.info("✔ Notebook finalizó correctamente.")
                    return True
                else:
                    error_info = state.get("state_message", "Error desconocido")
                    raise Exception(f"❌ Notebook falló: {error_info}")
            
            if time.time() - start > timeout:
                raise Exception(f"⛔ Timeout esperando el run {run_id}")
            
            time.sleep(5)
            
        except Exception as e:
            if "Notebook falló" in str(e) or "Timeout" in str(e):
                raise
            logging.error(f"❌ Error en wait_for_run: {str(e)}")
            time.sleep(5)


# ================================
# Ejecutar los notebooks secuenciales
# ================================
def trigger_notebook_run(destination: str, adls_path: str):
    """
    Ejecuta la secuencia de notebooks para un destino específico
    
    Args:
        destination: 'practitioner' o 'continuous_integration'
        adls_path: Ruta del archivo en ADLS
    """
    
    if destination not in NOTEBOOKS:
        raise ValueError(f"❌ Destino inválido: {destination}. Debe ser 'flight_delays'")
    
    params = {
        "adls_endpoint": ADLS_ENDPOINT
    }
    notebook_sequence = NOTEBOOKS[destination]
    
    logging.info("=" * 60)
    logging.info(f"🚀 Pipeline Databricks para: {destination}")
    logging.info(f"📄 Archivo ADLS: {adls_path}")
    logging.info("=" * 60)
    
    try:
        for idx, nb in enumerate(notebook_sequence, 1):
            logging.info(f"\n{'='*60}")
            logging.info(f"📓 Paso {idx}/{len(notebook_sequence)}: {nb.split('/')[-1]}")
            logging.info(f"{'='*60}")
            
            run_id = run_notebook(nb, params)
            wait_for_run(run_id)
        
        logging.info("\n" + "=" * 60)
        logging.info("🏁 Pipeline completado exitosamente.")
        logging.info("=" * 60)
        return True
        
    except Exception as e:
        logging.error("\n" + "=" * 60)
        logging.error(f"💥 Pipeline falló: {str(e)}")
        logging.error("=" * 60)
        raise
        "notebook_task": {
            "notebook_path": notebook_path,
            "base_parameters": params
        },
        "timeout_seconds": 3600  # 1 hora de timeout
    }
    
    url = f"{DATABRICKS_WORKSPACE_URL}/api/2.1/jobs/runs/submit"
    
    try:
        response = requests.post(url, headers=HEADERS, json=payload)
        
        if response.status_code != 200:
            logging.error(f"❌ Response status: {response.status_code}")
            logging.error(f"❌ Response body: {response.text}")
            raise Exception(
                f"❌ Error lanzando notebook '{notebook_path}': {response.text}"
            )
        
        run_id = response.json()["run_id"]
        logging.info(f"✔ Notebook lanzado correctamente. Run ID: {run_id}")
        
        return run_id
        
    except Exception as e:
        logging.error(f"❌ Excepción lanzando notebook: {str(e)}")
        raise


# ================================
# Esperar a que un run termine
# ================================
def wait_for_run(run_id: int, timeout: int = 900):
    logging.info(f"⏳ Esperando ejecución del Run ID: {run_id}")
    
    url = f"{DATABRICKS_WORKSPACE_URL}/api/2.1/jobs/runs/get"
    start = time.time()
    
    while True:
        try:
            response = requests.get(url, headers=HEADERS, params={"run_id": run_id})
            
            if response.status_code != 200:
                logging.error(f"❌ Error consultando estado del run: {response.text}")
                time.sleep(5)
                continue
            
            state = response.json().get("state", {})
            life = state.get("life_cycle_state")
            result = state.get("result_state")
            
            logging.info(f"   → Estado actual: {life} / {result}")
            
            if life == "TERMINATED":
                if result == "SUCCESS":
                    logging.info("✔ Notebook finalizó correctamente.")
                    return True
                else:
                    error_info = state.get("state_message", "Error desconocido")
                    raise Exception(f"❌ Notebook falló: {error_info}")
            
            if time.time() - start > timeout:
                raise Exception(f"⛔ Timeout esperando el run {run_id}")
            
            time.sleep(5)
            
        except Exception as e:
            if "Notebook falló" in str(e) or "Timeout" in str(e):
                raise
            logging.error(f"❌ Error en wait_for_run: {str(e)}")
            time.sleep(5)


# ================================
# Ejecutar los notebooks secuenciales
# ================================
def trigger_notebook_run(destination: str, adls_path: str):
    """
    Ejecuta la secuencia de notebooks para un destino específico
    
    Args:
        destination: 'practitioner' o 'continuous_integration'
        adls_path: Ruta del archivo en ADLS
    """
    
    if destination not in NOTEBOOKS:
        raise ValueError(f"❌ Destino inválido: {destination}. Debe ser 'flight_delays'")
    
    params = {
        "adls_endpoint": ADLS_ENDPOINT
    }
    notebook_sequence = NOTEBOOKS[destination]
    
    logging.info("=" * 60)
    logging.info(f"🚀 Pipeline Databricks para: {destination}")
    logging.info(f"📄 Archivo ADLS: {adls_path}")
    logging.info(f"🔧 Cluster ID: {CLUSTER_ID}")
    logging.info("=" * 60)
    
    try:
        for idx, nb in enumerate(notebook_sequence, 1):
            logging.info(f"\n{'='*60}")
            logging.info(f"📓 Paso {idx}/{len(notebook_sequence)}: {nb.split('/')[-1]}")
            logging.info(f"{'='*60}")
            
            run_id = run_notebook(nb, params)
            wait_for_run(run_id)
        
        logging.info("\n" + "=" * 60)
        logging.info("🏁 Pipeline completado exitosamente.")
        logging.info("=" * 60)
        return True
        
    except Exception as e:
        logging.error("\n" + "=" * 60)
        logging.error(f"💥 Pipeline falló: {str(e)}")
        logging.error("=" * 60)
        raise


# ================================
# Función de diagnóstico (opcional)
# ================================
def diagnose_cluster():
    """Función auxiliar para diagnosticar problemas con el cluster"""
    logging.info("\n🔍 DIAGNÓSTICO DE CLUSTER")
    logging.info("=" * 60)
    
    logging.info(f"Cluster ID configurado: {CLUSTER_ID}")
    logging.info(f"Workspace URL: {DATABRICKS_WORKSPACE_URL}")
    
    # Listar todos los clusters
    list_clusters()
    
    # Verificar estado del cluster específico
    try:
        ensure_cluster_running(CLUSTER_ID)
    except Exception as e:
        logging.error(f"❌ No se pudo verificar el cluster: {str(e)}")
    
    logging.info("=" * 60)


# Ejemplo de uso si ejecutas este archivo directamente
if __name__ == "__main__":
    # Descomentar para diagnosticar
    # diagnose_cluster()
    pass