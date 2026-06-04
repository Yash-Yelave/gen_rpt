// src/pages/Published/index.tsx
import React from 'react';
import { ReportGrid } from '@/components/report/ReportGrid';
import { ReportStatus } from '@/types';

export const PublishedList: React.FC = () => (
  <div className="p-6">
    <div className="mb-6">
      <h1 className="text-xl font-bold text-gray-900 tracking-tight">Published Reports</h1>
      <p className="text-sm text-gray-500 mt-1">Live reports that have been fully published</p>
    </div>
    <ReportGrid
      statuses={[ReportStatus.Published]}
      emptyTitle="No published reports"
      emptyText="There are no published reports in the system."
    />
  </div>
);
