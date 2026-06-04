// src/pages/Revisions/index.tsx
import React from 'react';
import { ReportGrid } from '@/components/report/ReportGrid';
import { ReportStatus } from '@/types';

export const RevisionsList: React.FC = () => (
  <div className="p-6">
    <div className="mb-6">
      <h1 className="text-xl font-bold text-gray-900 tracking-tight">Revisions</h1>
      <p className="text-sm text-gray-500 mt-1">Reports sent back for regeneration based on comments</p>
    </div>
    <ReportGrid
      statuses={[ReportStatus.NeedsRevision, ReportStatus.Rejected]}
      emptyTitle="No reports needing revision"
      emptyText="All reports are on track."
    />
  </div>
);
