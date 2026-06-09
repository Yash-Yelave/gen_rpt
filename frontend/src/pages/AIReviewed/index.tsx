// src/pages/AIReviewed/index.tsx
import React from 'react';
import { ReportGrid } from '@/components/report/ReportGrid';
import { ReportStatus } from '@/types';

export const AIReviewedList: React.FC = () => (
  <div className="p-6">
    <div className="mb-6">
      <h1 className="text-xl font-bold text-gray-900 tracking-tight">AI Reviewed</h1>
      <p className="text-sm text-gray-500 mt-1">Reports that have been AI-reviewed and are awaiting human review</p>
    </div>
    <ReportGrid
      statuses={[ReportStatus.NeedsHumanReview]}
      emptyTitle="No reports awaiting review"
      emptyText="All AI-reviewed reports have been assigned a human decision."
    />
  </div>
);
