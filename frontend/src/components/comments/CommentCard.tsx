// src/components/comments/CommentCard.tsx
import React from 'react';
import type { Comment } from '@/types';
import { formatDate } from '@/utils/formatters';
import { priorityBadgeClasses, commentStatusBadgeClasses, commentBorderClass } from '@/utils/statusHelpers';
import { useReviewActions } from '@/hooks/useReviewActions';

interface Props {
  comment: Comment;
}

export const CommentCard = React.memo(({ comment: c }: Props) => {
  const { resolveComment } = useReviewActions(c.reportId);

  const handleResolve = () => {
    resolveComment.mutate(c.id);
  };

  return (
    <div
      id={`comment-${c.id}`}
      className={`bg-white border border-gray-200 rounded mb-3 shadow-xs p-3 transition-colors ${commentBorderClass(c.status)}`}
    >
      <div className="flex items-center justify-between mb-2 flex-wrap gap-2">
        <div className="flex items-center gap-2 flex-wrap">
          <span className="text-sm font-semibold text-gray-900">{c.reviewer}</span>
          <span className="text-[11px] font-semibold text-gray-500 bg-gray-100 px-1.5 py-0.5 rounded">
            {c.section}
          </span>
          <span className={`inline-flex items-center px-1.5 py-0.5 rounded-full text-[11px] font-semibold ${priorityBadgeClasses(c.priority)}`}>
            {c.priority}
          </span>
          <span className={`inline-flex items-center px-1.5 py-0.5 rounded-full text-[11px] font-semibold ${commentStatusBadgeClasses(c.status)}`}>
            {c.status}
          </span>
        </div>
        <span className="text-xs text-gray-400 font-medium">{formatDate(c.timestamp)}</span>
      </div>
      
      <div className="text-sm text-gray-700 leading-relaxed mb-3">{c.text}</div>
      
      <div className="flex items-center justify-between pt-2 border-t border-gray-100">
        <div className="flex items-center gap-2">
          {c.status !== 'resolved' ? (
            <button
              onClick={handleResolve}
              disabled={resolveComment.isPending}
              className="text-xs font-semibold text-blue-600 hover:text-blue-800 transition-colors disabled:opacity-50"
            >
              Mark Resolved
            </button>
          ) : (
            <span className="text-xs font-semibold text-green-700 flex items-center gap-1">
              ✓ Resolved
            </span>
          )}
        </div>
      </div>
    </div>
  );
});
CommentCard.displayName = 'CommentCard';
