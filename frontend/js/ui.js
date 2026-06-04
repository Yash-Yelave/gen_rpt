/**
 * ui.js — Generic UI utilities: toast, navigation, collapsibles.
 */

/* ===== TOAST ===== */
const Toast = (() => {
  const el = document.getElementById('toast');
  let timer = null;

  function show(message, type = '', duration = 3000) {
    if (!el) return;
    el.textContent = message;
    el.className = `toast toast--show${type ? ' toast--' + type : ''}`;
    clearTimeout(timer);
    timer = setTimeout(() => {
      el.classList.remove('toast--show');
    }, duration);
  }

  return { show };
})();


/* ===== NAVIGATION ===== */
function initNavigation() {
  document.querySelectorAll('.sidebar__nav-item[data-view]').forEach(link => {
    link.addEventListener('click', (e) => {
      e.preventDefault();
      const view = link.dataset.view;
      State.setView(view);
    });
  });

  State.on('viewChanged', (view) => {
    // Update active nav item
    document.querySelectorAll('.sidebar__nav-item[data-view]').forEach(l => {
      l.classList.toggle('active', l.dataset.view === view);
    });
    // Show/hide views
    document.querySelectorAll('.view').forEach(v => {
      v.style.display = 'none';
    });
    const el = document.getElementById('view-' + view);
    if (el) el.style.display = '';

    // Render specific view
    if (view === 'dashboard') renderDashboard();
    if (view === 'pending') renderFilteredGrid('pending', ['Needs Human Review', 'AI Reviewed']);
    if (view === 'reviewed') renderFilteredGrid('reviewed', ['Approved', 'Ready to Publish']);
    if (view === 'published') renderFilteredGrid('published', ['Published']);
    if (view === 'revisions') renderFilteredGrid('revisions', ['Needs Revision']);
    if (view === 'settings') renderSettings();
  });
}


/* ===== COLLAPSIBLE PANEL CARDS ===== */
function initCollapsibles() {
  const pairs = [
    ['ai-review-toggle', 'ai-review-body', 'ai-chevron'],
    ['human-review-toggle', 'human-review-body', 'human-chevron'],
    ['comments-toggle', 'comments-body', 'comments-chevron'],
  ];

  pairs.forEach(([toggleId, bodyId, chevronId]) => {
    const toggle = document.getElementById(toggleId);
    const body = document.getElementById(bodyId);
    const chevron = document.getElementById(chevronId);
    if (!toggle || !body) return;

    toggle.addEventListener('click', () => {
      const isExpanded = toggle.getAttribute('aria-expanded') === 'true';
      toggle.setAttribute('aria-expanded', String(!isExpanded));
      body.classList.toggle('collapsed', isExpanded);
      if (chevron) chevron.classList.toggle('rotated', isExpanded);
    });
  });
}


/* ===== RENDER FILTERED REPORT GRID ===== */
function renderFilteredGrid(viewId, statuses) {
  const grid = document.getElementById(viewId + '-grid');
  const emptyState = document.getElementById('empty-state-' + viewId);
  if (!grid) return;

  const reports = State.getReports().filter(r => statuses.includes(r.status));
  grid.innerHTML = '';

  if (reports.length === 0) {
    grid.style.display = 'none';
    if (emptyState) emptyState.style.display = '';
    return;
  }

  grid.style.display = '';
  if (emptyState) emptyState.style.display = 'none';

  reports.forEach(r => {
    const card = document.createElement('div');
    card.className = 'report-card';
    card.setAttribute('role', 'button');
    card.setAttribute('tabindex', '0');
    card.setAttribute('aria-label', `Open report: ${r.title}`);
    card.innerHTML = `
      <div class="report-card__header">
        <div>
          <div class="report-card__title">${escHtml(r.title)}</div>
          <div class="report-card__id">${escHtml(r.id)} · ${escHtml(r.version)}</div>
        </div>
        <span class="status-badge ${statusClass(r.status)}">${escHtml(r.status)}</span>
      </div>
      <div style="display:flex; gap:8px; flex-wrap:wrap; margin-top:8px;">
        ${r.aiScore > 0 ? `<span class="score-chip">AI ${r.aiScore.toFixed(1)}</span>` : ''}
        ${r.commentCount > 0 ? `<span class="badge badge--gray">${r.commentCount} comment${r.commentCount > 1 ? 's' : ''}</span>` : ''}
      </div>
      <div class="report-card__meta">
        <span class="report-card__score">${r.aiScore > 0 ? r.aiGrade : 'Not scored'}</span>
        <span class="report-card__date">${formatDate(r.lastUpdated)}</span>
      </div>
    `;
    card.addEventListener('click', () => openReportReview(r.id));
    card.addEventListener('keydown', (e) => { if (e.key === 'Enter' || e.key === ' ') openReportReview(r.id); });
    grid.appendChild(card);
  });
}


/* ===== SETTINGS VIEW ===== */
function renderSettings() {
  const s = State.getSettings();
  const nameEl = document.getElementById('setting-name');
  const roleEl = document.getElementById('setting-role');
  const threshEl = document.getElementById('setting-threshold');
  if (nameEl) nameEl.value = s.reviewerName;
  if (roleEl) roleEl.value = s.reviewerRole;
  if (threshEl) threshEl.value = s.aiThreshold;
}

function initSettingsSave() {
  const btn = document.getElementById('btn-save-settings');
  if (!btn) return;
  btn.addEventListener('click', () => {
    const name = document.getElementById('setting-name')?.value?.trim() || 'Reviewer';
    const role = document.getElementById('setting-role')?.value?.trim() || '';
    const threshold = parseInt(document.getElementById('setting-threshold')?.value || '80', 10);
    State.updateSettings({ reviewerName: name, reviewerRole: role, aiThreshold: threshold });

    // Update sidebar user info
    document.querySelector('.sidebar__user-name').textContent = name;
    document.querySelector('.sidebar__user-role').textContent = role;
    document.querySelector('.sidebar__user-avatar').textContent = name.split(' ').map(w => w[0]).join('').slice(0,2).toUpperCase();

    Toast.show('Settings saved', 'success');
  });
}


/* ===== ZOOM CONTROLS ===== */
function initZoomControls() {
  let zoomLevel = 100;
  const doc = document.getElementById('report-document');
  const label = document.getElementById('zoom-label');

  document.getElementById('btn-zoom-in')?.addEventListener('click', () => {
    zoomLevel = Math.min(150, zoomLevel + 10);
    applyZoom();
  });

  document.getElementById('btn-zoom-out')?.addEventListener('click', () => {
    zoomLevel = Math.max(70, zoomLevel - 10);
    applyZoom();
  });

  function applyZoom() {
    if (doc) doc.style.fontSize = (zoomLevel / 100) + 'rem';
    if (label) label.textContent = zoomLevel + '%';
  }
}


/* ===== OPEN REPORT FOR REVIEW ===== */
function openReportReview(id) {
  State.setSelectedReport(id);
  State.setView('review');
}
