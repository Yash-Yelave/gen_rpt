// src/components/report/ReportCard.tsx
import React from 'react';
import { useNavigate } from 'react-router-dom';
import { StatusBadge } from '@/components/common/StatusBadge';
import { formatDate } from '@/utils/formatters';
import type { Report } from '@/types';

interface Props {
  report: Report;
}

export const ReportCard = React.memo(({ report: r }: Props) => {
  const navigate = useNavigate();

  return (
    <div
      className="bg-white border border-gray-200 rounded-lg p-4 hover:shadow-md hover:border-blue-200 transition-all cursor-pointer"
      role="button"
      tabIndex={0}
      onClick={() => navigate(`/review/${r.id}`)}
      onKeyDown={(e) => { if (e.key === 'Enter' || e.key === ' ') navigate(`/review/${r.id}`); }}
      aria-label={`Open report: ${r.title}`}
    >
      <div className="flex items-start justify-between gap-2 mb-3">
        <div>
          <div className="text-sm font-semibold text-gray-900 leading-snug">{r.title}</div>
          <div className="text-xs text-gray-400 font-mono mt-0.5">{r.id} · {r.version}</div>
        </div>
        <StatusBadge status={r.status} />
      </div>
      <div className="flex gap-2 flex-wrap mb-3">
        {r.aiScore > 0 && (
          <span className="inline-flex items-center bg-blue-50 border border-blue-100 text-blue-700 text-xs font-bold px-2 py-0.5 rounded-full">
            AI {r.aiScore.toFixed(1)}
          </span>
        )}
        {r.commentCount > 0 && (
          <span className="inline-flex items-center bg-gray-100 text-gray-600 text-xs font-semibold px-2 py-0.5 rounded-full">
            {r.commentCount} comment{r.commentCount > 1 ? 's' : ''}
          </span>
        )}
      </div>
      <div className="flex items-center justify-between pt-3 border-t border-gray-200">
        {r.aiScore > 0 ? (
          <span className="text-xs font-bold text-blue-700">AI Score: {r.aiScore.toFixed(1)}</span>
        ) : (
          <span className="text-xs text-gray-400">Not scored</span>
        )}
        <span className="text-xs text-gray-400">{formatDate(r.lastUpdated)}</span>
      </div>
    </div>
  );
});
ReportCard.displayName = 'ReportCard';
