import React, { useState, useEffect, useMemo } from "react";
import { DateRange } from "react-date-range";
import "react-date-range/dist/styles.css"; // main style file
import "react-date-range/dist/theme/default.css"; // theme css file
import { es } from "date-fns/locale";
import { addDays } from "date-fns";
import {
  BarChart,
  Bar,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  PieChart,
  Pie,
  Cell,
  LineChart,
  Line,
  ResponsiveContainer,
} from "recharts";
import {
  DollarSign,
  ShoppingCart,
  TrendingUp,
  Package,
  Hash,
  Store,
  Users,
  Activity,
  Calendar,
} from "lucide-react";
import { useTransactions } from "../contexts/DataContext";

// --- 1. CONSTANTES Y CONFIGURACIÓN ---
const THEME = {
  colors: {
    primary: "#2563EB", // Blue-600
    primaryLight: "#3B82F6", // Blue-500
    secondary: "#64748B", // Slate-500
    accent: "#0EA5E9", // Sky-500
    background: "#F8FAFC", // Slate-50
    cardBg: "#FFFFFF",
    textMain: "#0F172A", // Slate-900
    textMuted: "#64748B", // Slate-500
    border: "#E2E8F0", // Slate-200
    success: "#10B981",
    chartPalette: ["#2563EB", "#3B82F6", "#60A5FA", "#93C5FD", "#BFDBFE"],
  },
  layout: {
    borderRadius: "1rem",
    padding: "1.5rem",
    gap: "1.5rem",
    iconSize: 20,
  },
};

// --- 4. COMPONENTES UI REUTILIZABLES ---

const formatCurrency = (value) => {
  return new Intl.NumberFormat("es-PE", {
    style: "currency",
    currency: "PEN",
  }).format(value || 0);
};

const formatNumber = (value) => {
  return new Intl.NumberFormat("es-PE", { maximumFractionDigits: 1 }).format(
    value || 0
  );
};

const Card = ({ children, className = "" }) => (
  <div
    className={`bg-white rounded-2xl border border-slate-200 shadow-sm p-6 ${className}`}
  >
    {children}
  </div>
);

const KPISmallCard = ({
  title,
  value,
  subValue,
  icon: Icon,
  type = "number",
}) => {
  const displayValue =
    type === "currency"
      ? formatCurrency(value)
      : type === "percent"
      ? `${formatNumber(value)}%`
      : formatNumber(value);

  return (
    <Card className="flex items-start justify-between transition-all hover:shadow-md">
      <div>
        <p className="text-sm font-medium text-slate-500 mb-1">{title}</p>
        <h3 className="text-2xl font-bold text-slate-900">{displayValue}</h3>
        {subValue && <p className="text-xs text-slate-400 mt-1">{subValue}</p>}
      </div>
      <div className="p-3 bg-blue-50 rounded-xl">
        <Icon size={THEME.layout.iconSize} className="text-blue-600" />
      </div>
    </Card>
  );
};

const RevenueStoreChart = ({ data }) => {
  const chartData = Array.isArray(data) ? data : [];

  return (
    <Card className="col-span-1 lg:col-span-2">
      <div className="flex justify-between items-center mb-6">
        <h4 className="text-lg font-semibold text-slate-800">
          Top Tiendas por Ingresos
        </h4>
        <Store size={20} className="text-slate-400" />
      </div>
      <div className="h-64 w-full">
        {chartData.length > 0 ? (
          <ResponsiveContainer width="100%" height="100%" minWidth={0} minHeight={0}>
            <BarChart
              data={chartData}
              layout="vertical"
              margin={{ top: 5, right: 30, left: 40, bottom: 5 }}
            >
              <CartesianGrid
                strokeDasharray="3 3"
                horizontal={false}
                stroke="#E2E8F0"
              />
              <XAxis type="number" hide />
              <YAxis
                type="category"
                dataKey="name"
                tick={{ fill: "#64748B", fontSize: 12 }}
                width={80}
              />
              <Tooltip
                cursor={{ fill: "transparent" }}
                contentStyle={{
                  borderRadius: "8px",
                  border: "none",
                  boxShadow: "0 4px 6px -1px rgb(0 0 0 / 0.1)",
                }}
                formatter={(value) => [formatCurrency(value), "Ingresos"]}
              />
              <Bar
                dataKey="value"
                fill={THEME.colors.primary}
                radius={[0, 4, 4, 0]}
                barSize={20}
              />
            </BarChart>
          </ResponsiveContainer>
        ) : (
          <div className="flex h-full items-center justify-center text-slate-400 text-sm">
            No hay datos de tiendas
          </div>
        )}
      </div>
    </Card>
  );
};

