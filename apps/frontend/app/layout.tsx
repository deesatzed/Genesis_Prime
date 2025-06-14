import type { Metadata } from 'next';
import { Inter } from 'next/font/google';
import './globals.css';
import { ThemeProvider } from '@/components/theme-provider';
import { Toaster } from '@/components/ui/toaster';
import ClientOverlays from '@/components/client-overlays';

const inter = Inter({ 
  subsets: ['latin'],
  display: 'swap',
  variable: '--font-inter',
});

export const metadata: Metadata = {
  title: 'Agno Swarm Demo - Consciousness as Controlled Hallucination',
  description: 'A prototype demonstration of agentic swarm AI implementing consciousness through predictive processing and controlled hallucination.',
  keywords: ['AI', 'consciousness', 'swarm intelligence', 'predictive processing', 'controlled hallucination', 'Agno-AGI'],
  authors: [{ name: 'Agno Swarm Team' }],
  viewport: 'width=device-width, initial-scale=1',
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en" suppressHydrationWarning className={`${inter.variable}`}>
      <body className="min-h-screen bg-gradient-to-br from-slate-950 to-slate-900 text-slate-100 antialiased">
        <ThemeProvider
          attribute="class"
          defaultTheme="dark"
          enableSystem={false}
          disableTransitionOnChange
        >
          <div className="flex flex-col min-h-screen">
            <main className="flex-1">
              {children}
            </main>
          </div>
          <ClientOverlays />
          <Toaster />
        </ThemeProvider>
      </body>
    </html>
  );
}
