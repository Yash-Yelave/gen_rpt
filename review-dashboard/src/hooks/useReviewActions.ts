// src/hooks/useReviewActions.ts
import { useMutation, useQueryClient } from '@tanstack/react-query';
import { reviewsService } from '@/services/reviews.service';
import { commentsService } from '@/services/comments.service';
import { QUERY_KEYS } from '@/utils/constants';
import { uid } from '@/utils/formatters';
import type { Comment } from '@/types';

export function useReviewActions(reportId: string) {
  const qc = useQueryClient();

  const invalidate = () => {
    qc.invalidateQueries({ queryKey: QUERY_KEYS.reports });
    qc.invalidateQueries({ queryKey: QUERY_KEYS.report(reportId) });
    qc.invalidateQueries({ queryKey: QUERY_KEYS.comments(reportId) });
  };

  const saveReview = useMutation({
    mutationFn: (decision: string) => reviewsService.saveReview(reportId, decision),
    onSuccess: invalidate,
  });

  const markDone = useMutation({
    mutationFn: () => reviewsService.markDone(reportId),
    onSuccess: invalidate,
  });

  const sendToPublish = useMutation({
    mutationFn: () => reviewsService.sendToPublish(reportId),
    onSuccess: invalidate,
  });

  const requestRegeneration = useMutation({
    mutationFn: (params: { text: string; section: string; priority: string; reviewer: string; version: string }) =>
      reviewsService.requestRegeneration(reportId, params),
    onSuccess: invalidate,
  });

  const rejectReport = useMutation({
    mutationFn: () => reviewsService.rejectReport(reportId),
    onSuccess: invalidate,
  });

  const submitComment = useMutation({
    mutationFn: (comment: Omit<Comment, 'id' | 'timestamp' | 'status'>) =>
      commentsService.addComment(reportId, {
        ...comment,
        id: uid(),
        timestamp: new Date().toISOString(),
        status: 'open',
      }),
    onSuccess: invalidate,
  });

  const resolveComment = useMutation({
    mutationFn: (commentId: string) => commentsService.resolveComment(reportId, commentId),
    onSuccess: invalidate,
  });

  return { saveReview, markDone, sendToPublish, requestRegeneration, rejectReport, submitComment, resolveComment };
}
