/** @type {import('tailwindcss').Config} */
export default {
  content: ['./src/**/*.{astro,html,js,jsx,md,mdx,ts,tsx}'],
  theme: {
    extend: {
      colors: {
        bg: {
          primary: '#100f0d',
          secondary: '#161412',
          card: 'rgba(255,248,235,0.04)',
          article: 'rgba(255,248,235,0.025)',
        },
        accent: {
          amber: '#e8a742',
          gold: '#c98a2a',
          warm: '#e07b3a',
        },
        text: {
          primary: '#ede8e0',
          secondary: '#a09890',
          muted: '#5c564f',
        },
        border: {
          subtle: 'rgba(255,240,210,0.08)',
          hover: 'rgba(255,240,210,0.15)',
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
        'gradient-amber': 'linear-gradient(135deg, #e8a742, #e07b3a)',
      },
      typography: {
        DEFAULT: {
          css: {
            '--tw-prose-body': '#c8c0b4',
            '--tw-prose-headings': '#ede8e0',
            '--tw-prose-lead': '#a09890',
            '--tw-prose-links': '#e8a742',
            '--tw-prose-bold': '#ede8e0',
            '--tw-prose-counters': '#7a7068',
            '--tw-prose-bullets': '#5c564f',
            '--tw-prose-hr': 'rgba(255,240,210,0.10)',
            '--tw-prose-quotes': '#a09890',
            '--tw-prose-quote-borders': 'rgba(232,167,66,0.35)',
            '--tw-prose-captions': '#7a7068',
            '--tw-prose-code': '#e07b3a',
            '--tw-prose-pre-code': '#c8c0b4',
            '--tw-prose-pre-bg': 'rgba(0,0,0,0.35)',
            '--tw-prose-th-borders': 'rgba(255,240,210,0.12)',
            '--tw-prose-td-borders': 'rgba(255,240,210,0.07)',
            color: '#c8c0b4',
            lineHeight: '1.85',
            a: { color: '#e8a742', textDecoration: 'none' },
            'a:hover': { textDecoration: 'underline' },
            strong: { color: '#ede8e0' },
            h1: { color: '#ede8e0', fontWeight: '700' },
            h2: { color: '#e8e2d8', fontWeight: '600' },
            h3: { color: '#e0d9ce', fontWeight: '600' },
            h4: { color: '#d8d0c4' },
            blockquote: {
              borderLeftColor: 'rgba(232,167,66,0.35)',
              color: '#a09890',
              fontStyle: 'normal',
            },
            code: {
              color: '#e07b3a',
              backgroundColor: 'rgba(255,248,235,0.06)',
              padding: '0.15em 0.4em',
              borderRadius: '0.25rem',
              fontWeight: '400',
            },
            'code::before': { content: '""' },
            'code::after': { content: '""' },
            'pre code': { color: '#c8c0b4', backgroundColor: 'transparent', padding: '0' },
            img: {
              borderRadius: '0.75rem',
            },
            hr: { borderColor: 'rgba(255,240,210,0.10)' },
            table: { fontSize: '0.9em' },
            th: { color: '#ede8e0' },
          },
        },
      },
    },
  },
  plugins: [require('@tailwindcss/typography')],
};
