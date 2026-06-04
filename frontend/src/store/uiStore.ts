// src/store/uiStore.ts
import { create } from 'zustand';

interface ToastMessage {
  id: string;
  message: string;
  type: 'success' | 'error' | 'info' | '';
}

interface UIState {
  sidebarCollapsed: boolean;
  zoomLevel: number;
  toasts: ToastMessage[];
  searchQuery: string;
  statusFilter: string;
  setSidebarCollapsed: (v: boolean) => void;
  toggleSidebar: () => void;
  setZoomLevel: (level: number) => void;
  zoomIn: () => void;
  zoomOut: () => void;
  showToast: (message: string, type?: ToastMessage['type']) => void;
  dismissToast: (id: string) => void;
  setSearchQuery: (q: string) => void;
  setStatusFilter: (s: string) => void;
}

export const useUIStore = create<UIState>((set) => ({
  sidebarCollapsed: false,
  zoomLevel: 100,
  toasts: [],
  searchQuery: '',
  statusFilter: '',

  setSidebarCollapsed: (v) => set({ sidebarCollapsed: v }),
  toggleSidebar: () => set((s) => ({ sidebarCollapsed: !s.sidebarCollapsed })),

  setZoomLevel: (level) => set({ zoomLevel: Math.max(70, Math.min(150, level)) }),
  zoomIn: () => set((s) => ({ zoomLevel: Math.min(150, s.zoomLevel + 10) })),
  zoomOut: () => set((s) => ({ zoomLevel: Math.max(70, s.zoomLevel - 10) })),

  showToast: (message, type = '') => {
    const id = Date.now().toString();
    set((s) => ({ toasts: [...s.toasts, { id, message, type }] }));
    setTimeout(() => {
      set((s) => ({ toasts: s.toasts.filter((t) => t.id !== id) }));
    }, 3000);
  },

  dismissToast: (id) => set((s) => ({ toasts: s.toasts.filter((t) => t.id !== id) })),

  setSearchQuery: (q) => set({ searchQuery: q }),
  setStatusFilter: (s) => set({ statusFilter: s }),
}));
