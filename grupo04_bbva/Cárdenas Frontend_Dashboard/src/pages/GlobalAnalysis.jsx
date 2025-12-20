import React, { useState, useEffect, useMemo } from "react";
import { DateRange } from "react-date-range";
import "react-date-range/dist/styles.css";
import "react-date-range/dist/theme/default.css";
import { es } from "date-fns/locale";
import { addDays, format } from "date-fns";
import {
  LineChart,
  Line,
  Area,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  ResponsiveContainer,
  RadarChart,
  PolarGrid,
  PolarAngleAxis,
  PolarRadiusAxis,
  Radar,
  Legend,
  ScatterChart,
  Scatter,
  ZAxis,
} from "recharts";
import { Activity, Calendar, Store } from "lucide-react";
import { useTransactions } from "../contexts/DataContext"; // Importa el hook

const formatCurrency = (value) =>
  new Intl.NumberFormat("es-PE", { style: "currency", currency: "PEN" }).format(value || 0);

const formatNumber = (value) =>
  new Intl.NumberFormat("es-PE", { maximumFractionDigits: 1 }).format(value || 0);

const Card = ({ children, className = "" }) => (
  <div className={`bg-white rounded-2xl border border-slate-200 shadow-sm p-6 ${className}`}>
    {children}
  </div>
);

// --- COMPONENTES DE GRÁFICOS PARA ESTA VISTA ---

const RevenueTrendChart = ({ data }) => (
  <Card className="col-span-1 lg:col-span-2">
    <h3 className="text-lg font-semibold text-slate-800 mb-4">Tendencia de Ingresos</h3>
    <div className="h-80">
      <ResponsiveContainer width="100%" height="100%" minWidth={0} minHeight={0}>
        <LineChart data={data} margin={{ top: 5, right: 20, left: 20, bottom: 5 }}>
          <CartesianGrid strokeDasharray="3 3" stroke="#E2E8F0" />
          <XAxis dataKey="date" tick={{ fontSize: 12 }} />
          <YAxis tickFormatter={(value) => formatCurrency(value)} tick={{ fontSize: 12 }} />
          <Tooltip contentStyle={{ borderRadius: "8px", border: "none" }} formatter={(value) => [formatCurrency(value), "Ingresos"]} />
          <defs>
            <linearGradient id="colorRevenue" x1="0" y1="0" x2="0" y2="1">
              <stop offset="5%" stopColor="#2563EB" stopOpacity={0.8} />
              <stop offset="95%" stopColor="#2563EB" stopOpacity={0} />
            </linearGradient>
          </defs>
          <Area type="monotone" dataKey="revenue" stroke="none" fill="url(#colorRevenue)" />
          <Line type="monotone" dataKey="revenue" stroke="#2563EB" strokeWidth={2} dot={false} />
        </LineChart>
      </ResponsiveContainer>
    </div>
  </Card>
);

const SalesByDayOfWeekChart = ({ data }) => (
  <Card>
    <h3 className="text-lg font-semibold text-slate-800 mb-4">Ventas por Día de la Semana</h3>
    <div className="h-80">
      <ResponsiveContainer width="100%" height="100%" minWidth={0} minHeight={0}>
        <RadarChart cx="50%" cy="50%" outerRadius="80%" data={data}>
          <PolarGrid />
          <PolarAngleAxis dataKey="day" tick={{ fontSize: 12 }} />
          <PolarRadiusAxis angle={30} domain={[0, 'dataMax']} tick={false} axisLine={false} />
          <Radar name="Ingresos" dataKey="revenue" stroke="#0EA5E9" fill="#0EA5E9" fillOpacity={0.6} />
          <Tooltip formatter={(value) => formatCurrency(value)} />
        </RadarChart>
      </ResponsiveContainer>
    </div>
  </Card>
);

