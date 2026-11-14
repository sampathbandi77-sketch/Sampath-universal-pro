import './globals.css';
import PWARegister from '../components/PWARegister';
import type { Metadata } from 'next';
export const metadata: Metadata = { title: 'SAMPATH UNIVERSAL PRO', description: 'Universal AI Trading Intelligence', manifest: '/manifest.json', themeColor: '#07111f' };
export default function RootLayout({ children }: Readonly<{ children: React.ReactNode }>) { return <html lang="en"><body><PWARegister />{children}</body></html>; }
