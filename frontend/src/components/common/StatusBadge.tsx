// src/components/common/StatusBadge.tsx
import React from 'react';
import { statusBadgeClasses } from '@/utils/statusHelpers';

interface Props {
  status: string;
  className?: string;
}

export const StatusBadge = React.memo(({ status, className = '' }: Props) => (
  <span
    className={`inline-flex items-center px-2 py-0.5 rounded-full text-xs font-semibold whitespace-nowrap ${statusBadgeClasses(status)} ${className}`}
  >
    {status}
  </span>
));
StatusBadge.displayName = 'StatusBadge';
