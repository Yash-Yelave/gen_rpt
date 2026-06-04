// src/types/comment.types.ts

export enum CommentStatus {
  Open = 'open',
  Resolved = 'resolved',
  SentToRegeneration = 'sent to regeneration',
}

export enum CommentPriority {
  High = 'High',
  Medium = 'Medium',
  Low = 'Low',
}

export interface Comment {
  id: string;
  reportId: string;
  version: string;
  section: string;
  text: string;
  priority: CommentPriority | string;
  reviewer: string;
  timestamp: string;
  status: CommentStatus | string;
}
