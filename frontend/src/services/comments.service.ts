// src/services/comments.service.ts
import type { Comment } from '@/types';
import { reportsService } from './reports.service';

const delay = (ms = 150) => new Promise((r) => setTimeout(r, ms));

export const commentsService = {
  async getByReportId(reportId: string): Promise<Comment[]> {
    await delay();
    const report = await reportsService.getById(reportId);
    return report?.comments ?? [];
  },

  async addComment(reportId: string, comment: Comment): Promise<Comment[]> {
    await delay();
    const reports = await reportsService.getAll();
    const report = reports.find((r) => r.id === reportId);
    if (!report) throw new Error(`Report ${reportId} not found`);
    report.comments.push(comment);
    report.commentCount = report.comments.length;
    return [...report.comments];
  },

  async resolveComment(reportId: string, commentId: string): Promise<Comment[]> {
    await delay();
    const reports = await reportsService.getAll();
    const report = reports.find((r) => r.id === reportId);
    if (!report) throw new Error(`Report ${reportId} not found`);
    const comment = report.comments.find((c: Comment) => c.id === commentId);
    if (comment) comment.status = 'resolved';
    return [...report.comments];
  },
};
