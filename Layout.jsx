import { Outlet } from 'react-router-dom';
import Navbar from './Navbar';
import { Toaster } from '@/components/ui/toaster';

const Layout = () => {
  return (
    <div className="min-h-screen bg-gray-50">
      <Navbar />
      <main className="max-w-7xl mx-auto py-6 px-4 sm:px-6 lg:px-8">
        <Outlet />
      </main>
      <Toaster />
    </div>
  );
};

export default Layout;

