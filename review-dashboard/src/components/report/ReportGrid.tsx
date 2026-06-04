// src/components/report/ReportGrid.tsx
import React from 'react';
import { ReportCard } from './ReportCard';
import { EmptyState } from '@/components/common/EmptyState';
import { useFilteredReports } from '@/hooks/useReports';
import { FileSearch } from 'lucide-react';

interface Props {
  statuses: string[];
  emptyTitle: string;
  emptyText?: string;
}

export const ReportGrid: React.FC<Props> = ({ statuses, emptyTitle, emptyText }) => {
  const reports = useFilteredReports(statuses);

  if (reports.length === 0) {
    return (
      <EmptyState
        icon={<FileSearch className="w-full h-full" />}
        title={emptyTitle}
        text={emptyText}
      />
    );
  }

  return (
    <div className="grid grid-cols-1 md:grid-cols-2 xl:grid-cols-3 gap-4">
      {reports.map((r) => (
        <ReportCard key={r.id} report={r} />
      ))}
    </div>
  );
};
