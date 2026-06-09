// src/pages/Review/ReportReview.tsx
import React, { useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { useReport } from '@/hooks/useReports';
import { useReviewStore } from '@/store/reviewStore';
import { ReviewTopbar } from '@/components/review/ReviewTopbar';
import { ReportPreview } from '@/components/report/ReportPreview';
import { HumanReviewCard } from '@/components/review/HumanReviewCard';
import { CommentThread } from '@/components/comments/CommentThread';
import { EmptyState } from '@/components/common/EmptyState';
import { FileWarning } from 'lucide-react';

export const ReportReview: React.FC = () => {
  const { reportId } = useParams<{ reportId: string }>();
  const navigate = useNavigate();
  const { data: report, isLoading } = useReport(reportId ?? '');
  const resetForm = useReviewStore((s: any) => s.reset);
  const setDecision = useReviewStore((s: any) => s.setDecision);

  // Sync form with report's current humanStatus if it matches a valid decision
  useEffect(() => {
    if (report?.humanStatus && ['Approved', 'Needs Revision', 'Rejected'].includes(report.humanStatus)) {
      setDecision(report.humanStatus);
    } else {
      resetForm();
    }
  }, [report?.humanStatus, setDecision, resetForm]);

  if (isLoading) return <div className="p-8 text-center text-gray-500">Loading report…</div>;

  if (!report) {
    return (
      <div className="p-8 h-full flex items-center justify-center">
        <EmptyState
          icon={<FileWarning className="w-full h-full text-red-400" />}
          title="Report Not Found"
          text={`Could not find report with ID ${reportId}`}
        />
        <button onClick={() => navigate(-1)} className="mt-4 px-4 py-2 bg-blue-600 text-white rounded">Go Back</button>
      </div>
    );
  }

  return (
    <div className="flex flex-col h-full bg-surface-body">
      <ReviewTopbar report={report} />

      <div className="review-body-grid">
        {/* Left: Document Preview with tabs (Report / AI Review) */}
        <div className="overflow-hidden flex flex-col h-full">
          <ReportPreview report={report} />
        </div>

        {/* Right: Human Review + Comments only */}
        <div className="overflow-y-auto bg-gray-50 border-l border-gray-200">
          <div className="p-4 flex flex-col gap-4">
            <HumanReviewCard report={report} />
            <CommentThread report={report} />
          </div>
        </div>
      </div>
    </div>
  );
};
