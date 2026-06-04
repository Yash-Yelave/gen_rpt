// src/types/review.types.ts

export enum HumanDecision {
  Approved = 'Approved',
  NeedsRevision = 'Needs Revision',
  Rejected = 'Rejected',
}

export interface HumanReview {
  reportId: string;
  decision: HumanDecision | string | null;
  notes: string;
  reviewerName: string;
  reviewedAt: string | null;
}