const ClientCategoryBubbleChart = ({ data, colors }) => (
  <Card className="col-span-1 lg:col-span-3">
    <h3 className="text-lg font-semibold text-slate-800 mb-4">Análisis de Categorías de Cliente</h3>
    <div className="h-96">
      <ResponsiveContainer width="100%" height="100%" minWidth={0} minHeight={0}>
        <ScatterChart margin={{ top: 20, right: 20, bottom: 60, left: 60 }}>
          <CartesianGrid strokeDasharray="3 3" stroke="#E2E8F0" />
          <XAxis type="number" dataKey="transactions" name="Transacciones" tick={{ fontSize: 12 }} label={{ value: "Total Transacciones", position: 'insideBottom', offset: -25 }} />
          <YAxis type="number" dataKey="avgTicket" name="Ticket Promedio" tickFormatter={formatCurrency} tick={{ fontSize: 12 }} label={{ value: "Ticket Promedio", angle: -90, position: 'insideLeft', offset: -40 }} />
          <ZAxis type="number" dataKey="revenue" range={[100, 2000]} name="Revenue" />
          <Tooltip cursor={{ strokeDasharray: '3 3' }} content={<CustomTooltip />} />
          <Legend verticalAlign="bottom" height={36} iconType="circle" />
          {data.map((entry, index) => (
            <Scatter key={entry.category} name={entry.category} data={[entry]} fill={colors[index % colors.length]} shape="circle" />
          ))}
        </ScatterChart>
      </ResponsiveContainer>
    </div>
  </Card>
);

const CustomTooltip = ({ active, payload }) => {
  if (active && payload && payload.length) {
    const data = payload[0].payload;
    return (
      <div className="bg-white p-4 rounded-lg shadow-lg border border-slate-200">
        <p className="font-bold text-slate-800">{data.category}</p>
        <p className="text-sm text-slate-600">Revenue: {formatCurrency(data.revenue)}</p>
        <p className="text-sm text-slate-600">Transacciones: {formatNumber(data.transactions)}</p>
        <p className="text-sm text-slate-600">Ticket Promedio: {formatCurrency(data.avgTicket)}</p>
      </div>
    );
  }
  return null;
};


// --- VISTA PRINCIPAL DE ANÁLISIS GLOBAL ---

