import type { Metadata } from 'next';
import { DM_Sans, Source_Serif_4 } from 'next/font/google';
import './globals.css';
import { NotificationToasts } from '@/components/dashboard/notification-toasts';
import { ThemeProvider } from '@/components/theme/theme-provider';

const dmSans = DM_Sans({
  subsets: ['latin'],
  variable: '--font-dm-sans',
  display: 'swap',
});

const sourceSerif = Source_Serif_4({
  subsets: ['latin'],
  variable: '--font-source-serif',
  display: 'swap',
});

export const metadata: Metadata = {
  title: 'SentinelX — Enterprise intelligence',
  description: 'AI agents monitoring intelligence, risk, and opportunity 24/7.',
};

const themeInitScript = `(function(){try{var t=localStorage.getItem('sentinelx-theme');var d=t==='dark'||(!t&&matchMedia('(prefers-color-scheme: dark)').matches);document.documentElement.classList.add(d?'dark':'light');}catch(e){document.documentElement.classList.add('light');}})();`;

export default function RootLayout({ children }: Readonly<{ children: React.ReactNode }>) {
  return (
    <html lang="en" suppressHydrationWarning>
      <head>
        <script dangerouslySetInnerHTML={{ __html: themeInitScript }} />
      </head>
      <body className={`${dmSans.variable} ${sourceSerif.variable} font-sans antialiased`}>
        <ThemeProvider>
          {children}
          <NotificationToasts />
        </ThemeProvider>
      </body>
    </html>
  );
}
