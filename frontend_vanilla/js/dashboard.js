/**
 * dashboard.js — Dashboard view: stats cards, reports table with search/filter.
 */

let _searchQuery = '';
let _statusFilter = '';

/* ===== RENDER DASHBOARD ===== */
function renderDashboard() {
  updateStats();
  renderReportsTable();
  updateBadges();
}

/* ===== STATS CARDS ===== */
function updateStats() {
  const stats = State.getStats();
  setStatValue('stat-total-value', stats.total);
  setStatValue('stat-pending-value', stats.pendingHuman);
  setStatValue('stat-approved-value', stats.aiApproved);
  setStatValue('stat-publish-value', stats.readyToPublish);
  setStatValue('stat-revision-value', stats.needsRevision);

  const ts = document.getElementById('dashboard-updated');
  if (ts) ts.textContent = 'Updated ' + formatDate(new Date().toISOString());
}

function setStatValue(id, val) {
  const el = document.getElementById(id);
  if (el) el.textContent = val;
}

/* ===== SIDEBAR BADGES ===== */
function updateBadges() {
  const stats = State.getStats();
  const pendingBadge = document.getElementById('badge-pending');
  const revBadge = document.getElementById('badge-revisions');
  if (pendingBadge) pendingBadge.textContent = stats.pendingHuman;
  if (revBadge) revBadge.textContent = stats.needsRevision;
}

/* ===== REPORTS TABLE ===== */
function renderReportsTable() {
  const tbody = document.getElementById('reports-tbody');
  const emptyState = document.getElementById('empty-state-reports');
  const tableWrapper = document.querySelector('.table-wrapper');
  if (!tbody) return;

  let reports = State.getReports();

  // Apply filters
  if (_searchQuery) {
    const q = _searchQuery.toLowerCase();
    reports = reports.filter(r =>
      r.title.toLowerCase().includes(q) ||
      r.id.toLowerCase().includes(q) ||
      r.status.toLowerCase().includes(q)
    );
  }

  if (_statusFilter) {
    reports = reports.filter(r => r.status === _statusFilter);
  }

  if (reports.length === 0) {
    if (tableWrapper) tableWrapper.style.display = 'none';
    if (emptyState) emptyState.style.display = '';
    return;
  }

  if (tableWrapper) tableWrapper.style.display = '';
  if (emptyState) emptyState.style.display = 'none';

  tbody.innerHTML = reports.map(r => `
    <tr>
      <td>
        <div class="table-report-title">${escHtml(r.title)}</div>
        <div class="table-report-id">${escHtml(r.id)} · ${escHtml(r.version)}</div>
      </td>
      <td><span class="table-report-id">${escHtml(r.id)}</span></td>
      <td>
        ${r.aiScore > 0
          ? `<span class="ai-score-cell">${r.aiScore.toFixed(1)}</span> <span class="badge badge--gray" style="margin-left:4px;">${escHtml(r.aiGrade)}</span>`
          : '<span style="color:var(--gray-300);">—</span>'}
      </td>
      <td><span class="status-badge ${statusClass(r.status)}">${escHtml(r.status)}</span></td>
      <td>
        <span class="badge ${humanStatusBadge(r.humanStatus)}">${escHtml(r.humanStatus)}</span>
      </td>
      <td>
        ${r.commentCount > 0
          ? `<span class="badge badge--gray">${r.commentCount}</span>`
          : '<span style="color:var(--gray-300);">—</span>'}
      </td>
      <td style="color:var(--gray-400); font-size:var(--font-xs);">${formatDate(r.lastUpdated)}</td>
      <td>
        <button class="btn btn--primary btn--xs" data-report-id="${escHtml(r.id)}" aria-label="Open review for ${escHtml(r.title)}">
          Open
        </button>
      </td>
    </tr>
  `).join('');

  // Bind open buttons
  tbody.querySelectorAll('button[data-report-id]').forEach(btn => {
    btn.addEventListener('click', () => {
      const id = btn.dataset.reportId;
      openReportReview(id);
    });
  });
}

function humanStatusBadge(status) {
  const map = {
    'Not Started': 'badge--gray',
    'Pending':     'badge--blue',
    'In Progress': 'badge--orange',
    'Approved':    'badge--green',
    'Needs Revision': 'badge--orange',
    'Rejected':    'badge--red',
  };
  return map[status] || 'badge--gray';
}

/* ===== SEARCH + FILTER INIT ===== */
function initDashboardFilters() {
  const searchEl = document.getElementById('report-search');
  const filterEl = document.getElementById('filter-status');

  if (searchEl) {
    searchEl.addEventListener('input', debounce(() => {
      _searchQuery = searchEl.value.trim();
      renderReportsTable();
    }, 200));
  }

  if (filterEl) {
    filterEl.addEventListener('change', () => {
      _statusFilter = filterEl.value;
      renderReportsTable();
    });
  }
}
