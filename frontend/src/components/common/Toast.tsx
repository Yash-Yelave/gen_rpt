// src/components/common/Toast.tsx
import React from 'react';
import { useUIStore } from '@/store/uiStore';
import { X } from 'lucide-react';

export const ToastContainer: React.FC = () => {
  const { toasts, dismissToast } = useUIStore();

  return (
    <div className="fixed bottom-5 right-5 z-50 flex flex-col gap-2 pointer-events-none">
      {toasts.map((t) => {
        const bg =
          t.type === 'success'
            ? 'bg-green-700'
            : t.type === 'error'
            ? 'bg-red-700'
            : t.type === 'info'
            ? 'bg-blue-700'
            : 'bg-gray-900';
        return (
          <div
            key={t.id}
            className={`flex items-center gap-3 ${bg} text-white text-sm font-medium px-4 py-2.5 rounded shadow-md pointer-events-auto max-w-xs animate-in fade-in slide-in-from-bottom-2`}
          >
            <span className="flex-1">{t.message}</span>
            <button
              onClick={() => dismissToast(t.id)}
              className="text-white/70 hover:text-white flex-shrink-0"
              aria-label="Dismiss"
            >
              <X className="w-3.5 h-3.5" />
            </button>
          </div>
        );
      })}
    </div>
  );
};
