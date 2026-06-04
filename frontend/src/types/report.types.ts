// src/types/report.types.ts
import type { Comment } from './comment.types';

export enum ReportStatus {
  Generated = 'Generated',
  AIReviewed = 'AI Reviewed',
  NeedsHumanReview = 'Needs Human Review',
  NeedsRevision = 'Needs Revision',
  Approved = 'Approved',
  ReadyToPublish = 'Ready to Publish',
  Published = 'Published',
  Rejected = 'Rejected',
}

export enum AIGrade {
  Gold = 'Gold',
  Silver = 'Silver',
  Bronze = 'Bronze',
}

export interface ScoreComponents {
  research_quality: number;
  strategic_insight: number;
  source_quality: number;
  writing_quality: number;
  design_quality: number;
  executive_readiness: number;
}

export interface ReviewScores {
  overall_score: number;
  grade: AIGrade | string;
  components: ScoreComponents;
}

export interface PriorityImprovement {
  issue: string;
  impact: string;
  suggested_fix: string;
  priority_level: 'High' | 'Medium' | 'Low';
}

export interface ExecutiveReadiness {
  board_members: boolean;
  ministers: boolean;
  ceos: boolean;
  sovereign_wealth_funds: boolean;
  senior_executives: boolean;
  justification: string;
}

export interface AIRecommendations {
  strengths: string[];
  weaknesses: string[];
  priority_improvements: PriorityImprovement[];
  executive_readiness: ExecutiveReadiness;
}

export interface AIReview {
  scores: ReviewScores;
  recommendations: AIRecommendations;
  dataGaps: string[];
  writingFlaws: string[];
  strategicGaps: string[];
  gccGaps: string[];
}

export interface ReportSection {
  heading: string;
  body: string;
  isDisclaimer?: boolean;
}

export interface ReportContent {
  brand: string;
  label: string;
  date: string;
  sections: ReportSection[];
}

export interface Report {
  id: string;
  title: string;
  version: string;
  status: ReportStatus | string;
  humanStatus: string;
  aiScore: number;
  aiGrade: string;
  commentCount: number;
  lastUpdated: string;
  publishReady: boolean;
  aiReview: AIReview | null;
  reportContent: ReportContent;
  comments: Comment[];
}

export interface ReportVersion {
  version: string;
  createdAt: string;
  status: ReportStatus | string;
}
