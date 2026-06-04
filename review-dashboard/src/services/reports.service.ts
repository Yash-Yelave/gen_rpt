// src/services/reports.service.ts
import type { Report } from '@/types';
import { MOCK_REPORTS } from './mockData';

// In-memory store (simulates backend API)
let _reports: Report[] = JSON.parse(JSON.stringify(MOCK_REPORTS));

const delay = (ms = 200) => new Promise((r) => setTimeout(r, ms));

export const reportsService = {
  async getAll(): Promise<Report[]> {
    await delay();
    return _reports;
  },

  async getById(id: string): Promise<Report | null> {
    await delay();
    return _reports.find((r) => r.id === id) ?? null;
  },

  async updateStatus(id: string, status: string): Promise<Report> {
    await delay();
    const report = _reports.find((r) => r.id === id);
    if (!report) throw new Error(`Report ${id} not found`);
    report.status = status;
    report.lastUpdated = new Date().toISOString();
    return { ...report };
  },

  async updateHumanStatus(id: string, humanStatus: string): Promise<Report> {
    await delay();
    const report = _reports.find((r) => r.id === id);
    if (!report) throw new Error(`Report ${id} not found`);
    report.humanStatus = humanStatus;
    report.lastUpdated = new Date().toISOString();
    return { ...report };
  },

  async setPublishReady(id: string, ready: boolean): Promise<Report> {
    await delay();
    const report = _reports.find((r) => r.id === id);
    if (!report) throw new Error(`Report ${id} not found`);
    report.publishReady = ready;
    return { ...report };
  },

  // Reset to initial state (useful for testing)
  reset() {
    _reports = JSON.parse(JSON.stringify(MOCK_REPORTS));
  },
};
