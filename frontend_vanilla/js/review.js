/**
 * review.js — Report Review view: renders report document, AI review panel,
 * human review controls, comments thread, and action button logic.
 */

/* ===== REPORT DOCUMENT RENDERER ===== */
function renderReportDocument(report) {
  const docEl = document.getElementById('report-document');
  const emptyEl = document.getElementById('empty-state-preview');
  if (!docEl) return;

  if (!report || !report.reportContent) {
    if (emptyEl) emptyEl.style.display = '';
    return;
  }
  if (emptyEl) emptyEl.style.display = 'none';

  const { brand, label, date, sections } = report.reportContent;

  let html = `
    <div class="report-doc-header">
      <div class="report-doc-brand">${escHtml(brand)} · ${escHtml(label)}</div>
      <div class="report-doc-title">${escHtml(report.title)}</div>
      <div class="report-doc-meta-row">
        <span class="report-doc-meta-item">ID: ${escHtml(report.id)}</span>
        <span class="report-doc-meta-item">${escHtml(report.version)}</span>
        <span class="report-doc-meta-item">${escHtml(date)}</span>
      </div>
      ${report.aiScore > 0 ? `<div class="report-doc-score-row">
        <span class="report-doc-score-chip">AI Score: ${report.aiScore.toFixed(1)}</span>
        <span class="report-doc-score-chip">Grade: ${escHtml(report.aiGrade)}</span>
      </div>` : ''}
    </div>
  `;

  sections.forEach(section => {
    if (section.isDisclaimer) {
      html += `<div class="report-disclaimer"><strong>Disclaimer:</strong> ${escHtml(section.body)}</div>`;
    } else {
      const bodyHtml = section.body
        .split('\n\n')
        .map(para => para.trim())
        .filter(Boolean)
        .map(para => {
          if (para.startsWith('- ') || para.match(/^\d+\./)) {
            const items = para.split('\n').filter(Boolean);
            const lis = items.map(item => `<li>${escHtml(item.replace(/^[-\d.]+\s*/, ''))}</li>`).join('');
            return `<ul>${lis}</ul>`;
          }
          return `<p>${escHtml(para)}</p>`;
        })
        .join('');

      html += `
        <div class="report-section">
          <div class="report-section-heading">${escHtml(section.heading)}</div>
          <div class="report-section-body">${bodyHtml}</div>
        </div>
      `;
    }
  });

  docEl.innerHTML = html;
}


