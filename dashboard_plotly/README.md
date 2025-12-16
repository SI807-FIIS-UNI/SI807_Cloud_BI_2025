# Dashboard BI - SuperMarket Sales

## 📊 Descripción

Dashboard interactivo desarrollado con **HTML5, CSS3 y Plotly.js** que visualiza los 5 KPIs principales del análisis SuperMarket Sales.

## 🎯 KPIs Implementados

### KPI 1: Ventas por Sucursal
- **Gráfico 1:** Ventas mensuales por sucursal (barras agrupadas)
- **Gráfico 6:** Distribución total por ciudad (donut chart)

### KPI 2: Top Productos
- **Gráfico 2:** Ranking de productos por ventas (barras horizontales)
- **Gráfico 5:** Margen bruto por línea de producto (barras horizontales)
- **Gráfico 8:** Calificación por producto (scatter plot)

### KPI 3: Métodos de Pago
- **Gráfico 3:** Distribución de métodos de pago (pie chart)

### KPI 4: Ticket por Cliente
- **Gráfico 4:** Ticket promedio por tipo y género (barras)
- **Gráfico 7:** Ventas por segmentación (barras agrupadas)

## 🚀 Uso

### Opción 1: Abrir directamente
```powershell
start C:\Users\User\Desktop\parte_final\dashboard_plotly\index.html
```

### Opción 2: Servidor local
```powershell
cd C:\Users\User\Desktop\parte_final\dashboard_plotly
python -m http.server 8000
```
Luego abrir: http://localhost:8000

## 📁 Estructura de Archivos

```
dashboard_plotly/
├── index.html      # Estructura HTML del dashboard
├── styles.css      # Estilos visuales profesionales
├── app.js          # Lógica y generación de gráficos
└── README.md       # Esta documentación
```

## 🎨 Características Visuales

- **Diseño moderno:** Gradient backgrounds, glassmorphism effects
- **4 KPI Cards:** Resumen visual con iconos
- **8 Gráficos interactivos:** Diferentes tipos (bar, pie, scatter, donut)
- **Responsive:** Se adapta a diferentes tamaños de pantalla
- **Hover effects:** Animaciones suaves
- **Paleta de colores:** Gradientes púrpura, azul, rosa

## 📊 Tipos de Gráficos

1. **Barras agrupadas** - Comparación temporal
2. **Barras horizontales** - Rankings
3. **Pie/Donut charts** - Distribuciones
4. **Scatter plot** - Correlaciones
5. **Barras con gradiente** - Valores continuos

## ✅ Validación

- Total de gráficos: **8**
- Gráficos por pantalla: **8 (más de 4 requeridos)**
- KPIs cubiertos: **5/5 (100%)**
- Interactividad: ✅ Hover, zoom, pan
- Responsive: ✅ Mobile-friendly

## 🔧 Tecnologías

- **HTML5:** Estructura semántica
- **CSS3:** Gradientes, flexbox, grid, animaciones
- **Plotly.js 2.27.0:** Gráficos interactivos
- **JavaScript ES6:** Lógica moderna

## 📸 Capturas Recomendadas

Para documentación del examen:
1. Vista completa del dashboard (scroll completo)
2. KPI Cards detalle
3. Hover sobre gráficos (tooltips)
4. Responsive en móvil

---

**Desarrollado para:** Examen Final SI807 2025-2  
**Fecha:** 15 Diciembre 2025  
**Arquitectura:** AWS Medallion (Bronze-Plata-Oro)
