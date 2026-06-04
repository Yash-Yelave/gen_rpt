// src/store/reviewStore.ts
import { create } from 'zustand';

interface ReviewState {
  decision: string;
  commentText: string;
  commentSection: string;
  commentPriority: string;
  setDecision: (d: string) => void;
  setCommentText: (t: string) => void;
  setCommentSection: (s: string) => void;
  setCommentPriority: (p: string) => void;
  reset: () => void;
}

export const useReviewStore = create<ReviewState>((set) => ({
  decision: '',
  commentText: '',
  commentSection: 'Any Section',
  commentPriority: 'Medium',

  setDecision: (decision) => set({ decision }),
  setCommentText: (commentText) => set({ commentText }),
  setCommentSection: (commentSection) => set({ commentSection }),
  setCommentPriority: (commentPriority) => set({ commentPriority }),
  reset: () =>
    set({ decision: '', commentText: '', commentSection: 'Any Section', commentPriority: 'Medium' }),
}));
