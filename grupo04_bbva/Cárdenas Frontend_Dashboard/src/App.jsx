// src/App.jsx
import React, { Suspense } from "react";
import {
  BrowserRouter as Router,
  Routes,
  Route,
  NavLink,
} from "react-router-dom"; // 1. Importamos NavLink
import { Activity } from "lucide-react";

// 1. Cambiamos los imports estáticos por dinámicos con React.lazy
const ClientAnalysisView = React.lazy(() => import("./pages/ClientAnalysis.jsx"));
const GlobalAnalysis = React.lazy(() => import("./pages/GlobalAnalysis.jsx"));
const Comparison = React.lazy(() => import("./pages/Comparison.jsx"));

// 2. Componente auxiliar para manejar los estilos activo/inactivo limpiamente
const NavItem = ({ to, children }) => {
  const baseClasses = "block p-3 rounded-lg font-medium transition-colors";
  const activeClasses = "bg-blue-50 text-blue-700";
  const inactiveClasses =
    "text-slate-600 hover:bg-slate-50 hover:text-slate-900";

  return (
    <li>
      <NavLink
        to={to}
        // El prop 'end' asegura que la ruta "/" no se quede activa cuando entras a "/global"
        end={to === "/"}
        className={({ isActive }) =>
          `${baseClasses} ${isActive ? activeClasses : inactiveClasses}`
        }
      >
        {children}
      </NavLink>
    </li>
  );
};

function App() {
  return (
    <Router>
      <div className="flex min-h-screen bg-slate-50">
        {/* Sidebar de Navegación Simple */}
        <nav className="w-64 bg-white border-r border-slate-200 p-6 hidden md:block">
          <h2 className="text-xl font-bold text-slate-800 mb-8">
            Dashboard 2025
          </h2>

          <ul className="space-y-2">
            {/* 3. Usamos el componente NavItem para cada link */}
            <NavItem to="/">Análisis por Transacción</NavItem>

            <NavItem to="/global">Análisis Global</NavItem>

            <NavItem to="/comparacion">Comparación</NavItem>
          </ul>
        </nav>

        {/* Área de Contenido */}
        <main className="flex-1 overflow-auto">
          {/* 4. Envolvemos las rutas con Suspense para manejar la carga */}
          <Suspense
            fallback={
              <div className="h-full w-full flex items-center justify-center bg-slate-50">
                <div className="animate-pulse flex flex-col items-center text-blue-600">
                  <Activity size={48} className="mb-4 animate-spin" />
                  <span className="font-medium text-lg">Cargando vista...</span>
                </div>
              </div>
            }
          >
            <Routes>
              <Route path="/" element={<ClientAnalysisView />} />
              <Route path="/global" element={<GlobalAnalysis />} />
              <Route path="/comparacion" element={<Comparison />} />
            </Routes>
          </Suspense>
        </main>
      </div>
    </Router>
  );
}

export default App;
