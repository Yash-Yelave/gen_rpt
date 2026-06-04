// src/store/authStore.ts
import { create } from 'zustand';
import { persist } from 'zustand/middleware';

interface AuthState {
  reviewerName: string;
  reviewerRole: string;
  aiThreshold: number;
  setReviewerName: (name: string) => void;
  setReviewerRole: (role: string) => void;
  setAiThreshold: (threshold: number) => void;
  getAvatarInitials: () => string;
}

export const useAuthStore = create<AuthState>()(
  persist(
    (set, get) => ({
      reviewerName: 'Senior Reviewer',
      reviewerRole: 'Editorial Lead',
      aiThreshold: 80,

      setReviewerName: (name) => set({ reviewerName: name }),
      setReviewerRole: (role) => set({ reviewerRole: role }),
      setAiThreshold: (threshold) => set({ aiThreshold: threshold }),

      getAvatarInitials: () => {
        const name = get().reviewerName;
        return name
          .split(' ')
          .map((w) => w[0])
          .join('')
          .slice(0, 2)
          .toUpperCase();
      },
    }),
    { name: 'blueocean-auth' }
  )
);
