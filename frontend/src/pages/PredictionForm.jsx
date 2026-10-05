import React, { useState } from 'react';
import { predictOutcome } from '../services/api';
import {
  FORM_SECTIONS,
  VERIFIED_REAL_STUDENT_RECORD,
  getInitialFormState,
} from './formConfig';

const INTEGER_KEYS = new Set([
  'num_of_prev_attempts',
  'studied_credits',
  'module_presentation_length',
  'assessments_submitted_week10',
  'banked_assessment_count_week10',
  'tma_count_week10',
  'cma_count_week10',
  'exam_count_week10',
  'total_clicks_week10',
  'active_vle_days_week10',
  'unique_vle_sites_week10',
  'dataplus_clicks_week10',
  'dualpane_clicks_week10',
  'externalquiz_clicks_week10',
  'forumng_clicks_week10',
  'glossary_clicks_week10',
  'homepage_clicks_week10',
  'htmlactivity_clicks_week10',
  'oucollaborate_clicks_week10',
  'oucontent_clicks_week10',
  'ouelluminate_clicks_week10',
  'ouwiki_clicks_week10',
  'page_clicks_week10',
  'questionnaire_clicks_week10',
  'quiz_clicks_week10',
  'repeatactivity_clicks_week10',
  'resource_clicks_week10',
  'sharedsubpage_clicks_week10',
  'subpage_clicks_week10',
  'url_clicks_week10',
  'has_assessment_activity_week10',
  'has_vle_activity_week10',
]);

