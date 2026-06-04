/**
 * app.js — Entry point. Initializes all modules and renders the initial view.
 */

document.addEventListener('DOMContentLoaded', () => {
  // Initialize navigation
  initNavigation();

  // Initialize collapsible cards
  initCollapsibles();

  // Initialize zoom controls
  initZoomControls();

  // Initialize radio group visuals
  initRadioGroupVisuals();

  // Initialize comment submission
  initCommentSubmit();

  // Initialize action buttons
  initActionButtons();

  // Initialize settings save
  initSettingsSave();

  // Initialize dashboard filters
  initDashboardFilters();

  // Initialize review state listeners
  initReviewStateListeners();

  // Subscribe to stats changes
  State.on('statsChanged', () => {
    if (State.getCurrentView() === 'dashboard') {
      updateStats();
    }
    updateBadges();
  });

  State.on('reportUpdated', () => {
    if (State.getCurrentView() === 'dashboard') {
      renderReportsTable();
      updateStats();
    }
    updateBadges();
  });

  // Initial render
  renderDashboard();
  updateBadges();

  // Apply saved settings to sidebar
  const s = State.getSettings();
  const nameEl = document.querySelector('.sidebar__user-name');
  const roleEl = document.querySelector('.sidebar__user-role');
  const avatarEl = document.querySelector('.sidebar__user-avatar');
  if (nameEl) nameEl.textContent = s.reviewerName;
  if (roleEl) roleEl.textContent = s.reviewerRole;
  if (avatarEl) avatarEl.textContent = s.reviewerName.split(' ').map(w => w[0]).join('').slice(0, 2).toUpperCase();

  console.log('[BlueOcean Review Dashboard] Initialized successfully.');
});
