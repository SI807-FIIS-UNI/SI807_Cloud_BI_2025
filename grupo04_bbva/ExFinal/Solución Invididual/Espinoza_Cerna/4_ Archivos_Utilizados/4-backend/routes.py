# ============================================================
# 1. Importaciones
# ============================================================
import uuid
from flask import Blueprint, request, jsonify, current_app
from threading import Thread
from database import get_flight_kpis, get_flight_filter_options, get_flight_details
from databricks_client import trigger_notebook_run

# Subida ADLS
from azure_storage import upload_csv_stream_to_datalake

api = Blueprint("api", __name__)


# ============================================================
# 2. Test API
# ============================================================
@api.route("/")
def index():
    return jsonify({"message": "API del Dashboard funcionando correctamente", "status": "ok"})


# ============================================================
# 3. Headers esperados por destino
# ============================================================
EXPECTED_HEADERS = {
    "flight_delays": [
        'DayOfWeek','Date','DepTime','ArrTime','CRSArrTime','UniqueCarrier',
        'Airline','FlightNum','TailNum','ActualElapsedTime','CRSElapsedTime',
        'AirTime','ArrDelay','DepDelay','Origin','Org_Airport','Dest',
        'Dest_Airport','Distance','TaxiIn','TaxiOut','Cancelled',
        'CancellationCode','Diverted','CarrierDelay','WeatherDelay',
        'NASDelay','SecurityDelay','LateAircraftDelay'
    ]
}

TASK_STATUSES = {}


# ============================================================
# 4. Upload CSV directo a ADLS (sin archivos locales)
# ============================================================
@api.route("/upload", methods=["POST"])
def upload_file():

    if "file" not in request.files:
        return jsonify({"error": "No file uploaded"}), 400

    file = request.files["file"]
    filename = file.filename
    destination = "flight_delays" # Se asume un único destino para el caso de vuelos

    if not filename.lower().endswith(".csv"):
        return jsonify({"error": "El archivo debe ser .csv"}), 400

    if destination not in EXPECTED_HEADERS:
        return jsonify({"error": "Destino inválido."}), 400

    # -----------------------------------------
    # 1️⃣ Validar headers directo desde memoria
    # -----------------------------------------
    file.stream.seek(0)
    first_line = file.stream.readline().decode("utf-8")
    uploaded_headers = [h.replace("\ufeff", "").strip() for h in first_line.strip().split(",")]

    if uploaded_headers != EXPECTED_HEADERS[destination]:
        return jsonify({
            "error": "Los encabezados del CSV NO coinciden.",
            "expected": EXPECTED_HEADERS[destination],
            "received": uploaded_headers
        }), 400

    # -----------------------------------------
    # 2️⃣ Subir directo al Data Lake
    # -----------------------------------------
    file.stream.seek(0)
    try:
        blob_path = upload_csv_stream_to_datalake(destination, filename, file.stream)
    except Exception as e:
        return jsonify({"error": f"Error subiendo a Data Lake: {str(e)}"}), 500

    # -----------------------------------------
    # 3️⃣ Lanzar pipeline Databricks en background
    # -----------------------------------------
    task_id = str(uuid.uuid4())
    TASK_STATUSES[task_id] = {
        "status": "procesando",
        "message": "Ejecutando pipeline..."
    }

    app = current_app._get_current_object()
    thread = Thread(
        target=process_background,
        args=(app, task_id, destination, filename, blob_path)
    )
    thread.start()

    return jsonify({"task_id": task_id}), 202


# ============================================================
# 5. Estado de procesamiento
# ============================================================
@api.route("/upload/status/<task_id>", methods=["GET"])
def upload_status(task_id):
    task = TASK_STATUSES.get(task_id)
    if not task:
        return jsonify({"error": "Tarea no encontrada"}), 404
    return jsonify(task)


# ============================================================
# 6. Background – ejecutar Databricks
# ============================================================
def process_background(app, task_id, destination, filename, adls_path):
    with app.app_context():
        try:
            trigger_notebook_run(destination, adls_path)

            TASK_STATUSES[task_id] = {
                "status": "completado",
                "message": "Pipeline completado correctamente."
            }

        except Exception as e:
            TASK_STATUSES[task_id] = {
                "status": "error",
                "message": f"Error: {str(e)}"
            }


# ============================================================
# 7. Endpoints para el Dashboard de Vuelos
# ============================================================

@api.route("/flights/kpis", methods=["GET"])
def flight_kpis():
    """Endpoint para obtener los KPIs de vuelos con paginación y filtros."""
    args = request.args
    return jsonify(get_flight_kpis(
        page=args.get("page", 1, type=int),
        limit=args.get("limit", 10, type=int),
        airline=args.get("airline", "todos"),
        origin=args.get("origin", "todos"),
        date=args.get("date", "todos")
    ))

@api.route("/flights/filters", methods=["GET"])
def flight_filters():
    """Endpoint para obtener las opciones de los filtros (aerolíneas, orígenes, fechas)."""
    return jsonify(get_flight_filter_options())

@api.route("/flights/explore", methods=["GET"])
def flight_explorer():
    """Endpoint para obtener los datos detallados de vuelos para el explorador."""
    args = request.args
    return jsonify(get_flight_details(
        page=args.get("page", 1, type=int),
        limit=args.get("limit", 10, type=int),
        airline=args.get("airline", "todos"),
        origin=args.get("origin", "todos"),
        date=args.get("date", "todos")
    ))