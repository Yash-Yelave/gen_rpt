// src/pages/Reviewed/index.tsx
import React from 'react';
import { ReportGrid } from '@/components/report/ReportGrid';
import { ReportStatus } from '@/types';

export const ReviewedList: React.FC = () => (
  <div className="p-6">
    <div className="mb-6">
      <h1 className="text-xl font-bold text-gray-900 tracking-tight">Reviewed Reports</h1>
      <p className="text-sm text-gray-500 mt-1">Reports that have been approved or marked ready to publish</p>
    </div>
    <ReportGrid
      statuses={[ReportStatus.Approved, ReportStatus.ReadyToPublish]}
      emptyTitle="No reviewed reports"
      emptyText="There are currently no approved reports."
    />
  </div>
);