/* ===== AI REVIEW PANEL RENDERER ===== */
function renderAIReviewPanel(report) {
  const emptyEl = document.getElementById('empty-state-ai');
  const contentEl = document.getElementById('ai-review-content');
  const scoreNumEl = document.getElementById('ai-score-number');
  const gradeEl = document.getElementById('ai-grade-badge');

  if (!report.aiReview) {
    if (emptyEl) emptyEl.style.display = '';
    if (contentEl) contentEl.style.display = 'none';
    if (scoreNumEl) scoreNumEl.textContent = '—';
    if (gradeEl) gradeEl.textContent = '—';
    return;
  }

  if (emptyEl) emptyEl.style.display = 'none';
  if (contentEl) contentEl.style.display = '';

  const { scores, recommendations, dataGaps, writingFlaws, strategicGaps, gccGaps } = report.aiReview;

  // Score in header
  if (scoreNumEl) scoreNumEl.textContent = scores.overall_score.toFixed(1);
  if (gradeEl) gradeEl.textContent = scores.grade;

  // Score Grid
  const scoreGrid = document.getElementById('score-grid');
  if (scoreGrid) {
    const comps = scores.components;
    scoreGrid.innerHTML = Object.entries(comps).map(([key, val]) => `
      <div class="score-item">
        <span class="score-item__label">${formatScoreKey(key)}</span>
        <span class="score-item__value" style="color:${scoreColor(val)}">${val}</span>
      </div>
    `).join('');
  }

  // Strengths
  const strengthsEl = document.getElementById('ai-strengths');
  if (strengthsEl) {
    if (recommendations.strengths.length) {
      strengthsEl.innerHTML = recommendations.strengths.map(s => `<li class="strength">${escHtml(s)}</li>`).join('');
      document.getElementById('ai-strengths-section').style.display = '';
    } else {
      document.getElementById('ai-strengths-section').style.display = 'none';
    }
  }

  // Weaknesses
  const weaknessesEl = document.getElementById('ai-weaknesses');
  if (weaknessesEl) {
    if (recommendations.weaknesses.length) {
      weaknessesEl.innerHTML = recommendations.weaknesses.map(w => `<li class="weakness">${escHtml(w)}</li>`).join('');
      document.getElementById('ai-weaknesses-section').style.display = '';
    } else {
      document.getElementById('ai-weaknesses-section').style.display = 'none';
    }
  }

  // Priority Improvements
  const improvementsEl = document.getElementById('ai-improvements');
  if (improvementsEl) {
    if (recommendations.priority_improvements.length) {
      improvementsEl.innerHTML = recommendations.priority_improvements.map(imp => `
        <div class="improvement-item">
          <div class="improvement-item__header">
            <span class="improvement-item__issue">${escHtml(imp.issue)}</span>
            <span class="badge ${priorityBadgeClass(imp.priority_level)}">${escHtml(imp.priority_level)}</span>
          </div>
          <div class="improvement-item__fix">${escHtml(imp.suggested_fix)}</div>
        </div>
      `).join('');
      document.getElementById('ai-improvements-section').style.display = '';
    } else {
      document.getElementById('ai-improvements-section').style.display = 'none';
    }
  }

  // Executive Readiness
  const execGrid = document.getElementById('exec-readiness-grid');
  if (execGrid && recommendations.executive_readiness) {
    const er = recommendations.executive_readiness;
    const items = [
      { label: 'Board Members', key: 'board_members' },
      { label: 'Ministers', key: 'ministers' },
      { label: 'CEOs', key: 'ceos' },
      { label: 'SWF', key: 'sovereign_wealth_funds' },
      { label: 'Senior Exec', key: 'senior_executives' },
    ];
    execGrid.innerHTML = items.map(item => `
      <span class="exec-readiness-chip ${er[item.key] ? 'exec-readiness-chip--yes' : 'exec-readiness-chip--no'}">
        ${er[item.key] ? '✓' : '×'} ${item.label}
      </span>
    `).join('');
  }
}

function formatScoreKey(key) {
  return key.replace(/_/g, ' ').replace(/\b\w/g, c => c.toUpperCase());
}


/* ===== COMMENTS THREAD RENDERER ===== */
function renderComments(report) {
  const threadEl = document.getElementById('comments-thread');
  const emptyEl = document.getElementById('empty-state-comments');
  const countBadge = document.getElementById('comment-count-badge');

  const comments = (report && report.comments) ? report.comments : [];

  if (countBadge) countBadge.textContent = comments.length;

  if (!comments.length) {
    if (emptyEl) emptyEl.style.display = '';
    if (threadEl) threadEl.style.display = 'none';
    return;
  }

  if (emptyEl) emptyEl.style.display = 'none';
  if (threadEl) {
    threadEl.style.display = '';
    threadEl.innerHTML = comments.map(c => `
      <div class="comment-item comment--${c.status === 'open' ? 'open' : c.status === 'resolved' ? 'resolved' : 'sent'}" id="comment-${escHtml(c.id)}">
        <div class="comment-item__header">
          <div class="comment-item__meta">
            <span class="comment-item__author">${escHtml(c.reviewer)}</span>
            <span class="comment-item__section">${escHtml(c.section)}</span>
            <span class="badge ${priorityBadgeClass(c.priority)}">${escHtml(c.priority)}</span>
            <span class="badge ${commentStatusBadgeClass(c.status)}">${escHtml(c.status)}</span>
          </div>
          <span class="comment-item__time">${formatDate(c.timestamp)}</span>
        </div>
        <div class="comment-item__text">${escHtml(c.text)}</div>
        <div class="comment-item__footer">
          <div class="comment-item__actions">
            ${c.status !== 'resolved' ? `<button class="btn-resolve" data-comment-id="${escHtml(c.id)}" data-report-id="${escHtml(c.reportId)}">Mark Resolved</button>` : '<span style="font-size:11px;color:var(--green-700);">✓ Resolved</span>'}
          </div>
        </div>
      </div>
    `).join('');

    // Bind resolve buttons
    threadEl.querySelectorAll('.btn-resolve').forEach(btn => {
      btn.addEventListener('click', () => {
        const commentId = btn.dataset.commentId;
        const reportId = btn.dataset.reportId;
        State.resolveComment(reportId, commentId);
        const report = State.getSelectedReport();
        renderComments(report);
        Toast.show('Comment marked as resolved', 'success');
      });
    });
  }
}


