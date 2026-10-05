import React from 'react';
import RiskBadge from '../components/RiskBadge';

export default function PredictionResult({ predictionResult, onNavigate }) {
  // Default mock / demonstration data if advisor lands here directly without running a prediction
  const defaultSampleResult = {
    predicted_outcome: 'Pass',
    confidence: 0.7624,
    probabilities: {
      Distinction: 0.1038,
      Fail: 0.054,
      Pass: 0.7624,
      Withdrawn: 0.0798,
    },
    withdrawal_probability: 0.0798,
    risk_level: 'Low',
    advisor_message:
      'Current predicted withdrawal risk is low. Continue normal academic monitoring.',
  };

  const result = predictionResult || defaultSampleResult;
  const isDemo = !predictionResult;

  const classColorMap = {
    Distinction: 'bar-distinction',
    Pass: 'bar-pass',
    Fail: 'bar-fail',
    Withdrawn: 'bar-withdrawn',
  };

  return (
    <div className="page-container">
      <div className="page-header">
        <div>
          <h1 className="page-title">Prediction Result & Risk Analysis</h1>
          <p className="page-description">
            Advisor decision-support breakdown based on Week 10 academic and behavioral indicators.
          </p>
        </div>
        <div className="page-actions">
          <button
            type="button"
            className="btn btn-secondary"
            onClick={() => onNavigate('form')}
          >
            ← Back to Prediction Form
          </button>
        </div>
      </div>

      {isDemo && (
        <div className="alert alert-info mb-6">
          <strong>Demo Preview:</strong> Showing reference output from our verified training record. Run an inference in the Prediction Form to view live student results.
        </div>
      )}

      {/* Main Result Summary Card */}
      <div className="result-summary-grid mb-6">
        <div className="content-card result-primary-card">
          <div className="card-label">Predicted Final Outcome</div>
          <div className="outcome-display">
            <span className={`outcome-text outcome-${result.predicted_outcome.toLowerCase()}`}>
              {result.predicted_outcome}
            </span>
          </div>
          <div className="confidence-pill">
            Confidence: {(result.confidence * 100).toFixed(1)}%
          </div>
        </div>

        <div className="content-card result-risk-card">
          <div className="card-label">Withdrawal Risk Assessment</div>
          <div className="risk-level-row">
            <RiskBadge level={result.risk_level} />
            <span className="withdrawal-pct">
              {(result.withdrawal_probability * 100).toFixed(1)}%
            </span>
          </div>
          <p className="risk-subtext">Calculated probability of student withdrawal before semester completion.</p>
        </div>
      </div>

      {/* Advisor Decision Guidance Box */}
      <div className="content-card mb-6 advisor-guidance-card">
        <div className="card-section-title">
          <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" className="mr-2 text-teal">
            <path d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z"/>
          </svg>
          Advisor Decision-Support Guidance
        </div>
        <div className="guidance-box">
          <p className="guidance-message">"{result.advisor_message}"</p>
          <div className="guidance-footer">
            <span>Decision Support Mode</span> • <span>Week 10 Observation Horizon</span>
          </div>
        </div>
      </div>

      {/* Probability Distribution */}
      <div className="content-card">
        <div className="card-section-title">Outcome Probability Distribution</div>
        <p className="text-secondary mb-4">
          Multiclass probability distribution computed by the XGBClassifier across all 4 potential course outcomes:
        </p>

        <div className="probabilities-list">
          {Object.entries(result.probabilities || {}).map(([className, prob]) => {
            const percentage = (prob * 100).toFixed(1);
            const isHighest = className === result.predicted_outcome;

            return (
              <div key={className} className={`prob-row ${isHighest ? 'highest-prob' : ''}`}>
                <div className="prob-label-col">
                  <span className="prob-class-name">{className}</span>
                  {isHighest && <span className="top-indicator">Predicted</span>}
                </div>
                <div className="prob-bar-container">
                  <div
                    className={`prob-bar ${classColorMap[className] || 'bar-pass'}`}
                    style={{ width: `${Math.max(percentage, 2)}%` }}
                  />
                </div>
                <div className="prob-value-col">
                  <span className="prob-percentage">{percentage}%</span>
                </div>
              </div>
            );
          })}
        </div>
      </div>
    </div>
  );
}
