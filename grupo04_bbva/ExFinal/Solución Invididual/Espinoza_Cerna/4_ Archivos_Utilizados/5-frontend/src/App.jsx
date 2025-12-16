import { useState } from 'react'
import FileUpload from './components/FileUpload'
import KpiDashboard from './components/KpiDashboard'
import FlightExplorer from './components/FlightExplorer'
import './App.css'

function App() {
  const [activeTab, setActiveTab] = useState('upload');
  const [isProcessing, setIsProcessing] = useState(false);
  const [refreshKey, setRefreshKey] = useState(0);

  const isUploadActive = activeTab === 'upload';
  const isKpiDashboardActive = activeTab === 'kpi_dashboard';
  const isExplorerActive = activeTab === 'explorer';

  const handleProcessingComplete = () => {
    setIsProcessing(false);
    setRefreshKey(prevKey => prevKey + 1); // Increment key to force re-render of dashboard
  };

  return (
    <div className="min-h-screen flex flex-col items-center justify-center p-4 animate-fade-in-up">
      <div className="w-full max-w-6xl mx-auto">
        <h1 className="text-5xl md:text-6xl font-display font-bold text-center text-white mb-10 tracking-wider">
          ANÁLISIS DE RETRASOS DE VUELOS
        </h1>
        <div className="grid grid-cols-1 md:grid-cols-3 gap-8 mb-12">
          <button 
            onClick={() => setActiveTab('upload')}
            className={`group relative flex items-center justify-center gap-3 w-full h-16 px-6 text-white font-bold text-lg rounded-lg transition-all duration-300 shadow-glow-primary ${isUploadActive ? 'bg-primary' : 'bg-primary/20 border border-primary/50 hover:bg-primary/30'}`}
          >
            <span className="material-symbols-outlined">upload</span>
            SUBIR ARCHIVO
          </button>
          <button 
            onClick={() => setActiveTab('kpi_dashboard')}
            className={`group relative flex items-center justify-center gap-3 w-full h-16 px-6 text-white font-bold text-lg rounded-lg transition-all duration-300 shadow-glow-primary ${isKpiDashboardActive ? 'bg-primary' : 'bg-primary/20 border border-primary/50 hover:bg-primary/30'} disabled:opacity-50 disabled:cursor-not-allowed disabled:hover:bg-primary/20`}
            disabled={isProcessing}
          >
            <span className="material-symbols-outlined">bar_chart</span>
            DASHBOARD DE KPIS
          </button>
          <button 
            onClick={() => setActiveTab('explorer')}
            className={`group relative flex items-center justify-center gap-3 w-full h-16 px-6 text-white font-bold text-lg rounded-lg transition-all duration-300 shadow-glow-primary ${isExplorerActive ? 'bg-primary' : 'bg-primary/20 border border-primary/50 hover:bg-primary/30'} disabled:opacity-50 disabled:cursor-not-allowed disabled:hover:bg-primary/20`}
            disabled={isProcessing}
          >
            <span className="material-symbols-outlined">travel_explore</span>
            EXPLORADOR DE VUELOS
          </button>
        </div>
        <main>
          {isUploadActive && <FileUpload setIsProcessing={setIsProcessing} onComplete={handleProcessingComplete} />}
          {isKpiDashboardActive && <KpiDashboard key={refreshKey} />}
          {isExplorerActive && <FlightExplorer key={refreshKey} />}
        </main>
      </div>
    </div>
  );
}

export default App
