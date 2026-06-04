// src/pages/Review/index.tsx
import React from 'react';
import { ReportGrid } from '@/components/report/ReportGrid';
import { ReportStatus } from '@/types';

export const PendingReviewList: React.FC = () => {
  return (
    <div className="p-6">
      <div className="mb-6">
        <h1 className="text-xl font-bold text-gray-900 tracking-tight">Pending Review</h1>
        <p className="text-sm text-gray-500 mt-1">Reports awaiting human review decision</p>
      </div>

      <ReportGrid
        statuses={[ReportStatus.AIReviewed, ReportStatus.NeedsHumanReview]}
        emptyTitle="No reports pending review"
        emptyText="All reports have been reviewed."
      />
    </div>
  );
};
