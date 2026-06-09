// src/pages/Dashboard/index.tsx
import React from 'react';
import { StatCard } from '@/components/dashboard/StatCard';
import { ReportTable } from '@/components/dashboard/ReportTable';
import { useDashboardMetrics } from '@/hooks/useReports';
import { formatDate } from '@/utils/formatters';

export const Dashboard: React.FC = () => {
  const metrics = useDashboardMetrics();

  return (
    <div className="p-6">
      <div className="flex items-center justify-between mb-6">
        <div>
          <h1 className="text-xl font-bold text-gray-900 tracking-tight">Dashboard</h1>
          <p className="text-sm text-gray-500 mt-1">Overview of report review pipeline</p>
        </div>
        <div className="text-xs text-gray-400">
          Updated {formatDate(new Date().toISOString())}
        </div>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4 mb-8">
        <StatCard label="Total Reports" value={metrics.total} meta="This cycle" />
        <StatCard label="Pending Review" value={metrics.pendingHuman} meta="Awaiting human decision" accent="blue" />
        <StatCard label="Approved Reports" value={metrics.approvedReports} meta="Ready to publish" accent="green" />
        <StatCard label="Needs Revision" value={metrics.needsRevision} meta="Awaiting revision" accent="orange" />
      </div>

      <ReportTable />
    </div>
  );
};
