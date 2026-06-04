// src/components/layout/AppLayout.tsx
import React from 'react';
import { Outlet } from 'react-router-dom';
import { Sidebar } from './Sidebar';
import { ToastContainer } from '@/components/common/Toast';

export const AppLayout: React.FC = () => {
  return (
    <div className="app-shell">
      <Sidebar />
      <main className="main-content flex flex-col">
        <Outlet />
      </main>
      <ToastContainer />
    </div>
  );
};
