import React, { useState, useEffect } from 'react';
import Navbar from './components/Navbar';
import Dashboard from './pages/Dashboard';
import PredictionForm from './pages/PredictionForm';
import PredictionResult from './pages/PredictionResult';
import { checkHealth } from './services/api';

export default function App() {
  const [activePage, setActivePage] = useState('dashboard');
  const [backendStatus, setBackendStatus] = useState({ loading: true, status: null });
  const [predictionResult, setPredictionResult] = useState(null);
  const [studentInputData, setStudentInputData] = useState(null);

  // Poll or check backend health on mount
  useEffect(() => {
    let isMounted = true;

    async function verifyBackend() {
      try {
        const data = await checkHealth();
        if (isMounted) {
          setBackendStatus({ loading: false, status: data.status, details: data });
        }
      } catch (err) {
        if (isMounted) {
          setBackendStatus({ loading: false, status: 'offline', error: err.message });
        }
      }
    }

    verifyBackend();

    // Check again every 30 seconds
    const interval = setInterval(verifyBackend, 30000);
    return () => {
      isMounted = false;
      clearInterval(interval);
    };
  }, []);

  const handlePredictionSuccess = (result, inputData) => {
    setPredictionResult(result);
    setStudentInputData(inputData);
  };

  return (
    <div className="app-wrapper">
      <Navbar
        activePage={activePage}
        setActivePage={setActivePage}
        backendStatus={backendStatus}
      />

      <main className="main-content">
        {activePage === 'dashboard' && (
          <Dashboard
            backendStatus={backendStatus}
            onNavigate={setActivePage}
          />
        )}

        {activePage === 'form' && (
          <PredictionForm
            onPredictionSuccess={handlePredictionSuccess}
            onNavigate={setActivePage}
          />
        )}

        {activePage === 'result' && (
          <PredictionResult
            predictionResult={predictionResult}
            studentData={studentInputData}
            onNavigate={setActivePage}
          />
        )}
      </main>

      <footer className="footer" style={{ textAlign: 'center', padding: '1.5rem', borderTop: '1px solid var(--border-color)', color: 'var(--text-muted)', fontSize: '0.85rem' }}>
        University Student Dropout Risk Prediction System • Academic Advisor Portal (Week 10 Early Intervention)
      </footer>
    </div>
  );
}