const GaugeChartCard = ({
  title,
  value,
  maxValue = 100,
  type = "number",
  color,
}) => {
  const percent = maxValue > 0 ? (value / maxValue) * 100 : 0;
  const safePercent = Math.min(Math.max(percent || 0, 0), 100);
  const data = [
    { name: "value", value: safePercent },
    { name: "remaining", value: 100 - safePercent },
  ];

  const displayValue =
    type === "currency"
      ? formatCurrency(value)
      : type === "percent"
      ? `${formatNumber(value)}%`
      : formatNumber(value);

  return (
    <Card className="flex flex-col items-center justify-between">
      <h4 className="text-sm font-medium text-slate-500 mb-4 w-full text-left">
        {title}
      </h4>
      <div className="h-32 w-32 relative">
        <ResponsiveContainer width="100%" height="100%" minWidth={0} minHeight={0}>
          <PieChart>
            <Pie data={data} cx="50%" cy="50%" innerRadius={45} outerRadius={60} startAngle={90} endAngle={-270} dataKey="value" stroke="none">
              <Cell fill={color || THEME.colors.primary} />
              <Cell fill={THEME.colors.border} />
            </Pie>
          </PieChart>
        </ResponsiveContainer>
        <div className="absolute inset-0 flex items-center justify-center flex-col">
          <span className="text-2xl font-bold text-slate-800">
            {displayValue}
          </span>
        </div>
      </div>
    </Card>
  );
};

const MonthlyRevenueTrendChart = ({
  data,
  years,
  selectedYear,
  onYearChange,
  stores,
  selectedStore,
  onStoreChange,
}) => {
  const chartData = data[selectedYear] || [];

  return (
    <Card className="col-span-1 md:col-span-2 lg:col-span-4">
      <div className="flex flex-col sm:flex-row justify-between items-start sm:items-center mb-6 gap-4">
        <h4 className="text-lg font-semibold text-slate-800">
          Tendencia de Ingresos Mensuales
        </h4>
        <div className="flex gap-2">
          <select
            value={selectedStore}
            onChange={(e) => onStoreChange(e.target.value)}
            className="bg-slate-50 p-2 rounded-lg border border-slate-200 text-sm font-semibold text-slate-700 focus:outline-none focus:ring-2 focus:ring-blue-500"
          >
            <option value="">Todas las tiendas</option>
            {stores.map((store) => (
              <option key={store} value={store}>
                {store}
              </option>
            ))}
          </select>
          <select
            value={selectedYear}
            onChange={(e) => onYearChange(e.target.value)}
            className="bg-slate-50 p-2 rounded-lg border border-slate-200 text-sm font-semibold text-slate-700 focus:outline-none focus:ring-2 focus:ring-blue-500"
          >
            {years.map((year) => (
              <option key={year} value={year}>
                Año {year}
              </option>
            ))}
          </select>
        </div>
      </div>
      <div className="h-72 w-full">
        <ResponsiveContainer width="100%" height="100%" minWidth={0} minHeight={0}>
          <LineChart data={chartData} margin={{ top: 5, right: 20, left: 20, bottom: 5 }}>
            <CartesianGrid strokeDasharray="3 3" stroke={THEME.colors.border} />
            <XAxis dataKey="month" tick={{ fontSize: 12 }} />
            <YAxis tickFormatter={(value) => `${formatCurrency(value / 1000)}k`} tick={{ fontSize: 12 }} />
            <Tooltip
              formatter={(value) => [formatCurrency(value), "Ingresos"]}
              contentStyle={{ borderRadius: "8px", border: "none", boxShadow: "0 4px 6px -1px rgb(0 0 0 / 0.1)" }}
            />
            <Line type="monotone" dataKey="revenue" stroke={THEME.colors.primary} strokeWidth={2} dot={{ r: 4 }} activeDot={{ r: 6 }} />
          </LineChart>
        </ResponsiveContainer>
      </div>
    </Card>
  );
};

// --- 5. VISTA PRINCIPAL (CLIENT ANALYSIS) ---

