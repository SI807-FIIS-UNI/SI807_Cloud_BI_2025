import React, { useState, useEffect, useMemo } from "react";
import { DateRange } from "react-date-range";
import "react-date-range/dist/styles.css";
import "react-date-range/dist/theme/default.css";
import { es } from "date-fns/locale";
import { addDays, subDays } from "date-fns";
import {
  Activity,
  Calendar,
  Store,
  Users,
  ArrowDown,
  ArrowUp,
  Minus,
} from "lucide-react";
import { useTransactions } from "../contexts/DataContext";

// 2. HELPERS DE FORMATO
const formatCurrency = (value) =>
  new Intl.NumberFormat("es-PE", {
    style: "currency",
    currency: "PEN",
  }).format(value || 0);

const formatNumber = (value) =>
  new Intl.NumberFormat("es-PE", { maximumFractionDigits: 1 }).format(
    value || 0
  );

// --- COMPONENTES UI PARA LA VISTA DE COMPARACIÓN ---

const Card = ({ children, className = "" }) => (
  <div
    className={`bg-white rounded-2xl border border-slate-200 shadow-sm p-6 ${className}`}
  >
    {children}
  </div>
);

const ComparisonKPI = ({ title, valueA, valueB, type = "number" }) => {
  const formatValue = (val) =>
    type === "currency"
      ? formatCurrency(val)
      : type === "percent"
      ? `${formatNumber(val)}%`
      : formatNumber(val);

  const diff = valueA - valueB;
  const diffPercent = valueB !== 0 ? (diff / valueB) * 100 : valueA > 0 ? 100 : 0;

  const DiffIndicator = () => {
    if (Math.abs(diffPercent) < 0.1) {
      return <Minus size={16} className="text-slate-500" />;
    }
    if (diffPercent > 0) {
      return <ArrowUp size={16} className="text-green-500" />;
    }
    return <ArrowDown size={16} className="text-red-500" />;
  };

  return (
    <div className="grid grid-cols-3 items-center py-4 border-b border-slate-100 last:border-b-0">
      <p className="text-sm font-medium text-slate-600 col-span-3 sm:col-span-1">
        {title}
      </p>
      <p className="text-lg font-semibold text-slate-800">
        {formatValue(valueA)}
      </p>
      <div className="flex items-center gap-4">
        <p className="text-lg font-semibold text-slate-800">
          {formatValue(valueB)}
        </p>
        <div className="flex items-center gap-1 bg-slate-100 rounded-full px-2 py-1">
          <DiffIndicator />
          <span className="text-xs font-bold text-slate-600">
            {formatNumber(diffPercent)}%
          </span>
        </div>
      </div>
    </div>
  );
};

const FilterControls = ({
  title,
  filters,
  onFilterChange,
  availableStores,
  availableCategories,
}) => {
  const [showDatePicker, setShowDatePicker] = useState(false);

  return (
    <Card className="p-0">
      <h3 className="text-lg font-semibold text-white bg-blue-600 px-6 py-4">
        {title}
      </h3>
      <div className="p-6">
      <div className="space-y-4">
        {/* Filtro de Tienda */}
        <div className="relative w-full">
          <Store
            size={16}
            className="absolute left-3 top-1/2 -translate-y-1/2 text-slate-400"
          />
          <select
            value={filters.storeId}
            onChange={(e) => onFilterChange("storeId", e.target.value)}
            className="w-full appearance-none bg-slate-50 p-2 pl-9 pr-8 rounded-lg border border-slate-200 text-sm"
          >
            <option value="">Todas las tiendas</option>
            {availableStores.map((storeId) => (
              <option key={storeId} value={storeId}>
                {storeId}
              </option>
            ))}
          </select>
        </div>
        {/* Filtro de Categoría de Cliente */}
        <div className="relative w-full">
          <Users
            size={16}
            className="absolute left-3 top-1/2 -translate-y-1/2 text-slate-400"
          />
          <select
            value={filters.clientCategory}
            onChange={(e) => onFilterChange("clientCategory", e.target.value)}
            className="w-full appearance-none bg-slate-50 p-2 pl-9 pr-8 rounded-lg border border-slate-200 text-sm"
          >
            <option value="">Todas las categorías</option>
            {availableCategories.map((cat) => (
              <option key={cat} value={cat}>
                {cat}
              </option>
            ))}
          </select>
        </div>
        {/* Filtro de Fecha */}
        <div className="relative w-full">
          <button
            onClick={() => setShowDatePicker(!showDatePicker)}
            className="w-full flex items-center justify-start gap-2 bg-slate-50 p-2 px-3 rounded-lg border border-slate-200 text-sm"
          >
            <Calendar size={16} />
            <span>
              {filters.dateRange[0]?.startDate?.toLocaleDateString("es-ES")} -{" "}
              {filters.dateRange[0]?.endDate?.toLocaleDateString("es-ES")}
            </span>
          </button>
          {showDatePicker && (
            <div className="absolute top-full left-0 mt-2 z-10 bg-white rounded-xl shadow-lg border">
              <DateRange
                editableDateInputs={true}
                onChange={(item) => {
                  onFilterChange("dateRange", [item.selection]);
                  setShowDatePicker(false);
                }}
                moveRangeOnFirstSelection={false}
                ranges={filters.dateRange}
                locale={es}
              />
            </div>
          )}
        </div>
      </div>
      </div>
    </Card>
  );
};

// --- VISTA PRINCIPAL DE COMPARACIÓN ---

