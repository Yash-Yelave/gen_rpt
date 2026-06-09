// src/pages/ApprovedReports/index.tsx
import React from 'react';
import { ReportGrid } from '@/components/report/ReportGrid';
import { ReportStatus } from '@/types';

export const ApprovedReportsList: React.FC = () => (
  <div className="p-6">
    <div className="mb-6">
      <h1 className="text-xl font-bold text-gray-900 tracking-tight">Approved Reports</h1>
      <p className="text-sm text-gray-500 mt-1">Human-approved reports waiting for publish confirmation</p>
    </div>
    <ReportGrid
      statuses={[ReportStatus.Approved, ReportStatus.ReadyToPublish]}
      emptyTitle="No approved reports"
      emptyText="There are currently no approved reports awaiting publication."
    />
  </div>
);
