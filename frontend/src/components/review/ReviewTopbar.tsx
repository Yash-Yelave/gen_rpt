// src/components/review/ReviewTopbar.tsx
import React from 'react';
import { useNavigate } from 'react-router-dom';
import { ArrowLeft, Save } from 'lucide-react';
import { StatusBadge } from '@/components/common/StatusBadge';
import { useReviewActions } from '@/hooks/useReviewActions';
import { useReviewStore } from '@/store/reviewStore';
import { useUIStore } from '@/store/uiStore';
import type { Report } from '@/types';

interface Props {
  report: Report;
}

export const ReviewTopbar: React.FC<Props> = ({ report }) => {
  const navigate = useNavigate();
  const { decision } = useReviewStore();
  const { showToast } = useUIStore();
  const { saveReview } = useReviewActions(report.id);

  const handleSave = async () => {
    if (decision) {
      await saveReview.mutateAsync(decision);
    }
    showToast('Review saved successfully', 'success');
  };

  return (
    <div className="h-[60px] bg-white border-b border-gray-200 flex items-center justify-between px-4 sticky top-0 z-10">
      <div className="flex items-center gap-4 flex-1 min-w-0 pr-4">
        <button
          onClick={() => navigate(-1)}
          className="flex items-center gap-1.5 text-sm font-medium text-gray-500 hover:text-gray-900 transition-colors"
          aria-label="Back"
        >
          <ArrowLeft className="w-4 h-4" /> Back
        </button>
        <div className="h-4 w-px bg-gray-200"></div>
        <div className="flex-1 min-w-0">
          <div className="text-sm font-bold text-gray-900 truncate mb-0.5">{report.title}</div>
          <div className="flex items-center gap-3">
            <span className="text-[11px] text-gray-500 font-mono">ID: {report.id}</span>
            <span className="text-[11px] text-gray-500 font-mono">{report.version}</span>
            <StatusBadge status={report.status} className="!text-[10px] !px-1.5 !py-0" />
            {report.aiScore > 0 && (
              <span className="text-[10px] font-bold text-blue-700 bg-blue-50 border border-blue-100 px-1.5 rounded">
                AI Score: {report.aiScore.toFixed(1)}
              </span>
            )}
          </div>
        </div>
      </div>

      <div className="flex items-center gap-2 flex-shrink-0">
        <button
          onClick={handleSave}
          disabled={saveReview.isPending}
          className="flex items-center gap-1.5 px-3 py-1.5 bg-white border border-gray-300 rounded text-sm font-semibold text-gray-700 hover:bg-gray-50 transition-colors disabled:opacity-50"
        >
          <Save className="w-4 h-4" /> Save Review
        </button>
      </div>
    </div>
  );
};
