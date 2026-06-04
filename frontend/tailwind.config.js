/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      fontFamily: {
        sans: ['Inter', '-apple-system', 'BlinkMacSystemFont', 'Segoe UI', 'sans-serif'],
      },
      colors: {
        // Brand Blues (matching CSS variables from existing design)
        blue: {
          50:  '#EFF6FF',
          100: '#DBEAFE',
          200: '#BFDBFE',
          400: '#60A5FA',
          500: '#3B82F6',
          600: '#2563EB',
          700: '#1A56DB',
          800: '#1A3A8F',
          900: '#0C2463',
        },
        // Semantic greens
        green: {
          50:  '#ECFDF5',
          100: '#D1FAE5',
          600: '#059669',
          700: '#047857',
        },
        // Semantic oranges
        orange: {
          50:  '#FFFBEB',
          100: '#FEF3C7',
          600: '#D97706',
          700: '#B45309',
        },
        // Semantic reds
        red: {
          50:  '#FEF2F2',
          100: '#FEE2E2',
          600: '#DC2626',
          700: '#B91C1C',
        },
        // Grays (used extensively)
        gray: {
          50:  '#F9FAFB',
          100: '#F3F4F6',
          200: '#E5E7EB',
          300: '#D1D5DB',
          400: '#9CA3AF',
          500: '#6B7280',
          600: '#4B5563',
          700: '#374151',
          800: '#1F2937',
          900: '#111827',
        },
        // App surface tokens
        surface: {
          body:  '#F5F7FA',
          white: '#FFFFFF',
          panel: '#F8FAFC',
        },
        border: {
          DEFAULT: '#E5E7EB',
        },
      },
      fontSize: {
        'xs':   ['0.75rem',   { lineHeight: '1rem' }],
        'sm':   ['0.8125rem', { lineHeight: '1.25rem' }],
        'base': ['0.875rem',  { lineHeight: '1.5rem' }],
        'md':   ['1rem',      { lineHeight: '1.5rem' }],
        'lg':   ['1.125rem',  { lineHeight: '1.75rem' }],
        'xl':   ['1.25rem',   { lineHeight: '1.75rem' }],
        '2xl':  ['1.5rem',    { lineHeight: '2rem' }],
      },
      boxShadow: {
        'xs': '0 1px 2px rgba(0,0,0,0.06)',
        'sm': '0 1px 3px rgba(0,0,0,0.08), 0 1px 2px rgba(0,0,0,0.04)',
        'md': '0 4px 6px rgba(0,0,0,0.07), 0 2px 4px rgba(0,0,0,0.04)',
      },
      width: {
        sidebar: '224px',
      },
      height: {
        topbar: '60px',
      },
      screens: {
        'xs': '480px',
        'sm': '640px',
        'md': '768px',
        'lg': '1024px',
        'xl': '1280px',
      },
    },
  },
  plugins: [],
}
