// src/components/layout/Sidebar.tsx
import React from 'react';
import { NavLink } from 'react-router-dom';
import {
  LayoutDashboard,
  Bot,
  CheckCircle,
  Send,
  RotateCcw,
  XCircle,
  Settings,
  Waves,
} from 'lucide-react';
import { useAuthStore } from '@/store/authStore';
import { useDashboardMetrics } from '@/hooks/useReports';

const navItems = [
  { to: '/dashboard', label: 'Dashboard', icon: LayoutDashboard },
  { to: '/ai-reviewed', label: 'AI Reviewed', icon: Bot, badge: 'pendingHuman' },
  { to: '/approved', label: 'Approved Reports', icon: CheckCircle },
  { to: '/revisions', label: 'Revision Queue', icon: RotateCcw, badge: 'needsRevision' },
  { to: '/rejected', label: 'Rejected', icon: XCircle, badge: 'rejected' },
  { to: '/published', label: 'Published', icon: Send },
];

interface Props {
  onCloseMobile?: () => void;
}

export const Sidebar: React.FC<Props> = ({ onCloseMobile }) => {
  const { reviewerName, reviewerRole, getAvatarInitials } = useAuthStore();
  const metrics = useDashboardMetrics();

  const getBadgeCount = (key: string): number => {
    return (metrics as Record<string, number>)[key] ?? 0;
  };

  return (
    <aside className="w-[224px] md:w-[68px] lg:w-[224px] h-full bg-white flex flex-col flex-shrink-0 overflow-y-auto overflow-x-hidden transition-all duration-300">
      {/* Brand */}
      <div className="px-4 py-5 border-b border-gray-200">
        <div className="flex items-center gap-2 md:justify-center lg:justify-start">
          <div className="w-[22px] h-[22px] rounded-[5px] bg-blue-700 flex items-center justify-center flex-shrink-0">
            <Waves className="w-3 h-3 text-white" />
          </div>
          <span className="text-base font-bold text-blue-800 tracking-tight md:hidden lg:block">BlueOcean</span>
        </div>
        <div className="text-xs text-gray-400 mt-0.5 pl-[30px] md:hidden lg:block">Report Review</div>
      </div>

      {/* Nav */}
      <nav className="flex-1 px-3 py-3">
        <ul className="flex flex-col gap-0.5">
          {navItems.map(({ to, label, icon: Icon, badge }) => {
            const count = badge ? getBadgeCount(badge) : 0;
            return (
              <li key={to}>
                <NavLink
                  to={to}
                  onClick={onCloseMobile}
                  className={({ isActive }) =>
                    `flex items-center gap-2 px-3 py-2 rounded text-sm font-medium transition-colors focus:outline-none focus-visible:ring-2 focus-visible:ring-blue-500
                     ${isActive
                       ? 'bg-blue-50 text-blue-700 font-semibold'
                       : 'text-gray-600 hover:bg-blue-50 hover:text-blue-700'
                     } md:justify-center lg:justify-start`
                  }
                  title={label}
                >
                  <Icon className="w-4 h-4 flex-shrink-0" />
                  <span className="flex-1 md:hidden lg:block">{label}</span>
                  {badge && count > 0 && (
                    <span className={`md:hidden lg:inline-flex items-center px-1.5 py-0.5 rounded-full text-[11px] font-semibold ${
                      badge === 'needsRevision' ? 'bg-orange-100 text-orange-700'
                      : badge === 'rejected' ? 'bg-red-100 text-red-700'
                      : 'bg-blue-100 text-blue-800'
                    }`}>
                      {count}
                    </span>
                  )}
                </NavLink>
              </li>
            );
          })}
        </ul>

        <div className="text-[10px] font-semibold tracking-widest uppercase text-gray-400 px-2 py-4 pb-2 md:hidden lg:block">System</div>
        <ul>
          <li>
            <NavLink
              to="/settings"
              onClick={onCloseMobile}
              className={({ isActive }) =>
                `flex items-center gap-2 px-3 py-2 rounded text-sm font-medium transition-colors focus:outline-none focus-visible:ring-2 focus-visible:ring-blue-500
                 ${isActive ? 'bg-blue-50 text-blue-700 font-semibold' : 'text-gray-600 hover:bg-blue-50 hover:text-blue-700'} md:justify-center lg:justify-start`
              }
              title="Settings"
            >
              <Settings className="w-4 h-4 flex-shrink-0" />
              <span className="md:hidden lg:inline">Settings</span>
            </NavLink>
          </li>
        </ul>
      </nav>

      {/* User */}
      <div className="px-4 py-4 border-t border-gray-200 flex items-center gap-3 md:justify-center lg:justify-start">
        <div className="w-8 h-8 rounded-full bg-blue-100 text-blue-700 text-xs font-bold flex items-center justify-center flex-shrink-0">
          {getAvatarInitials()}
        </div>
        <div className="min-w-0 md:hidden lg:block">
          <div className="text-sm font-semibold text-gray-800 truncate">{reviewerName}</div>
          <div className="text-xs text-gray-400">{reviewerRole}</div>
        </div>
      </div>
    </aside>
  );
};