export default function ComparisonView() {
  const { allTransactions, loading } = useTransactions();

  // Dos estados de filtros, uno para cada conjunto a comparar
  const [filtersA, setFiltersA] = useState({
    dateRange: [
      {
        startDate: new Date("2023-05-01T00:00:00"),
        endDate: new Date("2023-05-31T23:59:59"),
        key: "selection",
      },
    ],
    storeId: "",
    clientCategory: "",
  });
  const [filtersB, setFiltersB] = useState({
    dateRange: [
      {
        startDate: new Date("2023-04-01T00:00:00"),
        endDate: new Date("2023-04-30T23:59:59"),
        key: "selection",
      },
    ],
    storeId: "",
    clientCategory: "",
  });

  // --- Lógica de Filtrado y Cálculo ---

  const { availableStores, availableCategories } = useMemo(() => {
    const stores = [...new Set(allTransactions.map((tx) => tx.tienda_id))].filter(Boolean);
    const categories = [...new Set(allTransactions.map((tx) => tx.categoria_cliente))].filter(Boolean);
    return {
      availableStores: stores.sort(),
      availableCategories: categories.sort(),
    };
  }, [allTransactions]);

  const calculateKpis = (transactions, filters) => {
    const { dateRange, storeId, clientCategory } = filters;
    const { startDate, endDate } = dateRange[0] || {};

    const filtered = transactions.filter((tx) => {
      if (!startDate || !endDate || tx.date < startDate || tx.date > endDate) return false;
      if (storeId && tx.tienda_id !== storeId) return false;
      if (clientCategory && tx.categoria_cliente !== clientCategory) return false;
      return true;
    });

    const totalTransactions = filtered.length;
    if (totalTransactions === 0) {
      return { totalRevenue: 0, averageTicket: 0, totalTransactions: 0, totalUnits: 0, discountRate: 0 };
    }

    const totalRevenue = filtered.reduce((sum, tx) => sum + tx.monto_total, 0);
    const totalUnits = filtered.reduce((sum, tx) => sum + tx.total_unidades, 0);
    const discountTransactions = filtered.filter((tx) => tx.descuento_aplicado).length;

    return {
      totalRevenue,
      totalTransactions,
      averageTicket: totalRevenue / totalTransactions,
      totalUnits,
      discountRate: (discountTransactions / totalTransactions) * 100,
    };
  };

  const kpisA = useMemo(() => calculateKpis(allTransactions, filtersA), [allTransactions, filtersA]);
  const kpisB = useMemo(() => calculateKpis(allTransactions, filtersB), [allTransactions, filtersB]);

  // Handlers para actualizar los filtros
  const handleFilterAChange = (key, value) => {
    setFiltersA((prev) => ({ ...prev, [key]: value }));
  };
  const handleFilterBChange = (key, value) => {
    setFiltersB((prev) => ({ ...prev, [key]: value }));
  };

  if (loading) {
    return (
      <div className="min-h-screen flex items-center justify-center bg-slate-50">
        <div className="animate-pulse flex flex-col items-center text-blue-600">
          <Activity size={48} className="mb-4 animate-spin" />
          <span className="font-medium text-lg">Cargando datos...</span>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-slate-50 p-6 md:p-10 font-sans">
      <header className="mb-10">
        <h1 className="text-3xl font-bold text-slate-900 tracking-tight">
          Dashboard Comparativo
        </h1>
        <p className="text-slate-500 mt-1">
          Compara dos segmentos de datos para encontrar insights.
        </p>
      </header>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
        {/* Columna de Filtros A */}
        <FilterControls
          title="Comparación A"
          filters={filtersA}
          onFilterChange={handleFilterAChange}
          availableStores={availableStores}
          availableCategories={availableCategories}
        />

        {/* Columna de Filtros B */}
        <FilterControls
          title="Comparación B"
          filters={filtersB}
          onFilterChange={handleFilterBChange}
          availableStores={availableStores}
          availableCategories={availableCategories}
        />
      </div>

      {/* Sección de Resultados */}
      <div className="mt-10">
        <Card>
          <div className="grid grid-cols-3 items-center p-4 rounded-lg bg-slate-100 border-b-2 border-slate-200">
            <h4 className="text-sm font-bold text-slate-600 uppercase tracking-wider col-span-3 sm:col-span-1">
              Métrica
            </h4>
            <h4 className="text-sm font-bold text-slate-600 uppercase tracking-wider">
              Comparación A
            </h4>
            <h4 className="text-sm font-bold text-slate-600 uppercase tracking-wider">
              Comparación B
            </h4>
          </div>
          <ComparisonKPI
            title="Revenue Total"
            valueA={kpisA.totalRevenue}
            valueB={kpisB.totalRevenue}
            type="currency"
          />
          <ComparisonKPI
            title="Ticket Promedio"
            valueA={kpisA.averageTicket}
            valueB={kpisB.averageTicket}
            type="currency"
          />
          <ComparisonKPI
            title="Total Transacciones"
            valueA={kpisA.totalTransactions}
            valueB={kpisB.totalTransactions}
            type="number"
          />
          <ComparisonKPI
            title="Total Unidades"
            valueA={kpisA.totalUnits}
            valueB={kpisB.totalUnits}
            type="number"
          />
          <ComparisonKPI
            title="% Trx con Descuento"
            valueA={kpisA.discountRate}
            valueB={kpisB.discountRate}
            type="percent"
          />
        </Card>
      </div>
    </div>
  );
}
