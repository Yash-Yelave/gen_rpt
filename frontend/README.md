# BlueOcean Report Review Dashboard

A production-ready React 18 application built with Vite, TypeScript, and TailwindCSS. This dashboard acts as a human-in-the-loop editorial tool for reviewing generated AI reports before publication, allowing reviewers to evaluate AI scores, leave targeted comments, request regenerations, and manage publication state.

---

## 🛠️ Technology Stack

- **Framework**: [React 18](https://react.dev/) + [Vite](https://vitejs.dev/) + [TypeScript](https://www.typescriptlang.org/)
- **Styling**: [TailwindCSS](https://tailwindcss.com/) (using vanilla CSS layout structures and a custom-tailored clean enterprise theme)
- **Routing**: [React Router v6](https://reactrouter.com/) (declarative routing with support for nested layout templates)
- **Data Fetching & Caching**: [TanStack Query v5](https://tanstack.com/query/latest) (React Query)
- **State Management**: [Zustand](https://docs.pmnd.rs/zustand/getting-started/introduction) (separated stores for auth/profile, UI behaviors, and review form states)
- **Icons**: [Lucide React](https://lucide.dev/)

---

## 📂 Project Structure

The project follows a standard, modular React directory structure under the `/src` folder:

```text
src/
├── assets/             # Static assets, logos, and global styles
├── components/         # Reusable presentation and functional components
│   ├── common/         # Generic UI (StatusBadge, EmptyState, SectionCard, Toast)
│   ├── layout/         # Core shell layouts (Sidebar, AppLayout)
│   ├── report/         # Report preview and report card grid components
│   ├── review/         # AI score cards, human review form panels, and top bars
│   └── comments/       # Comment threads, individual comment cards
├── hooks/              # Custom hooks mapping TanStack queries & mutations
├── pages/              # Routed page-level components
│   ├── Dashboard/      # Main stats and aggregate reports table
│   ├── Review/         # List of pending reports and the main 3-panel review screen
│   ├── Reviewed/       # List of approved reports
│   ├── Published/      # List of successfully published reports
│   ├── Revisions/      # List of reports rejected or sent back for revision
│   └── Settings/       # User profile and system score thresholds
├── routes/             # Client-side routing configurations (createBrowserRouter)
├── services/           # Service layer abstraction mimicking backend APIs
├── store/              # Global state managers (Zustand)
├── types/              # Domain-specific TypeScript models and interfaces
├── utils/              # Helper formatters and styling decorators
├── App.tsx             # App entry configuring providers (React Query, Router)
├── index.css           # Global CSS injection including tailwind directives
└── main.tsx            # React DOM mounting entry point
```

---

## 🏗️ State & Service Layer Architecture

### 1. Global State Management (`src/store/`)
- **`authStore.ts`**: Persists current reviewer profile data (Name, Role, and AI Auto-Approve thresholds) to `localStorage`.
- **`uiStore.ts`**: Manages volatile UI states, sidebar toggling, client-side document zooming (70% - 150%), and system-wide dismissible notification toasts.
- **`reviewStore.ts`**: Manages form states (decision selects, section targets, priority levels, and draft review descriptions) on the active review page.

### 2. Service Layer & Hooks (`src/services/` & `src/hooks/`)
- Abstracted backend calls using an asynchronous mock repository (`reports.service`, `comments.service`, `reviews.service`, `publish.service`) simulating realistic API delays.
- Leverages **React Query** (`useQuery` / `useMutation`) in hooks like `useReports` and `useReviewActions` to automate query caching, cache invalidation on edits, and mutate state seamlessly.

---

## 🚀 Getting Started

### Prerequisites
- [Node.js](https://nodejs.org/) (v18.0.0 or higher recommended)
- `npm` (packaged with Node)

### Installation

1. Navigate to the `frontend/` directory:
   ```bash
   cd frontend
   ```

2. Install dependencies:
   ```bash
   npm install
   ```

### Running Locally

To boot up the local Vite development server:
```bash
npm run dev
```
The application will run by default on [http://localhost:5173](http://localhost:5173).

### Building for Production

To compile static assets for production (optimized and outputted to the `dist/` directory, ready to be deployed to platforms like Cloudflare Pages):
```bash
npm run build
```

---

## 🎨 Layout & Design Integrity
- **Color Scheme**: Employs a strict minimalist, enterprise-grade design utilizing the *BlueOcean* color scheme (white background, clean grey borders, dark text, and specific shades of blue for highlighting).
- **Layout Panels**: The core report-review interface is structured as a responsive 3-panel system:
  1. **Left Sidebar**: Handles app navigation, user profiles, and reactive counter badges.
  2. **Middle Panel (Document Preview)**: Emulates a physical document sheet complete with text formatting and custom text zoom buttons.
  3. **Right Panel (AI & Human Evaluations)**: Standardised collapsible cards displaying granular AI feedback, editorial action forms, and chronologically ordered comments.
