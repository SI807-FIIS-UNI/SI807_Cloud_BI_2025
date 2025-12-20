import React, { createContext, useState, useEffect, useContext } from "react";

// 1. Definir la URL y las funciones de carga/adaptación aquí
const DATA_SOURCE_URL =
  "https://azdatalakefinal.blob.core.windows.net/oro/kpis/kpis.json?se=2026-01-01T00%3A00%3A00Z&sp=r&spr=https&sv=2022-11-02&sr=b&sig=Y9ETUHs%2BBK0yTlxLlrq4Rb0eqUvgrC7ZJhugtvVn4xk%3D";

const fetchTransactionsData = async () => {
  try {
    const response = await fetch(DATA_SOURCE_URL);
    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }
    const textData = await response.text();
    return textData
      .trim()
      .split("\n")
      .map((line) => {
        try {
          return JSON.parse(line);
        } catch {
          return null;
        }
      })
      .filter(Boolean);
  } catch (error) {
    console.error("Error al obtener los datos de transacciones:", error);
    return [];
  }
};

const adaptTransactionData = (transactions) => {
  if (!Array.isArray(transactions)) return [];
  return transactions.map((tx) => ({
    ...tx,
    ...tx.tiempo,
    ...tx.cliente,
    ...tx.tienda,
    ...tx.kpis,
    date: new Date(tx.tiempo?.fecha),
    tienda_id: tx.tienda?.ciudad,
  }));
};

// 2. Crear el Contexto
const DataContext = createContext();

// 3. Crear el Proveedor (Provider) que contendrá la lógica
export const DataProvider = ({ children }) => {
  const [allTransactions, setAllTransactions] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const loadData = async () => {
      setLoading(true);
      const rawData = await fetchTransactionsData();
      const adapted = adaptTransactionData(rawData);
      setAllTransactions(adapted);
      setLoading(false);
    };
    // Se ejecuta solo una vez al montar el Provider
    loadData();
  }, []);

  const value = {
    allTransactions,
    loading,
  };

  return <DataContext.Provider value={value}>{children}</DataContext.Provider>;
};

// 4. Crear un hook personalizado para consumir el contexto fácilmente
export const useTransactions = () => {
  const context = useContext(DataContext);
  if (context === undefined) {
    throw new Error("useTransactions debe ser usado dentro de un DataProvider");
  }
  return context;
};