export default function ClientAnalysisView() {
  const { allTransactions, loading } = useTransactions();
  const [showDatePicker, setShowDatePicker] = useState(false);
  const [selectedStoreId, setSelectedStoreId] = useState(""); // "" = Todas las tiendas
  const [monthlyChartStoreId, setMonthlyChartStoreId] = useState("");
  const [selectedYear, setSelectedYear] = useState(new Date().getFullYear());
  const [dateRange, setDateRange] = useState([
    {
      startDate: addDays(new Date(), -30),
      endDate: new Date(),
      key: "selection",
    },
  ]);

  useEffect(() => {
    const loadData = async () => {
      // Establecer un rango de fechas inicial por defecto (últimos 30 días)
      if (allTransactions.length > 0) {
        // Usamos reduce para evitar "Maximum call stack size exceeded" en arrays grandes
        const dateValues = allTransactions.map((t) => t.date.getTime()).filter(t => !isNaN(t));
        const maxTimestamp = dateValues.reduce((a, b) => Math.max(a, b), -Infinity);
        const minTimestamp = dateValues.reduce((a, b) => Math.min(a, b), Infinity);

        const maxDate = new Date(maxTimestamp);
        let minDate = addDays(maxDate, -30);

        // Asegurarse de que la fecha de inicio no sea anterior a la primera transacción
        const firstTransactionDate = new Date(minTimestamp);
        if (minDate < firstTransactionDate) minDate = firstTransactionDate;

        setDateRange([{ startDate: minDate, endDate: maxDate, key: "selection" }]);
      }
    };
    loadData();
  }, [allTransactions, loading]);

  // --- Lógica de Filtrado y Cálculo de KPIs ---
  const filteredTransactions = useMemo(() => {
    const { startDate, endDate } = dateRange[0] || {};
    if (!startDate || !endDate) return [];

    return allTransactions.filter((tx) => {
      // Filtro de Fecha
      const txDate = tx.date;
      const isDateInRange = txDate >= startDate && txDate <= endDate;
      if (!isDateInRange) return false;

      // Filtro de Tienda
      if (selectedStoreId && tx.tienda_id !== selectedStoreId) {
        return false;
      }

      return true;
    });
  }, [allTransactions, dateRange, selectedStoreId]);

  const availableStores = useMemo(() => {
    // Usamos la ciudad como el identificador de la tienda
    const storeIds = [...new Set(allTransactions.map((tx) => tx.tienda_id))].filter(Boolean);
    return storeIds.sort((a, b) => a - b);
  }, [allTransactions]);
  
  const { monthlyData, availableYears } = useMemo(() => {
    // Primero, filtramos las transacciones por tienda si hay una seleccionada.
    const transactionsForChart = monthlyChartStoreId
      ? allTransactions.filter(tx => tx.tienda_id === monthlyChartStoreId)
      : allTransactions;

    if (transactionsForChart.length === 0) {
      return { monthlyData: {}, availableYears: [] };
    }

    const dataByYear = transactionsForChart.reduce((acc, tx) => {
      if (!tx.date || isNaN(tx.date.getTime())) return acc;
      const year = tx.date.getFullYear();
      const month = tx.date.getMonth(); // 0-11
      if (!acc[year]) {
        acc[year] = Array(12).fill(0);
      }
      acc[year][month] += tx.monto_total || 0;
      return acc;
    }, {});

    const monthLabels = ["Ene", "Feb", "Mar", "Abr", "May", "Jun", "Jul", "Ago", "Sep", "Oct", "Nov", "Dic"];
    const finalData = {};
    for (const year in dataByYear) {
      finalData[year] = dataByYear[year].map((revenue, index) => ({
        month: monthLabels[index],
        revenue,
      }));
    }

    const years = Object.keys(finalData).sort((a, b) => b - a);
    if (years.length > 0 && !years.includes(String(selectedYear))) {
      setSelectedYear(years[0]);
    }

    return { monthlyData: finalData, availableYears: years };
  }, [allTransactions, monthlyChartStoreId]);

  const globalKpis = useMemo(() => {
    const txs = filteredTransactions;
    const totalTransactions = txs.length;

    if (totalTransactions === 0) {
      return {
        totalRevenue: 0,
        totalTransactions: 0,
        averageTicket: 0,
        totalUnits: 0,
        averagePrice: 0,
        discountRate: 0,
        revenueByStore: [],
        maxAveragePrice: 0,
      };
    }

    const totalRevenue = txs.reduce((sum, tx) => sum + tx.monto_total, 0);
    const totalUnits = txs.reduce((sum, tx) => sum + tx.total_unidades, 0);
    const discountTransactions = txs.filter((tx) => tx.descuento_aplicado).length;

    const revenueByStoreMap = txs.reduce((acc, tx) => {
      const storeName = tx.tienda_id; // Ahora es la ciudad
      acc[storeName] = (acc[storeName] || 0) + tx.monto_total;
      return acc;
    }, {});

    const revenueByStore = Object.entries(revenueByStoreMap)
      .map(([name, value]) => ({ name, value }))
      .sort((a, b) => b.value - a.value)
      .slice(0, 10);

    // Usamos reduce para evitar "Maximum call stack size exceeded"
    const maxAveragePrice = allTransactions.length > 0
      ? allTransactions.reduce((max, tx) => Math.max(max, tx.precio_promedio_unitario || 0), 0)
      : 0;

    return {
      totalRevenue,
      totalTransactions,
      averageTicket: totalRevenue / totalTransactions,
      totalUnits,
      averagePrice: totalRevenue / totalUnits,
      discountRate: (discountTransactions / totalTransactions) * 100,
      revenueByStore,
      maxAveragePrice,
    };
  }, [filteredTransactions, allTransactions]);

  if (loading) {
    return (
      <div className="min-h-screen flex items-center justify-center bg-slate-50 text-blue-600">
        <div className="animate-pulse flex flex-col items-center">
          <Activity size={48} className="mb-4 animate-spin" />
          <span className="font-medium text-lg">
            Procesando transacciones...
          </span>
        </div>
      </div>
    );
  }

  if (allTransactions.length === 0)
    return (
      <div className="min-h-screen bg-slate-50 flex items-center justify-center p-8 text-center text-slate-500">
        <div>
          <p className="text-lg font-semibold">No se encontraron datos.</p>
          <p className="text-sm mt-2">
            Revisa la conexión al Data Lake o el formato del JSON.
          </p>
        </div>
      </div>
    );

  return (
    <div className="min-h-screen bg-slate-50 p-6 md:p-10 font-sans text-slate-900">
      {/* Header & Controls */}
      <header className="flex flex-col md:flex-row justify-between items-start md:items-center mb-10 gap-4">
        <div>
          <h1 className="text-3xl font-bold text-slate-900 tracking-tight">
            Análisis Global de Transacciones
          </h1>
          <p className="text-slate-500 mt-1">
            Analizando {formatNumber(globalKpis.totalTransactions)} de{" "}
            {formatNumber(allTransactions.length)} transacciones.
          </p>
        </div>
        <div className="flex flex-col sm:flex-row items-stretch sm:items-center gap-4 w-full sm:w-auto">
          {/* Filtro de Tienda */}
          <div className="relative w-full sm:w-auto">
            <Store
              size={18}
              className="absolute left-3 top-1/2 -translate-y-1/2 text-slate-400 pointer-events-none"
            />
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
          <div className="relative w-full sm:w-auto">
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
              <div className="absolute top-full right-0 mt-2 z-10 bg-white rounded-xl shadow-lg border border-slate-200">
                <DateRange
                  editableDateInputs={true}
                  onChange={(item) => {
                    setDateRange([item.selection]);
                    setShowDatePicker(false); // Opcional: cerrar al seleccionar
                  }}
                  moveRangeOnFirstSelection={false}
                  ranges={dateRange}
                  locale={es}
                />
              </div>
            )}
          </div>
        </div>
      </header>

      {/* Grid Layout (Bento Grid) */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
        <KPISmallCard
          title="Revenue Total"
          value={globalKpis.totalRevenue}
          icon={DollarSign}
          type="currency"
        />
        <KPISmallCard
          title="Ticket Promedio"
          value={globalKpis.averageTicket}
          icon={TrendingUp}
          type="currency"
        />
        <KPISmallCard
          title="Transacciones"
          value={globalKpis.totalTransactions}
          icon={Hash}
          type="number"
        />
        <KPISmallCard
          title="Unidades Vendidas"
          value={globalKpis.totalUnits}
          icon={Package}
          type="number"
        />

        <RevenueStoreChart data={globalKpis.revenueByStore} />

        <GaugeChartCard
          title="Precio Promedio Item"
          value={globalKpis.averagePrice}
          maxValue={globalKpis.maxAveragePrice}
          type="currency"
          color={THEME.colors.primary}
        />
        <GaugeChartCard
          title="% Trx con Descuento"
          value={globalKpis.discountRate}
          type="percent"
          color={THEME.colors.accent}
        />

        <MonthlyRevenueTrendChart
          data={monthlyData}
          years={availableYears}
          stores={availableStores}
          selectedYear={selectedYear}
          onYearChange={setSelectedYear}
          selectedStore={monthlyChartStoreId}
          onStoreChange={setMonthlyChartStoreId}
        />
      </div>
    </div>
  );
}