export default function GlobalAnalysisView() {
  // Obtenemos los datos y el estado de carga desde el contexto
  const { allTransactions, loading } = useTransactions();
  const [showDatePicker, setShowDatePicker] = useState(false);
  const [selectedStoreId, setSelectedStoreId] = useState(""); // "" = Todas las tiendas
  const [dateRange, setDateRange] = useState([
    {
      startDate: new Date("2023-05-01T00:00:00"),
      endDate: new Date("2023-05-31T23:59:59"),
      key: "selection",
    },
  ]);

  const filteredTransactions = useMemo(() => {
    const { startDate, endDate } = dateRange[0] || {};
    if (!startDate || !endDate) return [];
    return allTransactions.filter(tx => {
      const isDateInRange = tx.date >= startDate && tx.date <= endDate;
      if (!isDateInRange) return false;

      if (selectedStoreId && tx.tienda_id !== selectedStoreId) {
        return false;
      }
      return true;
    });
  }, [allTransactions, dateRange, selectedStoreId]);

  const availableStores = useMemo(() => [...new Set(allTransactions.map(tx => tx.tienda_id))].filter(Boolean).sort(), [allTransactions]);

  // --- Preparación de datos para cada gráfico ---

  const trendData = useMemo(() => {
    const dailyRevenue = filteredTransactions.reduce((acc, tx) => {
      const dateStr = format(tx.date, 'yyyy-MM-dd');
      acc[dateStr] = (acc[dateStr] || 0) + tx.monto_total;
      return acc;
    }, {});
    return Object.entries(dailyRevenue).map(([date, revenue]) => ({ date, revenue })).sort((a, b) => new Date(a.date) - new Date(b.date));
  }, [filteredTransactions]);

  const salesByDayData = useMemo(() => {
    const dayMap = {
      Sunday: "Domingo", Monday: "Lunes", Tuesday: "Martes", Wednesday: "Miércoles",
      Thursday: "Jueves", Friday: "Viernes", Saturday: "Sábado"
    };
    const daysOfWeekOrder = ["Domingo", "Lunes", "Martes", "Miércoles", "Jueves", "Viernes", "Sábado"];
    const dayRevenue = {
      Domingo: 0, Lunes: 0, Martes: 0, Miércoles: 0,
      Jueves: 0, Viernes: 0, Sábado: 0
    };
    
    filteredTransactions.forEach(tx => {
        const dayNameInEnglish = tx.dia_semana_nombre;
        const dayNameInSpanish = dayMap[dayNameInEnglish];
        if(dayNameInSpanish) {
            dayRevenue[dayNameInSpanish] += tx.monto_total;
        }
    });

    // Mapear a un formato que el gráfico entienda y mantener el orden
    return daysOfWeekOrder.map(day => ({
      day, revenue: dayRevenue[day]
    }));
  }, [filteredTransactions]);

  const clientCategoryData = useMemo(() => {
    const categories = {};
    filteredTransactions.forEach(tx => {
      const cat = tx.categoria_cliente || "Sin Categoría";
      if (!categories[cat]) {
        categories[cat] = { revenue: 0, transactions: 0, count: 0 };
      }
      categories[cat].revenue += tx.monto_total;
      categories[cat].transactions++;
    });
    return Object.entries(categories).map(([category, data]) => ({
      category,
      revenue: data.revenue,
      transactions: data.transactions,
      avgTicket: data.revenue / data.transactions,
    }));
  }, [filteredTransactions]);

  const categoryColors = useMemo(() => {
    return ["#2563EB", "#0EA5E9", "#F59E0B", "#10B981", "#8B5CF6", "#EC4899"];
  }, []);

  if (loading) {
    return (
      <div className="min-h-screen flex items-center justify-center bg-slate-50">
        <div className="animate-pulse flex flex-col items-center text-blue-600">
          <Activity size={48} className="mb-4 animate-spin" />
          <span className="font-medium text-lg">Cargando análisis...</span>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-slate-50 p-6 md:p-10 font-sans">
      <header className="flex flex-col md:flex-row justify-between items-start md:items-center mb-10 gap-4">
        <div>
          <h1 className="text-3xl font-bold text-slate-900 tracking-tight">
            Análisis Global del Negocio
          </h1>
          <p className="text-slate-500 mt-1">
            Visualizaciones avanzadas de todas las transacciones.
          </p>
        </div>
        <div className="flex flex-col sm:flex-row items-stretch sm:items-center gap-4 w-full sm:w-auto">
          {/* Filtro de Tienda */}
          <div className="relative w-full sm:w-auto">
            <Store size={18} className="absolute left-3 top-1/2 -translate-y-1/2 text-slate-400 pointer-events-none" />
            <select
              value={selectedStoreId}
              onChange={(e) => setSelectedStoreId(e.target.value)}
              className="w-full appearance-none bg-white p-2 pl-9 pr-8 rounded-xl shadow-sm border border-slate-200 text-sm font-semibold text-slate-700 hover:bg-slate-100 transition-colors focus:outline-none focus:ring-2 focus:ring-blue-500"
            >
              <option value="">Todas las tiendas</option>
              {availableStores.map((storeId) => (
                <option key={storeId} value={storeId}>
                  {storeId}
                </option>
              ))}
            </select>
          </div>
          {/* Filtro de Fecha */}
          <div className="relative">
            <button
              onClick={() => setShowDatePicker(!showDatePicker)}
              className="w-full flex items-center justify-center sm:justify-start gap-2 bg-white p-2 px-4 rounded-xl shadow-sm border border-slate-200 text-sm font-semibold text-slate-700 hover:bg-slate-100 transition-colors"
            >
              <Calendar size={18} />
              <span>
                {dateRange[0]?.startDate?.toLocaleDateString("es-ES")} -{" "}
                {dateRange[0]?.endDate?.toLocaleDateString("es-ES")}
              </span>
            </button>
            {showDatePicker && (
              <div className="absolute top-full right-0 mt-2 z-10 bg-white rounded-xl shadow-lg border">
                <DateRange
                  editableDateInputs={true}
                  onChange={(item) => { setDateRange([item.selection]); setShowDatePicker(false); }}
                  moveRangeOnFirstSelection={false}
                  ranges={dateRange}
                  locale={es}
                />
              </div>
            )}
          </div>
        </div>
      </header>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
        <RevenueTrendChart data={trendData} />
        <SalesByDayOfWeekChart data={salesByDayData} />
        <ClientCategoryBubbleChart data={clientCategoryData} colors={categoryColors} />
      </div>
    </div>
  );
}
