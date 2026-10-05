import React from 'react';

/**
 * Reusable clean card for metrics, status, or key numbers.
 */
export default function StatusCard({ title, value, subtitle, icon, badge, tone = 'default' }) {
  return (
    <div className={`status-card tone-${tone}`}>
      <div className="status-card-header">
        <span className="status-card-title">{title}</span>
        {icon && <span className="status-card-icon">{icon}</span>}
      </div>
      <div className="status-card-body">
        <div className="status-card-value-row">
          <span className="status-card-value">{value}</span>
          {badge && <span className="status-card-badge">{badge}</span>}
        </div>
        {subtitle && <p className="status-card-subtitle">{subtitle}</p>}
      </div>
    </div>
  );
}
