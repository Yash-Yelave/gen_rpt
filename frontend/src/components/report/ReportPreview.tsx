// src/components/report/ReportPreview.tsx
import React from 'react';
import type { Report, ReportSection } from '@/types';
import { useUIStore } from '@/store/uiStore';


interface Props {
  report: Report;
}

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

export const ReportPreview: React.FC<Props> = ({ report }) => {
  const { zoomLevel, zoomIn, zoomOut } = useUIStore();
  const { reportContent: content, title, id, version, aiScore, aiGrade } = report;

  return (
    <div className="flex flex-col border-r border-gray-200 bg-gray-100 overflow-hidden">
      {/* Pane header */}
      <div className="flex items-center justify-between px-4 py-3 bg-white border-b border-gray-200 flex-shrink-0">
        <span className="text-xs font-semibold text-gray-700 uppercase tracking-widest">Report Preview</span>
        <div className="flex items-center gap-2">
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
      </div>

      {/* Document */}
      <div className="flex-1 overflow-y-auto p-6">
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
            <div className="flex items-center gap-4 flex-wrap">
              <span className="text-xs text-gray-400">ID: {id}</span>
              <span className="text-xs text-gray-400">{version}</span>
              <span className="text-xs text-gray-400">{content.date}</span>
            </div>
            {aiScore > 0 && (
              <div className="flex gap-3 mt-3">
                <span className="bg-blue-50 border border-blue-100 text-blue-700 text-xs font-bold px-2.5 py-1 rounded">
                  AI Score: {aiScore.toFixed(1)}
                </span>
                <span className="bg-blue-50 border border-blue-100 text-blue-700 text-xs font-bold px-2.5 py-1 rounded">
                  Grade: {aiGrade}
                </span>
              </div>
            )}
          </div>

          {/* Sections */}
          {content.sections.map((section, i) => (
            <ReportSectionBlock key={i} section={section} />
          ))}
        </div>
      </div>
    </div>
  );
};