/* ===== REVIEW TOPBAR RENDERER ===== */
function renderReviewTopbar(report) {
  const titleEl = document.getElementById('review-report-title');
  const idEl = document.getElementById('review-report-id');
  const versionEl = document.getElementById('review-report-version');
  const statusBadge = document.getElementById('review-status-badge');
  const scoreEl = document.getElementById('review-ai-score');

  if (!report) return;
  if (titleEl) titleEl.textContent = report.title;
  if (idEl) idEl.textContent = 'ID: ' + report.id;
  if (versionEl) versionEl.textContent = report.version;
  if (statusBadge) {
    statusBadge.textContent = report.status;
    statusBadge.className = `status-badge ${statusClass(report.status)}`;
  }
  if (scoreEl) scoreEl.textContent = report.aiScore > 0 ? `AI ${report.aiScore.toFixed(1)}` : 'Not scored';
}


/* ===== RADIO GROUP SELECTION ===== */
function initRadioGroupVisuals() {
  document.querySelectorAll('.radio-option').forEach(opt => {
    const input = opt.querySelector('input[type="radio"]');
    if (!input) return;
    opt.addEventListener('click', () => {
      // Deselect all in group
      document.querySelectorAll('.radio-option').forEach(o => {
        o.classList.remove('selected--approved', 'selected--revision', 'selected--rejected');
      });
      const val = input.value;
      if (val === 'Approved') opt.classList.add('selected--approved');
      if (val === 'Needs Revision') opt.classList.add('selected--revision');
      if (val === 'Rejected') opt.classList.add('selected--rejected');
      input.checked = true;
    });
  });
}


/* ===== COMMENT SUBMISSION ===== */
function initCommentSubmit() {
  const btn = document.getElementById('btn-submit-comment');
  if (!btn) return;

  btn.addEventListener('click', () => {
    const report = State.getSelectedReport();
    if (!report) return;

    const text = document.getElementById('comment-text')?.value?.trim();
    if (!text) {
      Toast.show('Please enter a comment before submitting.', 'error');
      return;
    }

    const section = document.getElementById('comment-section-select')?.value || 'Any Section';
    const priority = document.getElementById('comment-priority')?.value || 'Medium';
    const settings = State.getSettings();

    const comment = {
      id: uid(),
      reportId: report.id,
      version: report.version,
      section,
      text,
      priority,
      reviewer: settings.reviewerName,
      timestamp: new Date().toISOString(),
      status: 'open',
    };

    State.addComment(report.id, comment);
    renderComments(State.getSelectedReport());

    // Clear form
    document.getElementById('comment-text').value = '';

    // Update comment count badge in sidebar
    updateBadges();

    Toast.show('Comment added to review thread', 'success');
  });
}


