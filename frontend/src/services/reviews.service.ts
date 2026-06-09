// src/services/reviews.service.ts
import { reportsService } from './reports.service';
import { commentsService } from './comments.service';
import type { Comment } from '@/types';
import { uid } from '@/utils/formatters';

const delay = (ms = 150) => new Promise((r) => setTimeout(r, ms));

export const reviewsService = {
  async saveReview(reportId: string, decision: string): Promise<void> {
    await delay();
    // Always mark humanStatus as 'In Progress' when a review is saved —
    // the decision is a draft until the reviewer explicitly approves/rejects/publishes
    await reportsService.updateHumanStatus(reportId, 'In Progress');
  },

  async markDone(reportId: string): Promise<void> {
    await delay();
    await reportsService.updateStatus(reportId, 'Approved');
    await reportsService.updateHumanStatus(reportId, 'Approved');
  },

  async sendToPublish(reportId: string): Promise<void> {
    await delay();
    await reportsService.updateStatus(reportId, 'Ready to Publish');
    await reportsService.updateHumanStatus(reportId, 'Approved');
    await reportsService.setPublishReady(reportId, true);
  },

  async requestRegeneration(
    reportId: string,
    commentData: { text: string; section: string; priority: string; reviewer: string; version: string }
  ): Promise<void> {
    await delay();
    const comment: Comment = {
      id: uid(),
      reportId,
      version: commentData.version,
      section: commentData.section,
      text: commentData.text,
      priority: commentData.priority,
      reviewer: commentData.reviewer,
      timestamp: new Date().toISOString(),
      status: 'sent to regeneration',
    };
    await commentsService.addComment(reportId, comment);
    await reportsService.updateStatus(reportId, 'Needs Revision');
    await reportsService.updateHumanStatus(reportId, 'Needs Revision');
  },

  async rejectReport(reportId: string): Promise<void> {
    await delay();
    await reportsService.updateStatus(reportId, 'Rejected');
    await reportsService.updateHumanStatus(reportId, 'Rejected');
  },
};
