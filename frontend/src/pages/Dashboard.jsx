import React from 'react';
import StatusCard from '../components/StatusCard';

export default function Dashboard({ backendStatus, onNavigate }) {
  const isHealthy = backendStatus?.status === 'healthy';

  return (
    <div className="page-container">
      <div className="page-header">
        <div>
          <h1 className="page-title">Advisor Decision-Support Dashboard</h1>
          <p className="page-description">
            Early identification and proactive academic support system using student data up to Week 10.
          </p>
        </div>
        <div className="page-actions">
          <button
            type="button"
            className="btn btn-primary"
            onClick={() => onNavigate('form')}
          >
            Open Prediction Form →
          </button>
        </div>
      </div>

      {/* Metric / Status Cards Grid */}
      <div className="card-grid">
        <StatusCard
          title="Backend API Status"
          value={isHealthy ? 'Operational' : backendStatus?.loading ? 'Checking...' : 'Disconnected'}
          subtitle={isHealthy ? 'FastAPI service connected at 127.0.0.1:8000' : 'Ensure FastAPI server is running'}
          badge={isHealthy ? 'Healthy' : 'Action Required'}
          tone={isHealthy ? 'success' : 'warning'}
        />
        <StatusCard
          title="Model Pipeline"
          value="XGBClassifier"
          subtitle="Trained imblearn pipeline with RandomOverSampler"
          badge="Week 10 Model"
          tone="primary"
        />
        <StatusCard
          title="Input Features"
          value="52 Raw Fields"
          subtitle="44 Numerical + 8 Categorical (Expands to 90 Transformed)"
          badge="ColumnTransformer"
          tone="info"
        />
        <StatusCard
          title="Outcome Classes"
          value="4 Outcomes"
          subtitle="Withdrawn • Fail • Pass • Distinction"
          badge="Multiclass"
          tone="default"
        />
      </div>

      {/* Advisory Principles & Guidance Banner */}
      <div className="content-card mb-6">
        <div className="card-section-title">
          <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" className="mr-2 text-teal">
            <circle cx="12" cy="12" r="10" />
            <line x1="12" y1="16" x2="12" y2="12" />
            <line x1="12" y1="8" x2="12.01" y2="8" />
          </svg>
          Core Advisory Principles & System Integrity
        </div>
        <div className="principles-grid">
          <div className="principle-box">
            <h3 className="principle-title">Early Intervention Window</h3>
            <p className="principle-text">
              The model observes student interactions strictly up to <strong>Week 10</strong>. This provides sufficient lead time for advisors to intervene before final assessments and withdrawals occur.
            </p>
          </div>
          <div className="principle-box">
            <h3 className="principle-title">Leakage-Free Safety</h3>
            <p className="principle-text">
              Post-outcome fields such as <code>final_result</code> and <code>date_unregistration</code> are strictly forbidden. The system prevents optimistic bias and post-event contamination.
            </p>
          </div>
          <div className="principle-box">
            <h3 className="principle-title">Supportive & Non-Punitive</h3>
            <p className="principle-text">
              Risk scores serve solely as decision support for academic advisors. Predictions are never deterministic labels and must guide empathetic outreach and tutoring assistance.
            </p>
          </div>
        </div>
      </div>

      {/* Withdrawal Risk Tier Breakdown */}
      <div className="content-card">
        <div className="card-section-title">Withdrawal Risk Classification Framework</div>
        <p className="text-secondary mb-4">
          The system calculates multi-class probabilities and maps the specific <strong>Withdrawn Probability</strong> to three actionable advisor tiers:
        </p>

        <div className="tier-table-container">
          <table className="tier-table">
            <thead>
              <tr>
                <th>Risk Tier</th>
                <th>Withdrawal Probability Range</th>
                <th>Advisor Decision-Support Guidance</th>
              </tr>
            </thead>
            <tbody>
              <tr>
                <td>
                  <span className="risk-badge risk-low">Low Risk</span>
                </td>
                <td><code>&lt; 30%</code></td>
                <td>Current predicted withdrawal risk is low. Continue normal academic monitoring.</td>
              </tr>
              <tr>
                <td>
                  <span className="risk-badge risk-moderate">Moderate Risk</span>
                </td>
                <td><code>30% – 59.9%</code></td>
                <td>This student shows a moderate predicted withdrawal risk. Consider reviewing engagement and assessment progress.</td>
              </tr>
              <tr>
                <td>
                  <span className="risk-badge risk-high">High Risk</span>
                </td>
                <td><code>&ge; 60%</code></td>
                <td>This student shows a high predicted withdrawal risk and may benefit from early academic support and outreach.</td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );
}
