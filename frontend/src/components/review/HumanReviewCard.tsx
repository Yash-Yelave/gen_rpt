// src/components/review/HumanReviewCard.tsx
import React from 'react';
import { User } from 'lucide-react';
import { SectionCard } from '@/components/common/SectionCard';
import { useReviewStore } from '@/store/reviewStore';
import { useReviewActions } from '@/hooks/useReviewActions';
import { useAuthStore } from '@/store/authStore';
import { useUIStore } from '@/store/uiStore';
import { REPORT_SECTIONS, COMMENT_PRIORITIES } from '@/utils/constants';
import type { Report } from '@/types';

interface Props {
  report: Report;
}

const DECISIONS = ['Approved', 'Needs Revision', 'Rejected'] as const;

const decisionSelectedClass: Record<string, string> = {
  Approved:         'bg-green-50 border-green-600 text-green-700 font-semibold',
  'Needs Revision': 'bg-orange-50 border-orange-600 text-orange-700 font-semibold',
  Rejected:         'bg-red-50 border-red-600 text-red-700 font-semibold',
};

export const HumanReviewCard: React.FC<Props> = ({ report }) => {
  const decision = useReviewStore((s) => s.decision);
  const commentText = useReviewStore((s) => s.commentText);
  const commentSection = useReviewStore((s) => s.commentSection);
  const commentPriority = useReviewStore((s) => s.commentPriority);
  const setDecision = useReviewStore((s) => s.setDecision);
  const setCommentText = useReviewStore((s) => s.setCommentText);
  const setCommentSection = useReviewStore((s) => s.setCommentSection);
  const setCommentPriority = useReviewStore((s) => s.setCommentPriority);

  const { reviewerName } = useAuthStore();
  const { showToast } = useUIStore();
  const actions = useReviewActions(report.id);

  const handleSubmitComment = async () => {
    if (!commentText.trim()) {
      showToast('Please enter a comment before submitting.', 'error');
      return;
    }
    await actions.submitComment.mutateAsync({
      reportId: report.id,
      version: report.version,
      section: commentSection,
      text: commentText,
      priority: commentPriority,
      reviewer: reviewerName,
    });
    setCommentText('');
    showToast('Comment added to review thread', 'success');
  };

  const handleSaveReview = async () => {
    if (decision) await actions.saveReview.mutateAsync(decision);
    showToast('Review saved successfully', 'success');
  };

  const handleMarkDone = async () => {
    await actions.markDone.mutateAsync();
    showToast('Report marked as done (Approved)', 'success');
  };

  const handleSendToPublish = async () => {
    await actions.sendToPublish.mutateAsync();
    showToast('Report sent to publish queue', 'success');
  };

  const handleRequestRegeneration = async () => {
    if (!commentText.trim()) {
      showToast('Add a comment describing the revision needed before requesting regeneration.', 'error');
      return;
    }
    await actions.requestRegeneration.mutateAsync({
      text: commentText,
      section: commentSection,
      priority: commentPriority,
      reviewer: reviewerName,
      version: report.version,
    });
    setCommentText('');
    showToast('Report sent for AI regeneration with your comments', 'info');
  };

  const handleReject = async () => {
    if (!window.confirm(`Are you sure you want to reject "${report.title}"?`)) return;
    await actions.rejectReport.mutateAsync();
    showToast('Report rejected', 'error');
  };

  return (
    <SectionCard title="Human Review" icon={<User />} defaultOpen>
      {/* Decision Selector */}
      <div className="mb-3">
        <label className="block text-[11px] font-semibold text-gray-500 uppercase tracking-wide mb-1.5">Decision</label>
        <div className="flex gap-2 flex-wrap" role="radiogroup" aria-label="Review decision">
          {DECISIONS.map((d) => (
            <label
              key={d}
              className={`flex items-center gap-1.5 px-3 py-1.5 border rounded cursor-pointer transition-colors text-sm text-gray-600 hover:bg-gray-50 focus-within:ring-2 focus-within:ring-blue-500/50 ${
                decision === d ? decisionSelectedClass[d] : 'border-gray-200'
              }`}
            >
              <input
                type="radio"
                name="human-decision"
                value={d}
                checked={decision === d}
                onChange={() => setDecision(d)}
                className="sr-only"
              />
              {d}
            </label>
          ))}
        </div>
      </div>

      {/* Section */}
      <div className="mb-3">
        <label className="block text-[11px] font-semibold text-gray-500 uppercase tracking-wide mb-1.5" htmlFor="section-select">
          Section
        </label>
        <select
          id="section-select"
          value={commentSection}
          onChange={(e) => setCommentSection(e.target.value)}
          className="w-full px-3 py-1.5 border border-gray-200 rounded text-sm text-gray-800 outline-none focus:border-blue-500 focus:ring-2 focus:ring-blue-500/10 bg-white cursor-pointer"
        >
          {REPORT_SECTIONS.map((s: string) => <option key={s} value={s}>{s}</option>)}
        </select>
      </div>

      {/* Priority */}
      <div className="mb-3">
        <label className="block text-[11px] font-semibold text-gray-500 uppercase tracking-wide mb-1.5" htmlFor="priority-select">
          Priority
        </label>
        <select
          id="priority-select"
          value={commentPriority}
          onChange={(e) => setCommentPriority(e.target.value)}
          className="w-full px-3 py-1.5 border border-gray-200 rounded text-sm text-gray-800 outline-none focus:border-blue-500 focus:ring-2 focus:ring-blue-500/10 bg-white cursor-pointer"
        >
          {COMMENT_PRIORITIES.map((p: string) => <option key={p} value={p}>{p}</option>)}
        </select>
      </div>

      {/* Comment */}
      <div className="mb-3">
        <label className="block text-[11px] font-semibold text-gray-500 uppercase tracking-wide mb-1.5" htmlFor="comment-input">
          Comment
        </label>
        <textarea
          id="comment-input"
          rows={4}
          value={commentText}
          onChange={(e) => setCommentText(e.target.value)}
          placeholder="Add your comment or revision note…"
          className="w-full px-3 py-2 border border-gray-200 rounded text-sm text-gray-800 outline-none focus:border-blue-500 focus:ring-2 focus:ring-blue-500/10 bg-white resize-y leading-relaxed"
        />
      </div>

      <button
        onClick={handleSubmitComment}
        disabled={actions.submitComment.isPending}
        className="w-full flex items-center justify-center gap-1.5 px-3 py-2 bg-white border border-gray-200 text-gray-700 text-sm font-medium rounded hover:bg-gray-50 hover:border-gray-300 transition-colors disabled:opacity-50 focus:outline-none focus-visible:ring-2 focus-visible:ring-blue-500/50 mb-3"
      >
        + Submit Comment
      </button>

      {/* Action Buttons */}
      <div className="flex flex-col gap-2 pt-3 border-t border-gray-200">
        <button
          onClick={handleSaveReview}
          disabled={actions.saveReview.isPending}
          className="w-full flex items-center justify-center gap-1.5 px-3 py-2 bg-white border border-gray-200 text-gray-700 text-sm font-medium rounded hover:bg-gray-50 transition-colors disabled:opacity-50 focus:outline-none focus-visible:ring-2 focus-visible:ring-blue-500/50"
        >
          Save Review
        </button>
        <button
          onClick={handleMarkDone}
          disabled={actions.markDone.isPending}
          className="w-full flex items-center justify-center gap-1.5 px-3 py-2 bg-green-600 text-white text-sm font-medium rounded hover:bg-green-700 transition-colors disabled:opacity-50 focus:outline-none focus-visible:ring-2 focus-visible:ring-green-500/50"
        >
          ✓ Mark as Done
        </button>
        <button
          onClick={handleSendToPublish}
          disabled={actions.sendToPublish.isPending}
          className="w-full flex items-center justify-center gap-1.5 px-3 py-2 bg-blue-700 text-white text-sm font-medium rounded hover:bg-blue-800 transition-colors disabled:opacity-50 focus:outline-none focus-visible:ring-2 focus-visible:ring-blue-500/50"
        >
          Send to Publish
        </button>
        <button
          onClick={handleRequestRegeneration}
          disabled={actions.requestRegeneration.isPending}
          className="w-full flex items-center justify-center gap-1.5 px-3 py-2 bg-red-600 text-white text-sm font-medium rounded hover:bg-red-700 transition-colors disabled:opacity-50 focus:outline-none focus-visible:ring-2 focus-visible:ring-red-500/50"
        >
          ↻ Request Regeneration
        </button>
        <button
          onClick={handleReject}
          disabled={actions.rejectReport.isPending}
          className="w-full px-3 py-2 bg-transparent border border-red-100 text-red-600 text-sm font-medium rounded hover:bg-red-50 transition-colors disabled:opacity-50 focus:outline-none focus-visible:ring-2 focus-visible:ring-red-500/50"
        >
          Reject Report
        </button>
      </div>
    </SectionCard>
  );
};
