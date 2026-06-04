// src/services/publish.service.ts
import { reportsService } from './reports.service';
import type { PublishRecord } from '@/types';

const _publishLog: PublishRecord[] = [];

export const publishService = {
  async publish(reportId: string, publishedBy: string, version: string): Promise<PublishRecord> {
    await reportsService.updateStatus(reportId, 'Published');
    const record: PublishRecord = {
      reportId,
      publishedAt: new Date().toISOString(),
      publishedBy,
      version,
    };
    _publishLog.push(record);
    return record;
  },

  async getPublishLog(): Promise<PublishRecord[]> {
    return [..._publishLog];
  },
};
