import { useState } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { Menu, X, User, LogOut, Home, Users, Briefcase, Calculator, Calendar, Package, Settings } from 'lucide-react';
import { Button } from '@/components/ui/button';
import { logout, getCurrentUser } from '@/services/auth';

const Navbar = () => {
  const [isOpen, setIsOpen] = useState(false);
  const navigate = useNavigate();
  const user = getCurrentUser();

  const handleLogout = () => {
    logout();
    navigate('/login');
  };

  const toggleMenu = () => {
    setIsOpen(!isOpen);
  };

  const closeMenu = () => {
    setIsOpen(false);
  };

  const navItems = [
    { name: 'Dashboard', path: '/', icon: <Home className="w-5 h-5 mr-2" /> },
    { name: 'Clientes', path: '/clients', icon: <Users className="w-5 h-5 mr-2" /> },
    { name: 'Projetos', path: '/projects', icon: <Briefcase className="w-5 h-5 mr-2" /> },
    { name: 'Orçamentos', path: '/estimates', icon: <Calculator className="w-5 h-5 mr-2" /> },
    { name: 'Agenda', path: '/schedule', icon: <Calendar className="w-5 h-5 mr-2" /> },
    { name: 'Materiais', path: '/materials', icon: <Package className="w-5 h-5 mr-2" /> },
  ];

  return (
    <nav className="bg-primary text-white shadow-md">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex items-center justify-between h-16">
          <div className="flex items-center">
            <div className="flex-shrink-0">
              <Link to="/" className="flex items-center">
                <span className="text-xl font-bold">Tile System</span>
              </Link>
            </div>
            <div className="hidden md:block">
              <div className="ml-10 flex items-baseline space-x-4">
                {navItems.map((item) => (
                  <Link
                    key={item.path}
                    to={item.path}
                    className="flex items-center px-3 py-2 rounded-md text-sm font-medium hover:bg-primary-dark transition-colors"
                  >
                    {item.icon}
                    {item.name}
                  </Link>
                ))}
              </div>
            </div>
          </div>
          <div className="hidden md:block">
            <div className="ml-4 flex items-center md:ml-6">
              <div className="ml-3 relative flex items-center">
                <Link to="/profile" className="flex items-center px-3 py-2 rounded-md text-sm font-medium hover:bg-primary-dark transition-colors">
                  <User className="w-5 h-5 mr-2" />
                  {user?.name}
                </Link>
                <Button
                  variant="ghost"
                  onClick={handleLogout}
                  className="flex items-center px-3 py-2 rounded-md text-sm font-medium hover:bg-primary-dark transition-colors"
                >
                  <LogOut className="w-5 h-5 mr-2" />
                  Sair
                </Button>
              </div>
            </div>
          </div>
          <div className="-mr-2 flex md:hidden">
            <button
              onClick={toggleMenu}
              className="inline-flex items-center justify-center p-2 rounded-md text-white hover:bg-primary-dark focus:outline-none"
            >
              <span className="sr-only">Abrir menu principal</span>
              {isOpen ? <X className="block h-6 w-6" /> : <Menu className="block h-6 w-6" />}
            </button>
          </div>
        </div>
      </div>

      {/* Mobile menu */}
      {isOpen && (
        <div className="md:hidden">
          <div className="px-2 pt-2 pb-3 space-y-1 sm:px-3">
            {navItems.map((item) => (
              <Link
                key={item.path}
                to={item.path}
                className="flex items-center px-3 py-2 rounded-md text-base font-medium hover:bg-primary-dark transition-colors"
                onClick={closeMenu}
              >
                {item.icon}
                {item.name}
              </Link>
            ))}
          </div>
          <div className="pt-4 pb-3 border-t border-gray-700">
            <div className="flex items-center px-5">
              <div className="flex-shrink-0">
                <User className="h-10 w-10 rounded-full" />
              </div>
              <div className="ml-3">
                <div className="text-base font-medium">{user?.name}</div>
                <div className="text-sm font-medium text-gray-300">{user?.email}</div>
              </div>
            </div>
            <div className="mt-3 px-2 space-y-1">
              <Link
                to="/profile"
                className="flex items-center px-3 py-2 rounded-md text-base font-medium hover:bg-primary-dark transition-colors"
                onClick={closeMenu}
              >
                <User className="w-5 h-5 mr-2" />
                Perfil
              </Link>
              <Link
                to="/settings"
                className="flex items-center px-3 py-2 rounded-md text-base font-medium hover:bg-primary-dark transition-colors"
                onClick={closeMenu}
              >
                <Settings className="w-5 h-5 mr-2" />
                Configurações
              </Link>
              <button
                onClick={() => {
                  handleLogout();
                  closeMenu();
                }}
                className="flex w-full items-center px-3 py-2 rounded-md text-base font-medium hover:bg-primary-dark transition-colors"
              >
                <LogOut className="w-5 h-5 mr-2" />
                Sair
              </button>
            </div>
          </div>
        </div>
      )}
    </nav>
  );
};

export default Navbar;

