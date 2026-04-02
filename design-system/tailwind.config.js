/**
 * Airwallex Tailwind CSS Configuration
 * =====================================
 *
 * Complete theme configuration based on Airwallex Brand Guidelines.
 * Use with: @import './tokens/colors.css'; etc.
 */

/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    './src/**/*.{js,ts,jsx,tsx,html}',
    './pages/**/*.{js,ts,jsx,tsx}',
    './components/**/*.{js,ts,jsx,tsx}',
    './app/**/*.{js,ts,jsx,tsx}',
  ],
  darkMode: ['class', '[data-theme="dark"]'],
  theme: {
    extend: {
      /* ========================================
         COLORS
         ======================================== */
      colors: {
        // Airwallex Orange - Primary Brand
        'awx-orange': {
          50: '#FFF7F5',
          100: '#FFEBE5',
          200: '#FFD4C7',
          300: '#FFB199',
          400: '#FF8A66',
          500: '#FF6B40', // Primary
          600: '#F54D1F',
          700: '#D93D12',
          800: '#B33210',
          900: '#8F2A0F',
        },
        // Coral (for gradients)
        'awx-coral': {
          400: '#FF8066',
          500: '#FF6B5B',
          600: '#F55046',
        },
        // Spend - Pink/Magenta
        'awx-spend': {
          50: '#FFF5F8',
          100: '#FFE5ED',
          200: '#FFCCD9',
          300: '#FFA3BC',
          400: '#FF7A9E',
          500: '#FF5082',
          600: '#E6366A',
          700: '#C42555',
          800: '#A11F47',
          900: '#7D1A3A',
        },
        // Payments - Blue
        'awx-payments': {
          50: '#F0F7FF',
          100: '#E0EFFF',
          200: '#B8DBFF',
          300: '#85C1FF',
          400: '#52A3FF',
          500: '#2B7FFF',
          600: '#1A5FDB',
          700: '#1347B0',
          800: '#0F3785',
          900: '#0B2860',
        },
        // Platform APIs - Purple
        'awx-platform': {
          50: '#FAF5FF',
          100: '#F3E8FF',
          200: '#E9D5FF',
          300: '#D8B4FE',
          400: '#C084FC',
          500: '#A855F7',
          600: '#9333EA',
          700: '#7E22CE',
          800: '#6B21A8',
          900: '#581C87',
        },
        // Gray scale
        'awx-gray': {
          50: '#FAFAFA',
          100: '#F5F5F5',
          200: '#E5E5E5',
          300: '#D4D4D4',
          400: '#A3A3A3',
          500: '#737373',
          600: '#525252',
          700: '#404040',
          800: '#262626',
          900: '#171717',
          950: '#0A0A0A',
        },
      },

      /* ========================================
         TYPOGRAPHY
         ======================================== */
      fontFamily: {
        sans: ['Circular', 'DM Sans', '-apple-system', 'BlinkMacSystemFont', 'Segoe UI', 'Roboto', 'sans-serif'],
        chinese: ['Source Han Sans', 'Noto Sans SC', 'PingFang SC', 'Microsoft YaHei', 'sans-serif'],
        mono: ['SF Mono', 'Fira Code', 'Fira Mono', 'Menlo', 'Monaco', 'Consolas', 'monospace'],
      },
      fontSize: {
        'awx-xs': ['0.75rem', { lineHeight: '1rem' }],
        'awx-sm': ['0.875rem', { lineHeight: '1.25rem' }],
        'awx-base': ['1rem', { lineHeight: '1.5rem' }],
        'awx-lg': ['1.125rem', { lineHeight: '1.75rem' }],
        'awx-xl': ['1.25rem', { lineHeight: '1.75rem' }],
        'awx-2xl': ['1.5rem', { lineHeight: '2rem' }],
        'awx-3xl': ['1.875rem', { lineHeight: '2.25rem' }],
        'awx-4xl': ['2.25rem', { lineHeight: '2.5rem' }],
        'awx-5xl': ['3rem', { lineHeight: '1.2' }],
        'awx-6xl': ['3.75rem', { lineHeight: '1.2' }],
        'awx-7xl': ['4.5rem', { lineHeight: '1.1' }],
        'awx-8xl': ['6rem', { lineHeight: '1.1' }],
      },
      letterSpacing: {
        'awx-tighter': '-0.05em',
        'awx-tight': '-0.025em',
        'awx-normal': '0',
        'awx-wide': '0.025em',
        'awx-wider': '0.05em',
        'awx-widest': '0.1em',
      },

      /* ========================================
         SPACING
         ======================================== */
      spacing: {
        'awx-section': '6rem',
        'awx-container': '1.5rem',
      },

      /* ========================================
         BORDER RADIUS
         ======================================== */
      borderRadius: {
        'awx-sm': '0.25rem',
        'awx-md': '0.5rem',
        'awx-lg': '0.75rem',
        'awx-xl': '1rem',
        'awx-2xl': '1.5rem',
        'awx-3xl': '2rem',
      },

      /* ========================================
         BOX SHADOW
         ======================================== */
      boxShadow: {
        'awx-xs': '0 1px 2px 0 rgb(0 0 0 / 0.05)',
        'awx-sm': '0 1px 3px 0 rgb(0 0 0 / 0.1), 0 1px 2px -1px rgb(0 0 0 / 0.1)',
        'awx-md': '0 4px 6px -1px rgb(0 0 0 / 0.1), 0 2px 4px -2px rgb(0 0 0 / 0.1)',
        'awx-lg': '0 10px 15px -3px rgb(0 0 0 / 0.1), 0 4px 6px -4px rgb(0 0 0 / 0.1)',
        'awx-xl': '0 20px 25px -5px rgb(0 0 0 / 0.1), 0 8px 10px -6px rgb(0 0 0 / 0.1)',
        'awx-2xl': '0 25px 50px -12px rgb(0 0 0 / 0.25)',
        'awx-orange': '0 10px 40px -10px rgba(255, 107, 64, 0.4)',
        'awx-orange-lg': '0 20px 60px -15px rgba(255, 107, 64, 0.5)',
      },

      /* ========================================
         ANIMATION
         ======================================== */
      transitionDuration: {
        'awx-75': '75ms',
        'awx-100': '100ms',
        'awx-150': '150ms',
        'awx-200': '200ms',
        'awx-300': '300ms',
        'awx-500': '500ms',
        'awx-700': '700ms',
        'awx-1000': '1000ms',
      },
      transitionTimingFunction: {
        'awx-ease-in': 'cubic-bezier(0.4, 0, 1, 1)',
        'awx-ease-out': 'cubic-bezier(0, 0, 0.2, 1)',
        'awx-ease-in-out': 'cubic-bezier(0.4, 0, 0.2, 1)',
        'awx-bounce': 'cubic-bezier(0.68, -0.55, 0.265, 1.55)',
        'awx-spring': 'cubic-bezier(0.175, 0.885, 0.32, 1.275)',
      },
      animation: {
        'awx-fade-in': 'awx-fade-in 0.3s ease-out',
        'awx-fade-in-up': 'awx-fade-in-up 0.4s ease-out',
        'awx-slide-in-right': 'awx-slide-in-right 0.3s ease-out',
        'awx-scale-in': 'awx-scale-in 0.2s ease-out',
        'awx-pulse-orange': 'awx-pulse-orange 2s infinite',
      },
      keyframes: {
        'awx-fade-in': {
          '0%': { opacity: '0' },
          '100%': { opacity: '1' },
        },
        'awx-fade-in-up': {
          '0%': { opacity: '0', transform: 'translateY(16px)' },
          '100%': { opacity: '1', transform: 'translateY(0)' },
        },
        'awx-slide-in-right': {
          '0%': { opacity: '0', transform: 'translateX(-16px)' },
          '100%': { opacity: '1', transform: 'translateX(0)' },
        },
        'awx-scale-in': {
          '0%': { opacity: '0', transform: 'scale(0.95)' },
          '100%': { opacity: '1', transform: 'scale(1)' },
        },
        'awx-pulse-orange': {
          '0%, 100%': { boxShadow: '0 0 0 0 rgba(255, 107, 64, 0.4)' },
          '50%': { boxShadow: '0 0 0 8px rgba(255, 107, 64, 0)' },
        },
      },

      /* ========================================
         Z-INDEX
         ======================================== */
      zIndex: {
        'awx-dropdown': '20',
        'awx-sticky': '40',
        'awx-modal-backdrop': '50',
        'awx-modal': '60',
        'awx-tooltip': '70',
        'awx-notification': '80',
        'awx-loading': '90',
      },

      /* ========================================
         MAX WIDTH
         ======================================== */
      maxWidth: {
        'awx-prose': '65ch',
        'awx-container': '80rem',
        'awx-container-sm': '64rem',
      },

      /* ========================================
         BACKGROUND IMAGE (GRADIENTS)
         ======================================== */
      backgroundImage: {
        'awx-gradient-business': 'linear-gradient(135deg, #FF6B40 0%, #FF6B5B 100%)',
        'awx-gradient-spend': 'linear-gradient(135deg, #FF5082 0%, #FF7A9E 100%)',
        'awx-gradient-payments': 'linear-gradient(135deg, #2B7FFF 0%, #52A3FF 100%)',
        'awx-gradient-platform': 'linear-gradient(135deg, #A855F7 0%, #FF5082 100%)',
        'awx-gradient-hero': 'linear-gradient(135deg, #FF6B40 0%, #FF8066 50%, #FF7A9E 100%)',
      },
    },
  },
  plugins: [
    // Add any Tailwind plugins here
    // require('@tailwindcss/typography'),
    // require('@tailwindcss/forms'),
  ],
};
