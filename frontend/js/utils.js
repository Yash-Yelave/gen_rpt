/**
 * utils.js — Utility functions
 */

/** Format an ISO timestamp to a readable relative or absolute date. */
function formatDate(isoStr) {
  if (!isoStr) return '—';
  const d = new Date(isoStr);
  const now = new Date();
  const diffMs = now - d;
  const diffMins = Math.floor(diffMs / 60000);
  const diffHours = Math.floor(diffMins / 60);
  const diffDays = Math.floor(diffHours / 24);

  if (diffMins < 1) return 'just now';
  if (diffMins < 60) return `${diffMins}m ago`;
  if (diffHours < 24) return `${diffHours}h ago`;
  if (diffDays === 1) return 'yesterday';
  if (diffDays < 7) return `${diffDays}d ago`;

  return d.toLocaleDateString('en-GB', { day: 'numeric', month: 'short', year: 'numeric' });
}

/** Return CSS class for a given status string. */
function statusClass(status) {
  const map = {
    'Generated':          'status--generated',
    'AI Reviewed':        'status--ai-reviewed',
    'Needs Human Review': 'status--needs-human-review',
    'Needs Revision':     'status--needs-revision',
    'Approved':           'status--approved',
    'Ready to Publish':   'status--ready-to-publish',
    'Published':          'status--published',
    'Rejected':           'status--rejected',
  };
  return map[status] || 'status--generated';
}

/** Return badge class for priority. */
function priorityBadgeClass(priority) {
  const map = { High: 'badge--red', Medium: 'badge--orange', Low: 'badge--gray' };
  return map[priority] || 'badge--gray';
}

/** Return badge class for comment status. */
function commentStatusBadgeClass(status) {
  const map = {
    'open':                 'badge--blue',
    'resolved':             'badge--green',
    'sent to regeneration': 'badge--orange',
  };
  return map[status] || 'badge--gray';
}

/** Escape HTML special characters. */
function escHtml(str) {
  if (!str) return '';
  return str.replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;').replace(/"/g,'&quot;');
}

/** Generate a simple unique ID. */
function uid() {
  return 'c' + Date.now().toString(36) + Math.random().toString(36).slice(2, 6);
}

/** Get score color class. */
function scoreColor(score) {
  if (score >= 88) return 'var(--green-600)';
  if (score >= 75) return 'var(--blue-600)';
  if (score >= 60) return 'var(--orange-600)';
  return 'var(--red-600)';
}

/** Debounce function */
function debounce(fn, delay = 200) {
  let timer;
  return (...args) => {
    clearTimeout(timer);
    timer = setTimeout(() => fn(...args), delay);
  };
}
