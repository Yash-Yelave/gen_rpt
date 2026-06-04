// src/components/common/EmptyState.tsx
import React from 'react';
import { FileText } from 'lucide-react';

interface Props {
  icon?: React.ReactNode;
  title: string;
  text?: string;
  small?: boolean;
}

export const EmptyState = React.memo(({ icon, title, text, small = false }: Props) => (
  <div className={`flex flex-col items-center justify-center text-center ${small ? 'py-6 px-4' : 'py-10 px-6'}`}>
    <div className={`text-gray-300 mb-3 ${small ? 'w-8 h-8' : 'w-12 h-12'}`}>
      {icon ?? <FileText className="w-full h-full" />}
    </div>
    <div className="text-sm font-semibold text-gray-500 mb-1">{title}</div>
    {text && <div className="text-xs text-gray-400 max-w-xs">{text}</div>}
  </div>
));
EmptyState.displayName = 'EmptyState';