/* ===== ACTION BUTTONS ===== */
function initActionButtons() {
  document.getElementById('btn-back-to-list')?.addEventListener('click', () => {
    State.setView('dashboard');
  });

  document.getElementById('btn-save-review')?.addEventListener('click', () => {
    const report = State.getSelectedReport();
    if (!report) return;
    const decision = document.querySelector('input[name="human-decision"]:checked')?.value;
    if (decision) {
      State.updateHumanStatus(report.id, decision);
    }
    Toast.show('Review saved successfully', 'success');
    renderReviewTopbar(State.getSelectedReport());
    renderDashboard();
  });

  document.getElementById('btn-mark-done')?.addEventListener('click', () => {
    const report = State.getSelectedReport();
    if (!report) return;
    State.updateReportStatus(report.id, 'Approved');
    State.updateHumanStatus(report.id, 'Approved');
    report.publishReady = false;
    renderReviewTopbar(State.getSelectedReport());
    updateBadges();
    Toast.show('Report marked as done (Approved)', 'success');
  });

  document.getElementById('btn-send-publish')?.addEventListener('click', () => {
    const report = State.getSelectedReport();
    if (!report) return;
    State.updateReportStatus(report.id, 'Ready to Publish');
    State.updateHumanStatus(report.id, 'Approved');
    report.publishReady = true;
    renderReviewTopbar(State.getSelectedReport());
    updateBadges();
    Toast.show('Report sent to publish queue', 'success');
  });

  document.getElementById('btn-request-revision')?.addEventListener('click', () => {
    const report = State.getSelectedReport();
    if (!report) return;

    const commentText = document.getElementById('comment-text')?.value?.trim();
    if (!commentText) {
      Toast.show('Add a comment describing the revision needed before requesting regeneration.', 'error');
      return;
    }

    // Add comment with "sent to regeneration" status
    const section = document.getElementById('comment-section-select')?.value || 'Any Section';
    const priority = document.getElementById('comment-priority')?.value || 'High';
    const settings = State.getSettings();

    const comment = {
      id: uid(),
      reportId: report.id,
      version: report.version,
      section,
      text: commentText,
      priority,
      reviewer: settings.reviewerName,
      timestamp: new Date().toISOString(),
      status: 'sent to regeneration',
    };

    State.addComment(report.id, comment);
    State.updateReportStatus(report.id, 'Needs Revision');
    State.updateHumanStatus(report.id, 'Needs Revision');
    document.getElementById('comment-text').value = '';

    renderComments(State.getSelectedReport());
    renderReviewTopbar(State.getSelectedReport());
    updateBadges();

    Toast.show('Report sent for AI regeneration with your comments', 'info');
  });

  document.getElementById('btn-reject-report')?.addEventListener('click', () => {
    const report = State.getSelectedReport();
    if (!report) return;
    if (!confirm(`Are you sure you want to reject "${report.title}"?`)) return;
    State.updateReportStatus(report.id, 'Rejected');
    State.updateHumanStatus(report.id, 'Rejected');
    renderReviewTopbar(State.getSelectedReport());
    updateBadges();
    Toast.show('Report rejected', 'error');
  });
}


/* ===== LOAD REVIEW VIEW ===== */
function loadReviewView(report) {
  renderReviewTopbar(report);
  renderReportDocument(report);
  renderAIReviewPanel(report);
  renderComments(report);

  // Pre-fill human decision if exists
  const humanDecisionMap = {
    'Approved': 'radio-approved',
    'Needs Revision': 'radio-revision',
    'Rejected': 'radio-rejected',
  };
  const humanStatus = report.humanStatus;
  if (humanDecisionMap[humanStatus]) {
    const radioEl = document.getElementById(humanDecisionMap[humanStatus]);
    if (radioEl) {
      radioEl.checked = true;
      const opt = radioEl.closest('.radio-option');
      if (opt) {
        if (humanStatus === 'Approved') opt.classList.add('selected--approved');
        if (humanStatus === 'Needs Revision') opt.classList.add('selected--revision');
        if (humanStatus === 'Rejected') opt.classList.add('selected--rejected');
      }
    }
  }
}


/* ===== STATE LISTENERS FOR REVIEW ===== */
function initReviewStateListeners() {
  State.on('reportSelected', (report) => {
    if (!report) return;
    loadReviewView(report);
    // Scroll review panel to top
    const panel = document.getElementById('review-panel');
    if (panel) panel.scrollTop = 0;
    const previewScroll = document.getElementById('report-preview-scroll');
    if (previewScroll) previewScroll.scrollTop = 0;
  });

  State.on('viewChanged', (view) => {
    // When switching to review view, ensure content is loaded
    if (view === 'review') {
      const report = State.getSelectedReport();
      if (report) loadReviewView(report);
    }
  });
}
