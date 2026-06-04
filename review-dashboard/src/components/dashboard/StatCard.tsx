// src/components/dashboard/StatCard.tsx
import React from 'react';

interface Props {
  label: string;
  value: number | string;
  meta?: string;
  accent?: 'blue' | 'green' | 'orange' | 'none';
}

const accentClasses: Record<string, string> = {
  blue:   'border-t-[3px] border-t-blue-600',
  green:  'border-t-[3px] border-t-green-600',
  orange: 'border-t-[3px] border-t-orange-600',
  none:   '',
};

export const StatCard = React.memo(({ label, value, meta, accent = 'none' }: Props) => (
  <div className={`bg-white border border-gray-200 rounded-lg p-4 hover:shadow-sm transition-shadow ${accentClasses[accent]}`}>
    <div className="text-xs font-semibold text-gray-500 uppercase tracking-wide mb-2">{label}</div>
    <div className="text-[28px] font-bold text-gray-900 leading-none tracking-tight mb-1">{value}</div>
    {meta && <div className="text-xs text-gray-400">{meta}</div>}
  </div>
));
StatCard.displayName = 'StatCard';
