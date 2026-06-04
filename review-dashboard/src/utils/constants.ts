// src/utils/constants.ts

export const REPORT_SECTIONS = [
  'Any Section',
  'Executive Summary',
  'Charts',
  'Recommendations',
  'Key Highlights',
  'Methodology',
  'Conclusion',
  'Hardware Landscape',
  'Government Funding & Policy',
  'Strategic Risks',
  'Competitive Position',
];

export const COMMENT_PRIORITIES = ['Low', 'Medium', 'High'] as const;

export const HUMAN_DECISIONS = ['Approved', 'Needs Revision', 'Rejected'] as const;

export const REPORT_STATUSES = [
  'Generated',
  'AI Reviewed',
  'Needs Human Review',
  'Needs Revision',
  'Approved',
  'Ready to Publish',
  'Published',
  'Rejected',
] as const;

export const QUERY_KEYS = {
  reports: ['reports'] as const,
  report: (id: string) => ['reports', id] as const,
  metrics: ['metrics'] as const,
  comments: (reportId: string) => ['comments', reportId] as const,
};
