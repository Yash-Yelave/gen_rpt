// src/pages/Revisions/index.tsx
import React from 'react';
import { ReportGrid } from '@/components/report/ReportGrid';
import { ReportStatus } from '@/types';

export const RevisionsList: React.FC = () => (
  <div className="p-6">
    <div className="mb-6">
      <h1 className="text-xl font-bold text-gray-900 tracking-tight">Revision Queue</h1>
      <p className="text-sm text-gray-500 mt-1">Reports marked for revision — awaiting backend processing and re-submission</p>
    </div>
    <ReportGrid
      statuses={[ReportStatus.NeedsRevision]}
      emptyTitle="No reports in revision queue"
      emptyText="All reports are on track."
    />
  </div>
);
