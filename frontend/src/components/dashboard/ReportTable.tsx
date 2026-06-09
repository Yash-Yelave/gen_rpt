// src/components/dashboard/ReportTable.tsx
import React, { useMemo, useState, useCallback } from 'react';
import { useNavigate } from 'react-router-dom';
import { useReports } from '@/hooks/useReports';
import { formatDate } from '@/utils/formatters';
import { Search } from 'lucide-react';
import { ReportStatus } from '@/types';

// Badge classes inline — no need to import humanStatusBadgeClasses for just 2 states
const STATUS_BADGE: Record<string, string> = {
  'Needs Human Review': 'bg-blue-100 text-blue-700',
  'In Progress':        'bg-orange-100 text-orange-700',
};

export const ReportTable: React.FC = () => {
  const navigate = useNavigate();
  const { data: reports = [], isLoading } = useReports();
  const [search, setSearch] = useState('');

  // Show reports in the active human review phase:
  //   1. status = NeedsHumanReview or AIReviewed → labeled "Needs Human Review"
  //   2. humanStatus = "In Progress" (review saved but not yet finalised)
  const activeReports = useMemo(() => {
    return reports.filter((r) => {
      const isAwaitingReview =
        r.status === ReportStatus.NeedsHumanReview ||
        r.status === ReportStatus.AIReviewed;
      const isInProgress = r.humanStatus === 'In Progress';
      return isAwaitingReview || isInProgress;
    });
  }, [reports]);

  const filtered = useMemo(() => {
    if (!search) return activeReports;
    const q = search.toLowerCase();
    return activeReports.filter((r) =>
      r.title.toLowerCase().includes(q) ||
      r.id.toLowerCase().includes(q)
    );
  }, [activeReports, search]);

  const handleSearch = useCallback((e: React.ChangeEvent<HTMLInputElement>) => {
    setSearch(e.target.value);
  }, []);

  // humanStatus takes priority: if review has been saved it shows "In Progress"
  // otherwise the report is still awaiting a first review
  const getDisplayStatus = (_status: string, humanStatus: string): string => {
    if (humanStatus === 'In Progress') return 'In Progress';
    return 'Needs Human Review';
  };

  if (isLoading) {
    return <div className="text-sm text-gray-400 py-8 text-center">Loading reports…</div>;
  }

  return (
    <>
      {/* Controls */}
      <div className="flex items-center justify-between mb-3 gap-3">
        <h2 className="text-sm font-semibold text-gray-800">Active Reviews</h2>
        <div className="relative">
          <Search className="absolute left-2.5 top-1/2 -translate-y-1/2 w-3.5 h-3.5 text-gray-400 pointer-events-none" />
          <input
            type="search"
            value={search}
            onChange={handleSearch}
            placeholder="Search reports…"
            aria-label="Search reports"
            className="pl-8 pr-3 py-1.5 border border-gray-200 rounded text-sm text-gray-800 outline-none focus:border-blue-500 focus:ring-2 focus:ring-blue-500/10 w-48 bg-white"
          />
        </div>
      </div>

      {/* Table */}
      {filtered.length === 0 ? (
        <div className="bg-white border border-gray-200 rounded-lg py-12 text-center">
          <div className="text-sm font-semibold text-gray-500 mb-1">
            {search ? 'No reports match your search' : 'No active reviews'}
          </div>
          <div className="text-xs text-gray-400">
            {search ? 'Try a different search term.' : 'All reports have been reviewed or are in other stages.'}
          </div>
        </div>
      ) : (
        <div className="bg-white border border-gray-200 rounded-lg overflow-hidden">
          <table className="w-full border-collapse" aria-label="Active reviews list">
            <thead>
              <tr>
                {['Report', 'AI Score', 'Review Status', 'Comments', 'Last Updated'].map((h) => (
                  <th
                    key={h}
                    className="bg-gray-50 px-4 py-2 text-left text-[11px] font-semibold text-gray-500 uppercase tracking-wider border-b border-gray-200 whitespace-nowrap"
                  >
                    {h}
                  </th>
                ))}
              </tr>
            </thead>
            <tbody>
              {filtered.map((r) => {
                const displayStatus = getDisplayStatus(r.status, r.humanStatus);
                const badgeClass = STATUS_BADGE[displayStatus] ?? 'bg-gray-100 text-gray-600';

                return (
                  <tr
                    key={r.id}
                    className="border-b border-gray-200 last:border-b-0 hover:bg-blue-50 transition-colors cursor-pointer"
                    onClick={() => navigate(`/review/${r.id}`)}
                    role="button"
                    tabIndex={0}
                    onKeyDown={(e) => { if (e.key === 'Enter' || e.key === ' ') navigate(`/review/${r.id}`); }}
                    aria-label={`Open report: ${r.title}`}
                  >
                    <td className="px-4 py-3">
                      <div className="text-sm font-semibold text-gray-900">{r.title}</div>
                      <div className="text-xs text-gray-400 font-mono">{r.id} · {r.version}</div>
                    </td>
                    <td className="px-4 py-3">
                      {r.aiScore > 0 ? (
                        <span className="text-sm font-bold text-blue-700">{r.aiScore.toFixed(1)}</span>
                      ) : (
                        <span className="text-gray-300">—</span>
                      )}
                    </td>
                    <td className="px-4 py-3">
                      <span className={`inline-flex items-center px-2 py-0.5 rounded-full text-[11px] font-semibold ${badgeClass}`}>
                        {displayStatus}
                      </span>
                    </td>
                    <td className="px-4 py-3">
                      {r.commentCount > 0 ? (
                        <span className="text-xs bg-gray-100 text-gray-600 px-1.5 py-0.5 rounded font-semibold">
                          {r.commentCount}
                        </span>
                      ) : (
                        <span className="text-gray-300 text-xs">—</span>
                      )}
                    </td>
                    <td className="px-4 py-3 text-xs text-gray-400">{formatDate(r.lastUpdated)}</td>
                  </tr>
                );
              })}
            </tbody>
          </table>
        </div>
      )}
    </>
  );
};
