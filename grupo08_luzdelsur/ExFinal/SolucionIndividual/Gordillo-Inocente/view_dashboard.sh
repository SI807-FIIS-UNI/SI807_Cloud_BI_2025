#!/bin/bash
# Script para visualizar el dashboard de Plotly en el navegador
# Uso: ./view_dashboard.sh

echo "========================================"
echo "  Dashboard Supermarket Sales - Plotly"
echo "========================================"
echo ""

# Directorio del dashboard
DASHBOARD_DIR="dashboard_plotly"

# Verificar que existe el directorio
if [ ! -d "$DASHBOARD_DIR" ]; then
    echo "ERROR: No se encuentra el directorio $DASHBOARD_DIR"
    exit 1
fi

# Verificar que existe index.html
if [ ! -f "$DASHBOARD_DIR/index.html" ]; then
    echo "ERROR: No se encuentra $DASHBOARD_DIR/index.html"
    exit 1
fi

echo "✓ Dashboard encontrado en: $DASHBOARD_DIR"
echo ""

# Iniciar servidor HTTP simple en puerto 8000
echo "Iniciando servidor HTTP local en puerto 8000..."
echo "Dashboard disponible en: http://localhost:8000"
echo ""
echo "Presiona Ctrl+C para detener el servidor"
echo ""

# Cambiar al directorio del dashboard e iniciar servidor
cd "$DASHBOARD_DIR"

# Intentar con Python 3
if command -v python3 &> /dev/null; then
    python3 -m http.server 8000
# Si no, intentar con Python
elif command -v python &> /dev/null; then
    python -m http.server 8000
else
    echo "ERROR: Python no está instalado"
    echo "Alternativa: Abre manualmente el archivo index.html en tu navegador"
    exit 1
fi
