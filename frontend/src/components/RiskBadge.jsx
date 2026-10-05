import React from 'react';

/**
 * RiskBadge component displaying Low, Moderate, or High withdrawal risk.
 * @param {{ level: 'Low' | 'Moderate' | 'High' }} props
 */
export default function RiskBadge({ level }) {
  const normalizedLevel = (level || 'Low').toLowerCase();

  return (
    <span className={`risk-badge risk-${normalizedLevel}`}>
      <span className="risk-indicator-dot" />
      {level || 'Unknown'} Risk
    </span>
  );
}
