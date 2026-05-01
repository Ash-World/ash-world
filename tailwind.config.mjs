/** @type {import('tailwindcss').Config} */
export default {
  content: ['./src/**/*.{astro,html,js,jsx,md,mdx,ts,tsx}'],
  theme: {
    extend: {
      colors: {
        bg: {
          primary: '#0a0a0f',
          secondary: '#0d1117',
          card: 'rgba(255,255,255,0.04)',
        },
        accent: {
          amber: '#f59e0b',
          gold: '#d97706',
          warm: '#fb923c',
        },
        text: {
          primary: '#f1f5f9',
          secondary: '#94a3b8',
          muted: '#475569',
        },
        border: {
          subtle: 'rgba(255,255,255,0.08)',
          hover: 'rgba(255,255,255,0.16)',
        },
      },
      fontFamily: {
        sans: ['Pretendard', 'system-ui', 'sans-serif'],
        mono: ['JetBrains Mono', 'monospace'],
      },
      backdropBlur: {
        xs: '2px',
      },
      backgroundImage: {
        'gradient-radial': 'radial-gradient(var(--tw-gradient-stops))',
        'gradient-amber': 'linear-gradient(135deg, #f59e0b, #fb923c)',
      },
      typography: {
        DEFAULT: {
          css: {
            color: '#cbd5e1',
            a: { color: '#f59e0b' },
            strong: { color: '#f1f5f9' },
            h1: { color: '#f1f5f9' },
            h2: { color: '#f1f5f9' },
            h3: { color: '#f1f5f9' },
            code: { color: '#fb923c' },
            'pre code': { color: '#cbd5e1' },
          },
        },
      },
    },
  },
  plugins: [require('@tailwindcss/typography')],
};
