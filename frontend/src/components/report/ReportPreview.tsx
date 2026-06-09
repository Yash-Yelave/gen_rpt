// src/components/report/ReportPreview.tsx
import React, { useState } from 'react';
import { Bot, FileText } from 'lucide-react';
import type { Report, ReportSection } from '@/types';
import { useUIStore } from '@/store/uiStore';
import { formatScoreKey } from '@/utils/formatters';
import { scoreColor, priorityBadgeClasses } from '@/utils/statusHelpers';

interface Props {
  report: Report;
}

// Contributors list (static per spec)
const CONTRIBUTORS = [
  { name: 'Yash Yelave', initials: 'YY' },
  { name: 'Jacob', initials: 'JC' },
  { name: 'YFen', initials: 'YF' },
  { name: 'Niluksha', initials: 'NL' },
];

const AVATAR_COLORS = [
  'bg-blue-600',
  'bg-indigo-600',
  'bg-violet-600',
  'bg-teal-600',
];

function renderSectionBody(body: string): React.ReactNode {
  return body
    .split('\n\n')
    .map((para, i) => {
      const trimmed = para.trim();
      if (!trimmed) return null;
      const lines = trimmed.split('\n');
      const isList = lines.some((l) => l.trim().startsWith('- ') || l.trim().match(/^\d+\./));
      if (isList) {
        return (
          <ul key={i} className="list-disc pl-5 mb-3">
            {lines.map((line, j) => (
              <li key={j} className="text-gray-700 mb-1">
                {line.replace(/^[-\d.]+\s*/, '')}
              </li>
            ))}
          </ul>
        );
      }
      return <p key={i} className="mb-3 text-gray-700">{trimmed}</p>;
    });
}

const ReportSectionBlock = React.memo(({ section }: { section: ReportSection }) => {
  if (section.isDisclaimer) {
    return (
      <div className="report-disclaimer">
        <strong>Disclaimer:</strong> {section.body}
      </div>
    );
  }
  return (
    <div className="mb-6">
      <div className="report-section-heading">{section.heading}</div>
      <div className="report-section-body">{renderSectionBody(section.body)}</div>
    </div>
  );
});
ReportSectionBlock.displayName = 'ReportSectionBlock';

