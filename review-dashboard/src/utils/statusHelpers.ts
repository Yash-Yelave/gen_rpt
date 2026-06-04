// src/utils/statusHelpers.ts

export function statusBadgeClasses(status: string): string {
  const map: Record<string, string> = {
    'Generated':            'bg-gray-100 text-gray-600',
    'AI Reviewed':          'bg-blue-50 text-blue-700 border border-blue-100',
    'Needs Human Review':   'bg-orange-100 text-orange-700',
    'Needs Revision':       'bg-orange-100 text-orange-700',
    'Approved':             'bg-green-100 text-green-700',
    'Ready to Publish':     'bg-green-100 text-green-700',
    'Published':            'bg-green-700 text-white',
    'Rejected':             'bg-red-100 text-red-700',
  };
  return map[status] ?? 'bg-gray-100 text-gray-600';
}

export function humanStatusBadgeClasses(status: string): string {
  const map: Record<string, string> = {
    'Not Started':    'bg-gray-100 text-gray-600',
    'Pending':        'bg-blue-100 text-blue-700',
    'In Progress':    'bg-orange-100 text-orange-700',
    'Approved':       'bg-green-100 text-green-700',
    'Needs Revision': 'bg-orange-100 text-orange-700',
    'Rejected':       'bg-red-100 text-red-700',
  };
  return map[status] ?? 'bg-gray-100 text-gray-600';
}

export function priorityBadgeClasses(priority: string): string {
  const map: Record<string, string> = {
    High:   'bg-red-100 text-red-700',
    Medium: 'bg-orange-100 text-orange-700',
    Low:    'bg-gray-100 text-gray-600',
  };
  return map[priority] ?? 'bg-gray-100 text-gray-600';
}

export function commentStatusBadgeClasses(status: string): string {
  const map: Record<string, string> = {
    'open':                  'bg-blue-100 text-blue-700',
    'resolved':              'bg-green-100 text-green-700',
    'sent to regeneration':  'bg-orange-100 text-orange-700',
  };
  return map[status] ?? 'bg-gray-100 text-gray-600';
}

export function scoreColor(score: number): string {
  if (score >= 88) return '#059669'; // green-600
  if (score >= 75) return '#2563EB'; // blue-600
  if (score >= 60) return '#D97706'; // orange-600
  return '#DC2626'; // red-600
}

export function commentBorderClass(status: string): string {
  if (status === 'resolved') return 'comment-resolved';
  if (status === 'sent to regeneration') return 'comment-sent';
  return 'comment-open';
}
