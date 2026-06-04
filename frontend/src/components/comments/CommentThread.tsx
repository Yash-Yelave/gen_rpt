// src/components/comments/CommentThread.tsx
import React from 'react';
import { MessageSquare } from 'lucide-react';
import { SectionCard } from '@/components/common/SectionCard';
import { EmptyState } from '@/components/common/EmptyState';
import { CommentCard } from './CommentCard';
import type { Report } from '@/types';

interface Props {
  report: Report;
}

export const CommentThread: React.FC<Props> = ({ report }) => {
  const { comments = [] } = report;

  const countBadge = comments.length > 0 ? (
    <span className="bg-gray-100 text-gray-700 text-[11px] font-bold px-2 py-0.5 rounded-full">
      {comments.length}
    </span>
  ) : null;

  return (
    <SectionCard title="Comments" icon={<MessageSquare />} rightContent={countBadge} defaultOpen>
      {comments.length === 0 ? (
        <EmptyState
          small
          title="No comments yet"
          text="Use the human review panel to add a comment."
        />
      ) : (
        <div className="flex flex-col">
          {comments.map((c) => (
            <CommentCard key={c.id} comment={c} />
          ))}
        </div>
      )}
    </SectionCard>
  );
};
