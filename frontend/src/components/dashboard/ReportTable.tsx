// src/components/dashboard/ReportTable.tsx
import React, { useMemo, useState, useCallback } from 'react';
import { useNavigate } from 'react-router-dom';
import { useReports } from '@/hooks/useReports';
import { StatusBadge } from '@/components/common/StatusBadge';
import { humanStatusBadgeClasses } from '@/utils/statusHelpers';
import { formatDate } from '@/utils/formatters';
import { REPORT_STATUSES } from '@/utils/constants';
import { Search } from 'lucide-react';

export const ReportTable: React.FC = () => {
  const navigate = useNavigate();
  const { data: reports = [], isLoading } = useReports();
  const [search, setSearch] = useState('');
  const [statusFilter, setStatusFilter] = useState('');

  const filtered = useMemo(() => {
    let r = reports;
    if (search) {
      const q = search.toLowerCase();
      r = r.filter((rep) =>
        rep.title.toLowerCase().includes(q) ||
        rep.id.toLowerCase().includes(q) ||
        rep.status.toLowerCase().includes(q)
      );
    }
    if (statusFilter) {
      r = r.filter((rep) => rep.status === statusFilter);
    }
    return r;
  }, [reports, search, statusFilter]);

  const handleSearch = useCallback((e: React.ChangeEvent<HTMLInputElement>) => {
    setSearch(e.target.value);
  }, []);

  if (isLoading) {
    return <div className="text-sm text-gray-400 py-8 text-center">Loading reports…</div>;
  }

  return (
    <>
      {/* Controls */}
      <div className="flex items-center justify-between mb-3 gap-3">
        <h2 className="text-sm font-semibold text-gray-800">Recent Reports</h2>
        <div className="flex items-center gap-2">
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
          <select
            value={statusFilter}
            onChange={(e) => setStatusFilter(e.target.value)}
            aria-label="Filter by status"
            className="px-3 py-1.5 border border-gray-200 rounded text-sm text-gray-800 outline-none focus:border-blue-500 focus:ring-2 focus:ring-blue-500/10 bg-white cursor-pointer"
          >
            <option value="">All Statuses</option>
            {REPORT_STATUSES.map((s) => (
              <option key={s} value={s}>{s}</option>
            ))}
          </select>
        </div>
      </div>

      {/* Table */}
      {filtered.length === 0 ? (
        <div className="bg-white border border-gray-200 rounded-lg py-12 text-center">
          <div className="text-sm font-semibold text-gray-500 mb-1">No reports found</div>
          <div className="text-xs text-gray-400">No reports match your current filters.</div>
        </div>
      ) : (
        <div className="bg-white border border-gray-200 rounded-lg overflow-hidden">
          <table className="w-full border-collapse" aria-label="Reports list">
            <thead>
              <tr>
                {['Report', 'ID', 'AI Score', 'Status', 'Human Review', 'Comments', 'Last Updated', ''].map((h) => (
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
              {filtered.map((r) => (
                <tr
                  key={r.id}
                  className="border-b border-gray-200 last:border-b-0 hover:bg-blue-50 transition-colors"
                >
                  <td className="px-4 py-3">
                    <div className="text-sm font-semibold text-gray-900">{r.title}</div>
                    <div className="text-xs text-gray-400 font-mono">{r.id} · {r.version}</div>
                  </td>
                  <td className="px-4 py-3">
                    <span className="text-xs text-gray-400 font-mono">{r.id}</span>
                  </td>
                  <td className="px-4 py-3">
                    {r.aiScore > 0 ? (
                      <span className="flex items-center gap-1.5">
                        <span className="text-sm font-bold text-blue-700">{r.aiScore.toFixed(1)}</span>
                        <span className="text-xs bg-gray-100 text-gray-600 px-1.5 py-0.5 rounded">{r.aiGrade}</span>
                      </span>
                    ) : (
                      <span className="text-gray-300">—</span>
                    )}
                  </td>
                  <td className="px-4 py-3">
                    <StatusBadge status={r.status} />
                  </td>
                  <td className="px-4 py-3">
                    <span className={`inline-flex items-center px-1.5 py-0.5 rounded-full text-[11px] font-semibold ${humanStatusBadgeClasses(r.humanStatus)}`}>
                      {r.humanStatus}
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
                  <td className="px-4 py-3">
                    <button
                      className="px-2.5 py-1 bg-blue-700 text-white text-xs font-medium rounded hover:bg-blue-800 transition-colors"
                      onClick={() => navigate(`/review/${r.id}`)}
                      aria-label={`Open review for ${r.title}`}
                    >
                      Open
                    </button>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}
    </>
  );
};
