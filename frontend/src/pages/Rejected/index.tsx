// src/pages/Rejected/index.tsx
import React from 'react';
import { ReportGrid } from '@/components/report/ReportGrid';
import { ReportStatus } from '@/types';

export const RejectedList: React.FC = () => (
  <div className="p-6">
    <div className="mb-6">
      <h1 className="text-xl font-bold text-gray-900 tracking-tight">Rejected Reports</h1>
      <p className="text-sm text-gray-500 mt-1">Reports that have been rejected and will not proceed to publication</p>
    </div>
    <ReportGrid
      statuses={[ReportStatus.Rejected]}
      emptyTitle="No rejected reports"
      emptyText="There are no rejected reports in the system."
    />
  </div>
);
