// src/components/review/AIReviewCard.tsx
import React from 'react';
import { Bot } from 'lucide-react';
import { SectionCard } from '@/components/common/SectionCard';
import { EmptyState } from '@/components/common/EmptyState';
import { priorityBadgeClasses, scoreColor } from '@/utils/statusHelpers';
import { formatScoreKey } from '@/utils/formatters';
import type { AIReview } from '@/types';

interface Props {
  aiReview: AIReview | null;
}

const ExecChip: React.FC<{ label: string; ready: boolean }> = ({ label, ready }) => (
  <span
    className={`inline-flex items-center gap-1 text-xs font-medium px-2 py-1 rounded ${
      ready
        ? 'bg-green-50 border border-green-100 text-green-700'
        : 'bg-gray-50 border border-gray-200 text-gray-500'
    }`}
  >
    {ready ? '✓' : '×'} {label}
  </span>
);

export const AIReviewCard: React.FC<Props> = ({ aiReview }) => {
  const scoreDisplay = aiReview ? (
    <div className="flex items-center gap-1.5">
      <span className="text-[11px] text-gray-500 font-medium">AI Score</span>
      <span className="text-sm font-bold text-blue-700">{aiReview.scores.overall_score.toFixed(1)}</span>
    </div>
  ) : null;

  return (
    <SectionCard
      title="AI Review"
      icon={<Bot />}
      rightContent={scoreDisplay}
      defaultOpen
    >
      {!aiReview ? (
        <EmptyState small title="No AI Review" text="AI review has not been generated for this report." />
      ) : (
        <div>
          {/* Score Grid */}
          <div className="grid grid-cols-2 gap-2 mb-4">
            {Object.entries(aiReview.scores.components).map(([key, val]) => (
              <div key={key} className="score-item">
                <span className="text-xs text-gray-600 font-medium">{formatScoreKey(key)}</span>
                <span className="text-sm font-bold" style={{ color: scoreColor(val) }}>{val}</span>
              </div>
            ))}
          </div>

          {/* Strengths */}
          {aiReview.recommendations.strengths.length > 0 && (
            <div className="mb-4">
              <div className="text-[11px] font-bold uppercase tracking-wide text-green-700 mb-2">Strengths</div>
              <ul className="flex flex-col gap-1">
                {aiReview.recommendations.strengths.map((s: string, i: number) => (
                  <li key={i} className="review-list-item strength">{s}</li>
                ))}
              </ul>
            </div>
          )}

          {/* Weaknesses */}
          {aiReview.recommendations.weaknesses.length > 0 && (
            <div className="mb-4">
              <div className="text-[11px] font-bold uppercase tracking-wide text-red-700 mb-2">Weaknesses</div>
              <ul className="flex flex-col gap-1">
                {aiReview.recommendations.weaknesses.map((w: string, i: number) => (
                  <li key={i} className="review-list-item weakness">{w}</li>
                ))}
              </ul>
            </div>
          )}

          {/* Priority Improvements */}
          {aiReview.recommendations.priority_improvements.length > 0 && (
            <div className="mb-4">
              <div className="text-[11px] font-bold uppercase tracking-wide text-orange-700 mb-2">Priority Improvements</div>
              {aiReview.recommendations.priority_improvements.map((imp: any, i: number) => (
                <div key={i} className="bg-gray-50 border border-gray-200 rounded p-2.5 mb-2">
                  <div className="flex items-center justify-between mb-1">
                    <span className="text-xs font-semibold text-gray-800">{imp.issue}</span>
                    <span className={`text-[11px] font-semibold px-1.5 py-0.5 rounded ${priorityBadgeClasses(imp.priority_level)}`}>
                      {imp.priority_level}
                    </span>
                  </div>
                  <div className="text-xs text-gray-500 leading-snug">{imp.suggested_fix}</div>
                </div>
              ))}
            </div>
          )}

          {/* Executive Readiness */}
          <div>
            <div className="text-[11px] font-bold uppercase tracking-wide text-gray-500 mb-2">Executive Readiness</div>
            <div className="flex flex-wrap gap-2">
              {[
                { label: 'Board Members', key: 'board_members' as const },
                { label: 'Ministers', key: 'ministers' as const },
                { label: 'CEOs', key: 'ceos' as const },
                { label: 'SWF', key: 'sovereign_wealth_funds' as const },
                { label: 'Senior Exec', key: 'senior_executives' as const },
              ].map((item) => (
                <ExecChip
                  key={item.key}
                  label={item.label}
                  ready={aiReview.recommendations.executive_readiness[item.key]}
                />
              ))}
            </div>
          </div>
        </div>
      )}
    </SectionCard>
  );
};
