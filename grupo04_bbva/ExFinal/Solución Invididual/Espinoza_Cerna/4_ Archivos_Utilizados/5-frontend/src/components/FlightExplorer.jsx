import React, { useState, useEffect, useCallback } from 'react';

const FlightExplorer = () => {
  const [data, setData] = useState([]);
  const [filterOptions, setFilterOptions] = useState({ airlines: [], origins: [], dates: [] });
  const [selectedFilters, setSelectedFilters] = useState({
    airline: 'todos',
    origin: 'todos',
    date: 'todos',
  });
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  const [pagination, setPagination] = useState({
    currentPage: 1,
    totalPages: 1,
    totalCount: 0,
  });

  const fetchData = useCallback(async () => {
    setLoading(true);
    setError('');
    try {
      const params = new URLSearchParams({
        page: pagination.currentPage,
        limit: 10,
        airline: selectedFilters.airline,
        origin: selectedFilters.origin,
        date: selectedFilters.date,
      });
      const response = await fetch(`${import.meta.env.VITE_API_URL}/flights/explore?${params}`);
      if (!response.ok) throw new Error('Error al obtener los datos de los vuelos.');
      
      const result = await response.json();
      setData(result.data);
      setPagination(prev => ({
        ...prev,
        totalCount: result.totalCount,
        totalPages: Math.ceil(result.totalCount / 10),
      }));
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  }, [pagination.currentPage, selectedFilters]);

  const fetchFilters = async () => {
    try {
      const response = await fetch(`${import.meta.env.VITE_API_URL}/flights/filters`);
      if (!response.ok) throw new Error('Error al obtener los filtros.');
      const result = await response.json();
      setFilterOptions(result);
    } catch (err) {
      setError(err.message);
    }
  };

  useEffect(() => {
    fetchFilters();
  }, []);

  useEffect(() => {
    fetchData();
  }, [fetchData]);

  const handleFilterChange = (e) => {
    const { name, value } = e.target;
    setSelectedFilters(prev => ({ ...prev, [name]: value }));
    setPagination(prev => ({ ...prev, currentPage: 1 }));
  };

  const handlePageChange = (newPage) => {
    if (newPage > 0 && newPage <= pagination.totalPages) {
      setPagination(prev => ({ ...prev, currentPage: newPage }));
    }
  };

  const renderFilterDropdown = (name, label, options) => (
    <div className="flex-1">
      <label htmlFor={name} className="block text-sm font-mono text-white/70 mb-1">{label}</label>
      <select
        id={name}
        name={name}
        value={selectedFilters[name]}
        onChange={handleFilterChange}
        className="w-full bg-gray-800 border border-gray-600 text-white rounded-lg p-2 focus:ring-primary focus:border-primary transition"
      >
        <option value="todos">Todos</option>
        {options.map(opt => <option key={opt} value={opt}>{opt}</option>)}
      </select>
    </div>
  );

  return (
    <div className="bg-gray-900/50 border border-gray-700 rounded-xl p-6 backdrop-blur-sm">
      <h2 className="text-2xl font-bold text-white mb-4 font-orbitron">Explorador de Vuelos (Datos Detallados)</h2>
      
      <div className="grid grid-cols-1 md:grid-cols-3 gap-4 mb-6">
        {renderFilterDropdown('airline', 'Aerolínea', filterOptions.airlines)}
        {renderFilterDropdown('origin', 'Aeropuerto de Origen', filterOptions.origins)}
        {renderFilterDropdown('date', 'Fecha', filterOptions.dates)}
      </div>

      {loading && <div className="text-center text-white/70 p-8">Cargando datos...</div>}
      {error && <div className="text-center text-red-500 p-8">{error}</div>}

      {!loading && !error && (
        <>
          <div className="overflow-x-auto">
            <table className="w-full text-left font-mono text-sm">
              <thead className="border-b border-gray-600 text-white/70 uppercase">
                <tr>
                  <th className="p-3">Fecha</th>
                  <th className="p-3">Aerolínea</th>
                  <th className="p-3">Origen</th>
                  <th className="p-3">Destino</th>
                  <th className="p-3 text-right"># Vuelo</th>
                  <th className="p-3 text-right">Retraso Salida (min)</th>
                  <th className="p-3 text-right">Retraso Llegada (min)</th>
                  <th className="p-3 text-center">Cancelado</th>
                </tr>
              </thead>
              <tbody className="text-white">
                {data.map((row, index) => (
                  <tr key={index} className="border-b border-gray-800 hover:bg-gray-800/50">
                    <td className="p-3">{row.flight_date}</td>
                    <td className="p-3">{row.airline_name}</td>
                    <td className="p-3">{row.origin_airport}</td>
                    <td className="p-3">{row.destination_airport}</td>
                    <td className="p-3 text-right">{row.flight_num}</td>
                    <td className="p-3 text-right text-yellow-400">{row.dep_delay}</td>
                    <td className="p-3 text-right text-red-400">{row.arr_delay}</td>
                    <td className="p-3 text-center">{row.cancelled ? 'Sí' : 'No'}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
          {data.length === 0 && <div className="text-center text-white/70 p-8">No se encontraron resultados para los filtros seleccionados.</div>}

          <div className="flex justify-between items-center mt-6 text-white/70">
            <div>
              Página {pagination.currentPage} de {pagination.totalPages} ({pagination.totalCount} registros)
            </div>
            <div className="flex gap-2">
              <button
                onClick={() => handlePageChange(pagination.currentPage - 1)}
                disabled={pagination.currentPage === 1}
                className="px-4 py-2 bg-gray-700 rounded-md disabled:opacity-50"
              >
                Anterior
              </button>
              <button
                onClick={() => handlePageChange(pagination.currentPage + 1)}
                disabled={pagination.currentPage === pagination.totalPages}
                className="px-4 py-2 bg-gray-700 rounded-md disabled:opacity-50"
              >
                Siguiente
              </button>
            </div>
          </div>
        </>
      )}
    </div>
  );
};

export default FlightExplorer;