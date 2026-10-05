import React from 'react';

/**
 * Top navigation bar with academic branding, navigation items, and backend health status.
 */
export default function Navbar({ activePage, setActivePage, backendStatus }) {
  const isHealthy = backendStatus?.status === 'healthy';

  return (
    <header className="navbar">
      <div className="navbar-container">
        <div className="navbar-brand">
          <div className="brand-icon">
            <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
              <path d="M22 10v6M2 10l10-5 10 5-10 5z"/>
              <path d="M6 12v5c3 3 9 3 12 0v-5"/>
            </svg>
          </div>
          <div>
            <div className="brand-title">Student Dropout Risk System</div>
            <div className="brand-subtitle">Academic Advisor Portal • Week 10 Early Intervention</div>
          </div>
        </div>

        <nav className="navbar-nav">
          <button
            type="button"
            className={`nav-tab ${activePage === 'dashboard' ? 'active' : ''}`}
            onClick={() => setActivePage('dashboard')}
          >
            Dashboard
          </button>
          <button
            type="button"
            className={`nav-tab ${activePage === 'form' ? 'active' : ''}`}
            onClick={() => setActivePage('form')}
          >
            Prediction Form
          </button>
          <button
            type="button"
            className={`nav-tab ${activePage === 'result' ? 'active' : ''}`}
            onClick={() => setActivePage('result')}
          >
            Prediction Result
          </button>
        </nav>

        <div className="navbar-status">
          <span
            className={`backend-status-pill ${
              isHealthy ? 'status-online' : backendStatus?.loading ? 'status-checking' : 'status-offline'
            }`}
          >
            <span className="status-dot" />
            {backendStatus?.loading
              ? 'Checking API...'
              : isHealthy
              ? 'FastAPI Online'
              : 'API Offline'}
          </span>
        </div>
      </div>
    </header>
  );
}
