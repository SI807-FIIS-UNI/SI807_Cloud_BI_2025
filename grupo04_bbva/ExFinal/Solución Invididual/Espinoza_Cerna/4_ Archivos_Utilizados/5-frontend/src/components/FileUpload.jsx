import React, { useState, useEffect, useCallback } from 'react';

const FileUpload = ({ setIsProcessing, onComplete }) => {
  const [file, setFile] = useState(null);
  const [fileName, setFileName] = useState('');
  const [error, setError] = useState('');
  const [uploadStatus, setUploadStatus] = useState({ status: 'idle', message: '' });
  const [taskId, setTaskId] = useState(null);

  useEffect(() => {
    if (taskId && (uploadStatus.status === 'procesando' || uploadStatus.status === 'subiendo')) {
      const interval = setInterval(async () => {
        try {
          const response = await fetch(`${import.meta.env.VITE_API_URL}/upload/status/${taskId}`);
          const data = await response.json();
          setUploadStatus(data);

          if (data.status === 'completado' || data.status === 'error') {
            clearInterval(interval);
            setIsProcessing(false);
            if (data.status === 'completado') {
              setFile(null);
              setFileName('');
              if (onComplete) {
                onComplete();
              }
            }
          }
        } catch (err) {
          console.error('Error polling status:', err);
          clearInterval(interval);
          setIsProcessing(false);
        }
      }, 2000);

      return () => clearInterval(interval);
    }
  }, [taskId, uploadStatus.status, setIsProcessing, onComplete]);

  const handleFileChange = useCallback((e) => {
    const selectedFile = e.target.files[0];
    if (selectedFile) {
      setFile(selectedFile);
      setFileName(selectedFile.name);
      setError('');
      setUploadStatus({ status: 'idle', message: '' });
      setTaskId(null);
    }
  }, []);

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!file) return;

    const formData = new FormData();
    formData.append('file', file);
    setError('');
    setUploadStatus({ status: 'subiendo', message: 'Subiendo archivo al servidor...' });
    setIsProcessing(true);

    try {
      const response = await fetch(`${import.meta.env.VITE_API_URL}/upload`, {
        method: 'POST',
        body: formData,
      });

      const result = await response.json();

      if (!response.ok) {
        throw new Error(result.error || 'Error en la subida.');
      }

      setTaskId(result.task_id);
      setUploadStatus({ status: 'procesando', message: 'Archivo subido, iniciando pipeline...' });
    } catch (err) {
      setError(err.message);
      setUploadStatus({ status: 'error', message: err.message });
      setIsProcessing(false);
    }
  };

  return (
    <form onSubmit={handleSubmit} className="bg-gray-900/50 border border-gray-700 rounded-xl p-8 backdrop-blur-sm space-y-8">
      <div>
        <label htmlFor="file-upload" className="block text-lg font-mono text-white mb-2">
          1. Selecciona el archivo de datos
        </label>
        <div className="mt-2 flex justify-center rounded-lg border-2 border-dashed border-gray-600 px-6 py-10 hover:border-primary transition-colors">
          <div className="text-center">
            <span className="material-symbols-outlined text-5xl text-gray-500">draft</span>
            <div className="mt-4 flex text-sm leading-6 text-gray-400">
              <label
                htmlFor="file-upload"
                className="relative cursor-pointer rounded-md font-semibold text-primary focus-within:outline-none focus-within:ring-2 focus-within:ring-primary focus-within:ring-offset-2 focus-within:ring-offset-gray-900 hover:text-primary-light"
              >
                <span>Sube un archivo</span>
                <input id="file-upload" name="file-upload" type="file" className="sr-only" onChange={handleFileChange} accept=".csv" />
              </label>
              <p className="pl-1">o arrástralo aquí</p>
            </div>
            {fileName && <p className="text-sm text-white/80 mt-2">{fileName}</p>}
          </div>
        </div>
        <p className="text-sm text-white/60 mt-4">Solo se aceptan archivos .csv</p>
      </div>

      <button
        type="submit"
        className="w-full h-16 bg-primary text-white font-bold text-lg rounded-lg flex items-center justify-center gap-3 hover:bg-primary-dark transition-all duration-300 disabled:opacity-50 disabled:cursor-not-allowed"
        disabled={!file || uploadStatus.status === 'subiendo' || uploadStatus.status === 'procesando'}
      >
        <span className="material-symbols-outlined">play_arrow</span>
        SUBIR Y PROCESAR
      </button>

      {error && <p className="text-red-500 text-center font-mono">{error}</p>}

      {(uploadStatus.status === 'subiendo' || uploadStatus.status === 'procesando') && (
        <div className="text-center text-primary font-mono animate-pulse">{uploadStatus.message}</div>
      )}

      {uploadStatus.status === 'completado' && (
        <div className="text-center text-green-500 font-mono">{uploadStatus.message}</div>
      )}

      {uploadStatus.status === 'error' && uploadStatus.message !== error && (
        <p className="text-red-500 text-center font-mono">{uploadStatus.message}</p>
      )}
    </form>
  );
};

export default FileUpload;