// AI Review tab content (inline, extracted from AIReviewCard)
const AIReviewPane: React.FC<{ report: Report }> = ({ report }) => {
  const { aiReview } = report;
  if (!aiReview) {
    return (
      <div className="flex flex-col items-center justify-center py-16 text-center">
        <Bot className="w-8 h-8 text-gray-300 mb-2" />
        <div className="text-sm font-semibold text-gray-500">No AI Review</div>
        <div className="text-xs text-gray-400 mt-1">AI review has not been generated for this report.</div>
      </div>
    );
  }

  return (
    <div className="py-4">
      {/* Score header */}
      <div className="flex items-center gap-3 mb-5 p-3 bg-blue-50 border border-blue-100 rounded-md">
        <div>
          <div className="text-[11px] font-semibold text-blue-600 uppercase tracking-wide">AI Score</div>
          <div className="text-2xl font-bold text-blue-700">{aiReview.scores.overall_score.toFixed(1)}</div>
        </div>
        <div className="h-10 w-px bg-blue-200 mx-1" />
        <div className="grid grid-cols-2 gap-x-6 gap-y-1 flex-1">
          {Object.entries(aiReview.scores.components).map(([key, val]) => (
            <div key={key} className="flex items-center justify-between gap-2">
              <span className="text-xs text-gray-600">{formatScoreKey(key)}</span>
              <span className="text-xs font-bold" style={{ color: scoreColor(val) }}>{val}</span>
            </div>
          ))}
        </div>
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

      {/* Data Gaps */}
      {aiReview.dataGaps && aiReview.dataGaps.length > 0 && (
        <div className="mb-4">
          <div className="text-[11px] font-bold uppercase tracking-wide text-orange-700 mb-2">Data Gaps</div>
          <ul className="flex flex-col gap-1">
            {aiReview.dataGaps.map((g: string, i: number) => (
              <li key={i} className="review-list-item weakness">{g}</li>
            ))}
          </ul>
        </div>
      )}

      {/* Writing Flaws */}
      {aiReview.writingFlaws && aiReview.writingFlaws.length > 0 && (
        <div className="mb-4">
          <div className="text-[11px] font-bold uppercase tracking-wide text-red-700 mb-2">Writing Flaws</div>
          <ul className="flex flex-col gap-1">
            {aiReview.writingFlaws.map((f: string, i: number) => (
              <li key={i} className="review-list-item weakness">{f}</li>
            ))}
          </ul>
        </div>
      )}

      {/* Strategic Gaps */}
      {aiReview.strategicGaps && aiReview.strategicGaps.length > 0 && (
        <div className="mb-4">
          <div className="text-[11px] font-bold uppercase tracking-wide text-orange-700 mb-2">Strategic Gaps</div>
          <ul className="flex flex-col gap-1">
            {aiReview.strategicGaps.map((g: string, i: number) => (
              <li key={i} className="review-list-item weakness">{g}</li>
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
    </div>
  );
};

export const ReportPreview: React.FC<Props> = ({ report }) => {
  const { zoomLevel, zoomIn, zoomOut } = useUIStore();
  const { reportContent: content, title, id, version, aiScore } = report;
  const [activeTab, setActiveTab] = useState<'report' | 'ai-review'>('report');

  return (
    <div className="flex flex-col border-r border-gray-200 bg-gray-100 overflow-hidden h-full">
      {/* Tab Bar */}
      <div className="flex items-center bg-white border-b border-gray-200 flex-shrink-0 px-2">
        <button
          onClick={() => setActiveTab('report')}
          className={`flex items-center gap-1.5 px-4 py-3 text-sm font-medium border-b-2 transition-colors ${
            activeTab === 'report'
              ? 'border-blue-700 text-blue-700'
              : 'border-transparent text-gray-500 hover:text-gray-800'
          }`}
        >
          <FileText className="w-3.5 h-3.5" />
          Report
        </button>
        <button
          onClick={() => setActiveTab('ai-review')}
          className={`flex items-center gap-1.5 px-4 py-3 text-sm font-medium border-b-2 transition-colors ${
            activeTab === 'ai-review'
              ? 'border-blue-700 text-blue-700'
              : 'border-transparent text-gray-500 hover:text-gray-800'
          }`}
        >
          <Bot className="w-3.5 h-3.5" />
          AI Review
        </button>

        {/* Zoom controls — only shown on report tab */}
        {activeTab === 'report' && (
          <div className="flex items-center gap-2 ml-auto">
            <button
              onClick={zoomOut}
              className="text-xs text-gray-500 hover:bg-gray-100 px-2 py-1 rounded transition-colors font-medium"
              aria-label="Zoom out"
            >
              A−
            </button>
            <span className="text-xs text-gray-400 min-w-[36px] text-center">{zoomLevel}%</span>
            <button
              onClick={zoomIn}
              className="text-xs text-gray-500 hover:bg-gray-100 px-2 py-1 rounded transition-colors font-medium"
              aria-label="Zoom in"
            >
              A+
            </button>
          </div>
        )}
      </div>

      {/* Content */}
      <div className="flex-1 overflow-y-auto p-6">
        {activeTab === 'report' ? (
          <div
            className="report-document"
            style={{ fontSize: `${zoomLevel / 100}rem` }}
          >
            {/* Document Header */}
            <div className="border-b-2 border-blue-700 pb-5 mb-6">
              <div className="text-xs font-bold text-blue-700 uppercase tracking-widest mb-3">
                {content.brand} · {content.label}
              </div>
              <div className="text-[22px] font-bold text-gray-900 tracking-tight leading-snug mb-2">{title}</div>
              <div className="flex items-center gap-4 flex-wrap mb-3">
                <span className="text-xs text-gray-400">ID: {id}</span>
                <span className="text-xs text-gray-400">{version}</span>
                <span className="text-xs text-gray-400">{content.date}</span>
              </div>

              {/* AI Score (no grade) */}
              {aiScore > 0 && (
                <div className="flex gap-3 mb-4">
                  <span className="bg-blue-50 border border-blue-100 text-blue-700 text-xs font-bold px-2.5 py-1 rounded">
                    AI Score: {aiScore.toFixed(1)}
                  </span>
                </div>
              )}

              {/* Contributors */}
              <div className="flex items-center gap-3 flex-wrap">
                <span className="text-xs text-gray-500 font-medium">Worked On By:</span>
                <div className="flex items-center gap-1.5">
                  {CONTRIBUTORS.map((c, i) => (
                    <div key={c.name} className="relative group">
                      <div
                        className={`w-7 h-7 rounded-full ${AVATAR_COLORS[i % AVATAR_COLORS.length]} text-white text-[11px] font-bold flex items-center justify-center border-2 border-white -ml-1 first:ml-0 cursor-default`}
                        title={c.name}
                      >
                        {c.initials}
                      </div>
                      <div className="absolute bottom-full left-1/2 -translate-x-1/2 mb-1 px-2 py-1 bg-gray-800 text-white text-[10px] rounded whitespace-nowrap opacity-0 group-hover:opacity-100 transition-opacity pointer-events-none z-10">
                        {c.name}
                      </div>
                    </div>
                  ))}
                </div>
              </div>
            </div>

            {/* Sections */}
            {content.sections.map((section, i) => (
              <ReportSectionBlock key={i} section={section} />
            ))}
          </div>
        ) : (
          <AIReviewPane report={report} />
        )}
      </div>
    </div>
  );
};
