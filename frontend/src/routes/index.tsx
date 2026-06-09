// src/routes/index.tsx
import { createBrowserRouter, Navigate } from 'react-router-dom';
import { AppLayout } from '@/components/layout/AppLayout';
import { Dashboard } from '@/pages/Dashboard';
import { AIReviewedList } from '@/pages/AIReviewed';
import { ReportReview } from '@/pages/Review/ReportReview';
import { ApprovedReportsList } from '@/pages/ApprovedReports';
import { PublishedList } from '@/pages/Published';
import { RevisionsList } from '@/pages/Revisions';
import { RejectedList } from '@/pages/Rejected';
import { Settings } from '@/pages/Settings';

export const router = createBrowserRouter([
  {
    path: '/',
    element: <AppLayout />,
    children: [
      { index: true, element: <Navigate to="/dashboard" replace /> },
      { path: 'dashboard', element: <Dashboard /> },
      { path: 'ai-reviewed', element: <AIReviewedList /> },
      { path: 'review/:reportId', element: <ReportReview /> },
      { path: 'approved', element: <ApprovedReportsList /> },
      { path: 'revisions', element: <RevisionsList /> },
      { path: 'rejected', element: <RejectedList /> },
      { path: 'published', element: <PublishedList /> },
      { path: 'settings', element: <Settings /> },
      // Legacy redirects
      { path: 'review', element: <Navigate to="/ai-reviewed" replace /> },
      { path: 'reviewed', element: <Navigate to="/approved" replace /> },
      { path: '*', element: <Navigate to="/dashboard" replace /> },
    ],
  },
]);