export default function PredictionForm({ onPredictionSuccess, onNavigate }) {
  const [formData, setFormData] = useState(getInitialFormState());
  const [errors, setErrors] = useState({});
  const [apiError, setApiError] = useState(null);
  const [loading, setLoading] = useState(false);
  const [collapsedSections, setCollapsedSections] = useState({});
  const [loadedDemoNotice, setLoadedDemoNotice] = useState(false);

  // Toggle collapsible section
  const toggleSection = (sectionId) => {
    setCollapsedSections((prev) => ({
      ...prev,
      [sectionId]: !prev[sectionId],
    }));
  };

  // Handle single field change
  const handleChange = (fieldKey, value) => {
    setFormData((prev) => ({
      ...prev,
      [fieldKey]: value,
    }));

    // Clear field-specific error if user corrects value
    if (errors[fieldKey]) {
      setErrors((prev) => {
        const next = { ...prev };
        delete next[fieldKey];
        return next;
      });
    }
  };

  // Load verified example student record (Row 0 from X_train_raw.csv)
  const handleLoadExample = () => {
    setFormData({ ...VERIFIED_REAL_STUDENT_RECORD });
    setErrors({});
    setApiError(null);
    setLoadedDemoNotice(true);
    setTimeout(() => setLoadedDemoNotice(false), 5000);
  };

  // Reset form to blank
  const handleReset = () => {
    if (window.confirm('Reset all form fields to blank?')) {
      setFormData(getInitialFormState());
      setErrors({});
      setApiError(null);
    }
  };

  // Client-side validation across all 52 fields
  const validateForm = () => {
    const newErrors = {};

    FORM_SECTIONS.forEach((section) => {
      section.fields.forEach((field) => {
        const val = formData[field.key];

        // Check required presence
        if (val === '' || val === null || val === undefined) {
          newErrors[field.key] = `${field.label} is required.`;
          return;
        }

        // Numeric constraints check
        if (field.type === 'number') {
          const num = Number(val);
          if (isNaN(num)) {
            newErrors[field.key] = `${field.label} must be a valid number.`;
          } else {
            if (field.min !== undefined && num < field.min) {
              newErrors[field.key] = `Minimum allowed value is ${field.min}.`;
            }
            if (field.max !== undefined && num > field.max) {
              newErrors[field.key] = `Maximum allowed value is ${field.max}.`;
            }
          }
        }
      });
    });

    setErrors(newErrors);
    return Object.keys(newErrors).length === 0;
  };

  // Submit to POST /predict
  const handleSubmit = async (e) => {
    e.preventDefault();
    setApiError(null);

    if (!validateForm()) {
      setApiError('Please resolve the highlighted validation errors before submitting.');
      // Expand sections with errors
      const newCollapsed = { ...collapsedSections };
      FORM_SECTIONS.forEach((section) => {
        const hasError = section.fields.some((f) => errors[f.key]);
        if (hasError) {
          newCollapsed[section.id] = false;
        }
      });
      setCollapsedSections(newCollapsed);
      window.scrollTo({ top: 0, behavior: 'smooth' });
      return;
    }

    // Build payload with converted numbers
    const payload = {};
    FORM_SECTIONS.forEach((section) => {
      section.fields.forEach((field) => {
        const rawVal = formData[field.key];
        if (field.type === 'select') {
          payload[field.key] = String(rawVal);
        } else if (field.type === 'boolean-select') {
          payload[field.key] = Number(rawVal);
        } else if (INTEGER_KEYS.has(field.key)) {
          payload[field.key] = Math.round(Number(rawVal));
        } else {
          payload[field.key] = Number(rawVal);
        }
      });
    });

    setLoading(true);

    try {
      const response = await predictOutcome(payload);
      if (onPredictionSuccess) {
        onPredictionSuccess(response, payload);
      }
      onNavigate('result');
    } catch (err) {
      console.error('Prediction submission failed:', err);
      setApiError(
        err.message || 'An error occurred while communicating with the prediction backend.'
      );
      window.scrollTo({ top: 0, behavior: 'smooth' });
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="page-container">
      {/* Header */}
      <div className="page-header">
        <div>
          <h1 className="page-title">Student Prediction Form</h1>
          <p className="page-description">
            Enter raw early-semester indicators (available up to Week 10) to evaluate withdrawal risk and likely outcome.
          </p>
        </div>

        <div className="page-actions form-header-actions">
          <button
            type="button"
            className="btn btn-secondary"
            onClick={handleLoadExample}
            disabled={loading}
          >
            📋 Load Example Student
          </button>
          <button
            type="button"
            className="btn btn-secondary"
            onClick={handleReset}
            disabled={loading}
          >
            ↺ Reset Form
          </button>
          <button
            type="submit"
            form="student-prediction-form"
            className="btn btn-primary"
            disabled={loading}
          >
            {loading ? 'Evaluating Model...' : 'Predict Student Outcome →'}
          </button>
        </div>
      </div>

      {/* Global Alerts */}
      {loadedDemoNotice && (
        <div className="alert alert-info mb-6">
          <strong>Example Student Loaded:</strong> Populated all 52 raw fields using our verified training baseline (Module AAA, Cohort 2013J). You can inspect or modify values before predicting.
        </div>
      )}

      {apiError && (
        <div className="alert alert-error mb-6">
          <strong>Validation / Submission Notice:</strong> {apiError}
        </div>
      )}

      {/* Main 52-Field Form */}
      <form id="student-prediction-form" onSubmit={handleSubmit} noValidate>
        {FORM_SECTIONS.map((section) => {
          const isCollapsed = !!collapsedSections[section.id];
          const sectionErrorCount = section.fields.filter((f) => errors[f.key]).length;

          return (
            <div key={section.id} className="content-card form-section-card mb-6">
              <div
                className="form-section-header"
                onClick={() => toggleSection(section.id)}
                role="button"
                tabIndex={0}
                onKeyDown={(e) => {
                  if (e.key === 'Enter' || e.key === ' ') {
                    toggleSection(section.id);
                  }
                }}
              >
                <div className="section-title-wrap">
                  <span className="section-number-pill">{section.number}</span>
                  <div>
                    <h2 className="section-title">{section.title}</h2>
                    <p className="section-subtitle">{section.description}</p>
                  </div>
                </div>

                <div className="section-header-meta">
                  {sectionErrorCount > 0 && (
                    <span className="section-error-pill">
                      {sectionErrorCount} {sectionErrorCount === 1 ? 'error' : 'errors'}
                    </span>
                  )}
                  <span className="collapse-icon">{isCollapsed ? '▼' : '▲'}</span>
                </div>
              </div>

              {!isCollapsed && (
                <div className="form-fields-grid">
                  {section.fields.map((field) => {
                    const fieldError = errors[field.key];
                    const value = formData[field.key];

                    return (
                      <div
                        key={field.key}
                        className={`form-group ${fieldError ? 'has-error' : ''}`}
                      >
                        <label htmlFor={field.key} className="form-label">
                          {field.label}
                          <span className="required-asterisk">*</span>
                        </label>

                        {field.type === 'select' && (
                          <select
                            id={field.key}
                            className="form-control"
                            value={value}
                            onChange={(e) => handleChange(field.key, e.target.value)}
                          >
                            <option value="">-- Select {field.label} --</option>
                            {field.options.map((opt) => {
                              const optVal = typeof opt === 'object' ? opt.value : opt;
                              const optLabel = typeof opt === 'object' ? opt.label : opt;
                              return (
                                <option key={optVal} value={optVal}>
                                  {optLabel}
                                </option>
                              );
                            })}
                          </select>
                        )}

                        {field.type === 'boolean-select' && (
                          <select
                            id={field.key}
                            className="form-control"
                            value={value}
                            onChange={(e) => handleChange(field.key, e.target.value)}
                          >
                            <option value="">-- Select Status --</option>
                            {field.options.map((opt) => (
                              <option key={opt.value} value={opt.value}>
                                {opt.label}
                              </option>
                            ))}
                          </select>
                        )}

                        {field.type === 'number' && (
                          <input
                            id={field.key}
                            type="number"
                            className="form-control"
                            value={value}
                            min={field.min}
                            max={field.max}
                            step={field.step || 'any'}
                            placeholder={field.placeholder || ''}
                            onChange={(e) => handleChange(field.key, e.target.value)}
                          />
                        )}

                        {field.helper && !fieldError && (
                          <span className="form-helper-text">{field.helper}</span>
                        )}

                        {fieldError && (
                          <span className="form-error-text">{fieldError}</span>
                        )}
                      </div>
                    );
                  })}
                </div>
              )}
            </div>
          );
        })}

        {/* Bottom Action Footer */}
        <div className="form-footer-card content-card">
          <div className="form-footer-content">
            <div>
              <h3 className="footer-action-title">Ready for Model Prediction</h3>
              <p className="text-secondary" style={{ fontSize: '0.85rem' }}>
                All 52 early-semester indicators will be processed and evaluated against the trained model.
              </p>
            </div>
            <div className="form-footer-buttons">
              <button
                type="button"
                className="btn btn-secondary"
                onClick={handleReset}
                disabled={loading}
              >
                Reset All Fields
              </button>
              <button
                type="submit"
                className="btn btn-primary"
                disabled={loading}
              >
                {loading ? 'Evaluating Model...' : 'Predict Student Outcome →'}
              </button>
            </div>
          </div>
        </div>
      </form>
    </div>
  );
}
