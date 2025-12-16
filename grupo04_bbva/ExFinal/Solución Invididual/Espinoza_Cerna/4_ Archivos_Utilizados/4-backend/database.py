# ============================================================
# 1. Importar librerías
# ============================================================
from datetime import datetime
import psycopg2
import psycopg2.extras
from config import Config
from flask import g


# ============================================================
# 2. Conexión a la base de datos
# ============================================================
def get_db(maturity_level='practitioner'):
    if 'db_conn' not in g:
        if not Config.DB_CONN_STRING:
            raise ValueError("La cadena de conexión a la base de datos no está configurada.")
        g.db_conn = psycopg2.connect(Config.DB_CONN_STRING)
    return g.db_conn


def close_db(e=None):
    # Cierra la única conexión si existe.
    conn = g.pop('db_conn', None)
    if conn is not None:
        conn.close()


# ============================================================
# 3. Construcción dinámica de filtros
# ============================================================
def _build_where_clause(**filters):
    """Construye cláusulas WHERE para las consultas de vuelos."""
    where = []
    params = []

    mapping = {
        'airline': "airline_name = %s",
        'origin': "origin_airport = %s",
        'date': "flight_date = %s"
    }

    for key, value in filters.items():
        if value and value.lower() != "todos" and key in mapping:
            where.append(mapping[key])
            params.append(value)

    sql = ""
    if where:
        sql = "WHERE " + " AND ".join(where)

    return sql, params


# ============================================================
# 4. Obtener KPIs de Vuelos
# ============================================================
def get_flight_kpis(page=1, limit=10, airline='todos', origin='todos', date='todos'):
    """Obtiene datos paginados de la vista de KPIs de vuelos."""
    view = "public.vw_flight_kpis"
    where_sql, params = _build_where_clause(airline=airline, origin=origin, date=date)

    query_count = f"SELECT COUNT(*) FROM {view} {where_sql}"
    query_data = f"""
        SELECT 
            TO_CHAR(flight_date, 'YYYY-MM-DD') as flight_date,
            airline_name,
            origin_airport,
            total_flights,
            on_time_arrival_pct,
            cancellation_rate_pct,
            avg_arrival_delay
        FROM {view}
        {where_sql}
        ORDER BY flight_date DESC, airline_name, origin_airport
        LIMIT %s OFFSET %s
    """

    conn = get_db()
    try:
        with conn.cursor(cursor_factory=psycopg2.extras.DictCursor) as cur:
            cur.execute(query_count, params)
            total = cur.fetchone()[0]

            cur.execute(query_data, params + [limit, (page - 1) * limit])
            data = [dict(row) for row in cur.fetchall()]
            return {"data": data, "totalCount": total}
    except Exception as e:
        conn.rollback()
        return {"error": str(e)}


# ============================================================
# 5. Opciones de Filtros para Vuelos
# ============================================================
def get_flight_filter_options():
    """Obtiene valores únicos para los filtros de aerolínea, origen y fecha."""
    view = "public.vw_flight_kpis"
    conn = get_db()
    try:
        with conn.cursor() as cur:
            cur.execute(f"SELECT DISTINCT airline_name FROM {view} ORDER BY airline_name")
            airlines = [r[0] for r in cur.fetchall()]
            
            cur.execute(f"SELECT DISTINCT origin_airport FROM {view} ORDER BY origin_airport")
            origins = [r[0] for r in cur.fetchall()]
            
            cur.execute(f"SELECT DISTINCT TO_CHAR(flight_date, 'YYYY-MM-DD') FROM {view} ORDER BY 1 DESC")
            dates = [r[0] for r in cur.fetchall()]
            
            return {"airlines": airlines, "origins": origins, "dates": dates}
    except Exception as e:
        conn.rollback()
        return {"error": str(e)}


# ============================================================
# 6. Obtener Detalles de Vuelos (Explorador)
# ============================================================
def get_flight_details(page=1, limit=10, airline='todos', origin='todos', date='todos'):
    """Obtiene datos detallados de la vista de exploración de vuelos."""
    view = "public.vw_flight_analytics"
    where_sql, params = _build_where_clause(airline=airline, origin=origin, date=date)

    query_count = f"SELECT COUNT(*) FROM {view} {where_sql}"
    query_data = f"""
        SELECT 
            TO_CHAR(flight_date, 'YYYY-MM-DD') as flight_date,
            airline_name,
            origin_airport,
            destination_airport,
            flight_num,
            dep_delay,
            arr_delay,
            cancelled,
            diverted,
            air_time,
            distance
        FROM {view}
        {where_sql}
        ORDER BY flight_date DESC, airline_name, origin_airport, flight_num
        LIMIT %s OFFSET %s
    """

    conn = get_db()
    try:
        with conn.cursor(cursor_factory=psycopg2.extras.DictCursor) as cur:
            cur.execute(query_count, params)
            total = cur.fetchone()[0]

            cur.execute(query_data, params + [limit, (page - 1) * limit])
            data = [dict(row) for row in cur.fetchall()]
            return {"data": data, "totalCount": total}
    except Exception as e:
        conn.rollback()
        return {"error": str(e)}