/**
 * state.js — Application state management (simple reactive store).
 */

const State = (() => {
  let _reports = JSON.parse(JSON.stringify(window.MOCK_REPORTS)); // deep copy
  let _selectedReportId = null;
  let _currentView = 'dashboard';
  let _settings = {
    reviewerName: 'Senior Reviewer',
    reviewerRole: 'Editorial Lead',
    aiThreshold: 80,
  };
  const _listeners = {};

  function on(event, fn) {
    if (!_listeners[event]) _listeners[event] = [];
    _listeners[event].push(fn);
  }

  function emit(event, payload) {
    (_listeners[event] || []).forEach(fn => fn(payload));
  }

  function getReports() { return _reports; }

  function getReport(id) { return _reports.find(r => r.id === id) || null; }

  function getSelectedReport() {
    return _selectedReportId ? getReport(_selectedReportId) : null;
  }

  function setSelectedReport(id) {
    _selectedReportId = id;
    emit('reportSelected', getReport(id));
  }

  function getCurrentView() { return _currentView; }

  function setView(view) {
    _currentView = view;
    emit('viewChanged', view);
  }

  function updateReportStatus(id, newStatus) {
    const r = getReport(id);
    if (!r) return;
    r.status = newStatus;
    r.lastUpdated = new Date().toISOString();
    emit('reportUpdated', r);
    emit('statsChanged');
  }

  function updateHumanStatus(id, humanStatus) {
    const r = getReport(id);
    if (!r) return;
    r.humanStatus = humanStatus;
    r.lastUpdated = new Date().toISOString();
    emit('reportUpdated', r);
  }

  function addComment(reportId, comment) {
    const r = getReport(reportId);
    if (!r) return;
    r.comments.push(comment);
    r.commentCount = r.comments.length;
    emit('commentsUpdated', { reportId, comments: r.comments });
    emit('reportUpdated', r);
  }

  function resolveComment(reportId, commentId) {
    const r = getReport(reportId);
    if (!r) return;
    const c = r.comments.find(c => c.id === commentId);
    if (c) {
      c.status = 'resolved';
      emit('commentsUpdated', { reportId, comments: r.comments });
    }
  }

  function getSettings() { return { ..._settings }; }

  function updateSettings(s) {
    _settings = { ..._settings, ...s };
    emit('settingsUpdated', _settings);
  }

  function getStats() {
    const reports = _reports;
    return {
      total: reports.length,
      pendingHuman: reports.filter(r => ['Needs Human Review', 'AI Reviewed'].includes(r.status)).length,
      aiApproved: reports.filter(r => r.aiScore >= 80 && r.aiReview).length,
      readyToPublish: reports.filter(r => r.publishReady).length,
      needsRevision: reports.filter(r => r.status === 'Needs Revision').length,
    };
  }

  return {
    on, emit,
    getReports, getReport, getSelectedReport, setSelectedReport,
    getCurrentView, setView,
    updateReportStatus, updateHumanStatus,
    addComment, resolveComment,
    getSettings, updateSettings,
    getStats,
  };
})();
