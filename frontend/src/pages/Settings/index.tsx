// src/pages/Settings/index.tsx
import React from 'react';
import { useAuthStore } from '@/store/authStore';
import { useUIStore } from '@/store/uiStore';
import { SectionCard } from '@/components/common/SectionCard';
import { User, Shield } from 'lucide-react';

export const Settings: React.FC = () => {
  const { reviewerName, reviewerRole, setReviewerName, setReviewerRole, aiThreshold, setAiThreshold } = useAuthStore();
  const { showToast } = useUIStore();

  const handleSaveProfile = (e: React.FormEvent) => {
    e.preventDefault();
    showToast('Profile settings saved', 'success');
  };

  const handleSaveSystem = (e: React.FormEvent) => {
    e.preventDefault();
    showToast('System preferences saved', 'success');
  };

  return (
    <div className="p-6 max-w-3xl">
      <div className="mb-6">
        <h1 className="text-xl font-bold text-gray-900 tracking-tight">Settings</h1>
        <p className="text-sm text-gray-500 mt-1">Manage your profile and system preferences</p>
      </div>

      <div className="flex flex-col gap-6">
        <SectionCard title="Reviewer Profile" icon={<User />} defaultOpen className="rounded border border-gray-200">
          <form onSubmit={handleSaveProfile} className="p-4 flex flex-col gap-4">
            <div>
              <label className="block text-[11px] font-semibold text-gray-500 uppercase tracking-wide mb-1.5" htmlFor="name">
                Reviewer Name
              </label>
              <input
                id="name"
                type="text"
                value={reviewerName}
                onChange={(e) => setReviewerName(e.target.value)}
                className="w-full max-w-sm px-3 py-2 border border-gray-200 rounded text-sm text-gray-800 outline-none focus:border-blue-500 focus:ring-2 focus:ring-blue-500/10"
              />
            </div>
            <div>
              <label className="block text-[11px] font-semibold text-gray-500 uppercase tracking-wide mb-1.5" htmlFor="role">
                Role
              </label>
              <input
                id="role"
                type="text"
                value={reviewerRole}
                onChange={(e) => setReviewerRole(e.target.value)}
                className="w-full max-w-sm px-3 py-2 border border-gray-200 rounded text-sm text-gray-800 outline-none focus:border-blue-500 focus:ring-2 focus:ring-blue-500/10"
              />
            </div>
            <div>
              <button type="submit" className="px-4 py-2 bg-blue-700 text-white text-sm font-semibold rounded hover:bg-blue-800 transition-colors">
                Save Profile
              </button>
            </div>
          </form>
        </SectionCard>

        <SectionCard title="System Preferences" icon={<Shield />} defaultOpen className="rounded border border-gray-200">
          <form onSubmit={handleSaveSystem} className="p-4 flex flex-col gap-4">
            <div>
              <label className="block text-[11px] font-semibold text-gray-500 uppercase tracking-wide mb-1.5" htmlFor="threshold">
                AI Auto-Approve Threshold
              </label>
              <div className="flex items-center gap-3 max-w-sm">
                <input
                  id="threshold"
                  type="range"
                  min="50"
                  max="100"
                  value={aiThreshold}
                  onChange={(e) => setAiThreshold(Number(e.target.value))}
                  className="flex-1"
                />
                <span className="text-sm font-bold text-gray-700 min-w-[36px]">{aiThreshold}</span>
              </div>
              <p className="text-xs text-gray-400 mt-1">Reports with an AI score above this threshold can be automatically approved.</p>
            </div>
            <div>
              <button type="submit" className="px-4 py-2 bg-blue-700 text-white text-sm font-semibold rounded hover:bg-blue-800 transition-colors">
                Save Preferences
              </button>
            </div>
          </form>
        </SectionCard>
      </div>
    </div>
  );
};
