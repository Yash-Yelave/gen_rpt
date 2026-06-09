// src/components/review/HumanReviewCard.tsx
import React, { useState } from 'react';
import { User, Send, CheckCircle, AlertTriangle, XCircle } from 'lucide-react';
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

const decisionConfig: Record<string, { selectedClass: string; icon: React.ReactNode }> = {
  Approved:         { selectedClass: 'bg-green-50 border-green-600 text-green-700 font-semibold', icon: <CheckCircle className="w-4 h-4" /> },
  'Needs Revision': { selectedClass: 'bg-orange-50 border-orange-600 text-orange-700 font-semibold', icon: <AlertTriangle className="w-4 h-4" /> },
  Rejected:         { selectedClass: 'bg-red-50 border-red-600 text-red-700 font-semibold', icon: <XCircle className="w-4 h-4" /> },
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

  const [showRejectModal, setShowRejectModal] = useState(false);

  const { reviewerName } = useAuthStore();
  const { showToast } = useUIStore();
  const actions = useReviewActions(report.id);

  const handleDecisionChange = (d: string) => {
    if (d === 'Rejected') {
      setDecision(d);
      setShowRejectModal(true);
    } else {
      setDecision(d);
    }
  };

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

  const handlePublish = async () => {
    await actions.sendToPublish.mutateAsync();
    showToast('Report sent to publish queue', 'success');
  };

  const handleConfirmReject = async () => {
    await actions.rejectReport.mutateAsync();
    setShowRejectModal(false);
    showToast('Report rejected', 'error');
  };

  const handleCancelReject = () => {
    setShowRejectModal(false);
    setDecision('');
  };

  return (
    <>
      {/* Rejection Confirmation Modal */}
      {showRejectModal && (
        <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/30">
          <div className="bg-white rounded-lg border border-gray-200 shadow-xl p-6 max-w-sm w-full mx-4">
            <div className="flex items-center gap-3 mb-3">
              <div className="w-9 h-9 rounded-full bg-red-100 flex items-center justify-center flex-shrink-0">
                <XCircle className="w-5 h-5 text-red-600" />
              </div>
              <div>
                <div className="text-sm font-bold text-gray-900">Reject Report</div>
                <div className="text-xs text-gray-500">This action cannot be undone</div>
              </div>
            </div>
            <p className="text-sm text-gray-700 mb-5">
              Are you sure you want to reject <span className="font-semibold">"{report.title}"</span>?
            </p>
            <div className="flex gap-2">
              <button
                onClick={handleCancelReject}
                className="flex-1 px-3 py-2 border border-gray-200 rounded text-sm font-medium text-gray-700 hover:bg-gray-50 transition-colors"
              >
                Cancel
              </button>
              <button
                onClick={handleConfirmReject}
                disabled={actions.rejectReport.isPending}
                className="flex-1 px-3 py-2 bg-red-600 text-white rounded text-sm font-semibold hover:bg-red-700 transition-colors disabled:opacity-50"
              >
                Reject Report
              </button>
            </div>
          </div>
        </div>
      )}

      <SectionCard title="Human Review" icon={<User />} defaultOpen>
        {/* Decision Selector */}
        <div className="mb-4">
          <label className="block text-[11px] font-semibold text-gray-500 uppercase tracking-wide mb-2">
            Review Decision
          </label>
          <div className="flex flex-col gap-2" role="radiogroup" aria-label="Review decision">
            {DECISIONS.map((d) => {
              const config = decisionConfig[d];
              const isSelected = decision === d;
              return (
                <label
                  key={d}
                  className={`flex items-center gap-2 px-4 py-2.5 border rounded-md cursor-pointer transition-colors text-sm focus-within:ring-2 focus-within:ring-blue-500/50 ${
                    isSelected ? config.selectedClass : 'border-gray-200 text-gray-600 hover:bg-gray-50'
                  }`}
                >
                  <input
                    type="radio"
                    name="human-decision"
                    value={d}
                    checked={isSelected}
                    onChange={() => handleDecisionChange(d)}
                    className="sr-only"
                  />
                  {config.icon}
                  <span className="font-medium">{d}</span>
                </label>
              );
            })}
          </div>
        </div>

        {/* APPROVED FLOW */}
        {decision === 'Approved' && (
          <div className="pt-3 border-t border-gray-200">
            <div className="flex items-center gap-2 p-3 bg-green-50 border border-green-100 rounded-md mb-3">
              <CheckCircle className="w-4 h-4 text-green-600 flex-shrink-0" />
              <span className="text-xs text-green-700 font-medium">
                This report is approved and ready for publishing.
              </span>
            </div>
            <button
              onClick={handlePublish}
              disabled={actions.sendToPublish.isPending}
              className="w-full flex items-center justify-center gap-2 px-3 py-2.5 bg-blue-700 text-white text-sm font-semibold rounded hover:bg-blue-800 transition-colors disabled:opacity-50 focus:outline-none focus-visible:ring-2 focus-visible:ring-blue-500/50"
            >
              <Send className="w-4 h-4" />
              Publish Report
            </button>
          </div>
        )}

        {/* NEEDS REVISION FLOW */}
        {decision === 'Needs Revision' && (
          <div className="pt-3 border-t border-gray-200 flex flex-col gap-3">
            <div className="flex items-center gap-2 p-3 bg-orange-50 border border-orange-100 rounded-md">
              <AlertTriangle className="w-4 h-4 text-orange-600 flex-shrink-0" />
              <span className="text-xs text-orange-700 font-medium">
                This report requires revision before approval.
              </span>
            </div>

            {/* Section */}
            <div>
              <label className="block text-[11px] font-semibold text-gray-500 uppercase tracking-wide mb-1.5" htmlFor="section-select">
                Report Section
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
            <div>
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

            {/* Revision Instructions */}
            <div>
              <label className="block text-[11px] font-semibold text-gray-500 uppercase tracking-wide mb-1.5" htmlFor="comment-input">
                Revision Instructions
              </label>
              <textarea
                id="comment-input"
                rows={4}
                value={commentText}
                onChange={(e) => setCommentText(e.target.value)}
                placeholder="Describe what needs to be revised in this section…"
                className="w-full px-3 py-2 border border-gray-200 rounded text-sm text-gray-800 outline-none focus:border-blue-500 focus:ring-2 focus:ring-blue-500/10 bg-white resize-y leading-relaxed"
              />
            </div>

            <button
              onClick={handleSubmitComment}
              disabled={actions.submitComment.isPending}
              className="w-full flex items-center justify-center gap-1.5 px-3 py-2 bg-white border border-gray-200 text-gray-700 text-sm font-medium rounded hover:bg-gray-50 hover:border-gray-300 transition-colors disabled:opacity-50 focus:outline-none focus-visible:ring-2 focus-visible:ring-blue-500/50"
            >
              + Add Revision Comment
            </button>

            <button
              onClick={handleSaveReview}
              disabled={actions.saveReview.isPending}
              className="w-full flex items-center justify-center gap-1.5 px-3 py-2.5 bg-orange-600 text-white text-sm font-semibold rounded hover:bg-orange-700 transition-colors disabled:opacity-50 focus:outline-none focus-visible:ring-2 focus-visible:ring-orange-500/50"
            >
              Save Review
            </button>
          </div>
        )}

        {/* NO DECISION – prompt */}
        {!decision && (
          <div className="pt-3 border-t border-gray-200">
            <p className="text-xs text-gray-400 text-center py-2">
              Select a decision above to continue the review.
            </p>
          </div>
        )}
      </SectionCard>
    </>
  );
};
