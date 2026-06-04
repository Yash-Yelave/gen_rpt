// src/hooks/useReports.ts
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import { reportsService } from '@/services/reports.service';
import { QUERY_KEYS } from '@/utils/constants';
import type { Report } from '@/types';
import { ReportStatus } from '@/types';

export function useReports() {
  return useQuery({
    queryKey: QUERY_KEYS.reports,
    queryFn: () => reportsService.getAll(),
    staleTime: 30_000,
  });
}

export function useReport(id: string) {
  return useQuery({
    queryKey: QUERY_KEYS.report(id),
    queryFn: () => reportsService.getById(id),
    enabled: !!id,
    staleTime: 30_000,
  });
}

export function useDashboardMetrics() {
  const { data: reports = [] } = useReports();
  return {
    total: reports.length,
    pendingHuman: reports.filter((r) =>
      [ReportStatus.NeedsHumanReview, ReportStatus.AIReviewed].includes(r.status as ReportStatus)
    ).length,
    aiApproved: reports.filter((r) => r.aiScore >= 80 && r.aiReview !== null).length,
    readyToPublish: reports.filter((r) => r.publishReady).length,
    needsRevision: reports.filter((r) => r.status === ReportStatus.NeedsRevision).length,
  };
}

export function useFilteredReports(statuses: string[]) {
  const { data: reports = [] } = useReports();
  return reports.filter((r) => statuses.includes(r.status));
}

export function useUpdateReportStatus() {
  const qc = useQueryClient();
  return useMutation({
    mutationFn: ({ id, status }: { id: string; status: string }) =>
      reportsService.updateStatus(id, status),
    onSuccess: () => {
      qc.invalidateQueries({ queryKey: QUERY_KEYS.reports });
    },
  });
}

export function useUpdateHumanStatus() {
  const qc = useQueryClient();
  return useMutation({
    mutationFn: ({ id, humanStatus }: { id: string; humanStatus: string }) =>
      reportsService.updateHumanStatus(id, humanStatus),
    onSuccess: () => {
      qc.invalidateQueries({ queryKey: QUERY_KEYS.reports });
    },
  });
}
