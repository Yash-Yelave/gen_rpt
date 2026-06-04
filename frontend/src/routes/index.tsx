// src/routes/index.tsx
import { createBrowserRouter, Navigate } from 'react-router-dom';
import { AppLayout } from '@/components/layout/AppLayout';
import { Dashboard } from '@/pages/Dashboard';
import { PendingReviewList } from '@/pages/Review';
import { ReportReview } from '@/pages/Review/ReportReview';
import { ReviewedList } from '@/pages/Reviewed';
import { PublishedList } from '@/pages/Published';
import { RevisionsList } from '@/pages/Revisions';
import { Settings } from '@/pages/Settings';

export const router = createBrowserRouter([
  {
    path: '/',
    element: <AppLayout />,
    children: [
      { index: true, element: <Navigate to="/dashboard" replace /> },
      { path: 'dashboard', element: <Dashboard /> },
      { path: 'review', element: <PendingReviewList /> },
      { path: 'review/:reportId', element: <ReportReview /> },
      { path: 'reviewed', element: <ReviewedList /> },
      { path: 'published', element: <PublishedList /> },
      { path: 'revisions', element: <RevisionsList /> },
      { path: 'settings', element: <Settings /> },
      { path: '*', element: <Navigate to="/dashboard" replace /> },
    ],
  },
]);
