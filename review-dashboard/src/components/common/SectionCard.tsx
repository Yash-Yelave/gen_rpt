// src/components/common/SectionCard.tsx
import React, { useState } from 'react';
import { ChevronDown } from 'lucide-react';

interface Props {
  title: string;
  icon?: React.ReactNode;
  rightContent?: React.ReactNode;
  children: React.ReactNode;
  defaultOpen?: boolean;
  className?: string;
}

export const SectionCard: React.FC<Props> = ({
  title,
  icon,
  rightContent,
  children,
  defaultOpen = true,
  className = '',
}) => {
  const [open, setOpen] = useState(defaultOpen);

  return (
    <div className={`border-b border-gray-200 ${className}`}>
      <button
        className="flex items-center justify-between w-full px-4 py-3 bg-white hover:bg-gray-50 transition-colors cursor-pointer"
        onClick={() => setOpen(!open)}
        aria-expanded={open}
      >
        <div className="flex items-center gap-2">
          {icon && <span className="text-blue-600 flex-shrink-0 w-4 h-4">{icon}</span>}
          <span className="text-sm font-semibold text-gray-800">{title}</span>
        </div>
        <div className="flex items-center gap-2">
          {rightContent}
          <ChevronDown
            className={`w-3.5 h-3.5 text-gray-400 transition-transform duration-150 ${open ? '' : '-rotate-90'}`}
          />
        </div>
      </button>
      {open && <div className="panel-card-body">{children}</div>}
    </div>
  );
};
