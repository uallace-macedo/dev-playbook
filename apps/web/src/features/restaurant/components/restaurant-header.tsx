import { useNavigate } from 'react-router-dom';
import { Store, Plus, LogOut } from 'lucide-react';
import { useAuth } from '@/features/auth/hooks/use-auth';
import { ROUTES } from '@/config/routes';

type RestaurantHeaderProps = {
  onOpenCreateModal?: () => void;
};

export function RestaurantHeader({ onOpenCreateModal }: RestaurantHeaderProps) {
  const navigate = useNavigate();
  const { logout } = useAuth();

  function handleLogout() {
    if (logout) {
      logout();
    } else {
      localStorage.removeItem('token');
    }
    navigate(ROUTES.AUTH.LOGIN, { replace: true });
  }

  return (
    <header className="border-b border-slate-800/80 bg-slate-950/80 backdrop-blur-md shrink-0">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 h-16 flex items-center justify-between">
        <div className="flex items-center gap-2.5">
          <div className="p-2 rounded-xl bg-orange-500/10 border border-orange-500/20 text-orange-500">
            <Store className="w-5 h-5" />
          </div>
          <span className="font-bold text-lg text-white tracking-tight">
            Painel do<span className="text-orange-500"> Restaurante</span>
          </span>
        </div>

        <div className="flex items-center gap-3">
          {onOpenCreateModal && (
            <button
              onClick={onOpenCreateModal}
              className="py-2 px-3.5 bg-orange-500 hover:bg-orange-600 text-white font-semibold rounded-xl transition flex items-center gap-2 text-xs sm:text-sm shadow-lg shadow-orange-500/20"
            >
              <Plus className="w-4 h-4" />
              <span>Novo Restaurante</span>
            </button>
          )}

          <button
            onClick={handleLogout}
            className="flex items-center gap-2 px-3 py-2 rounded-xl border border-slate-800 bg-slate-900/50 hover:bg-slate-800 text-slate-300 hover:text-white text-xs font-medium transition"
            title="Sair do sistema"
          >
            <LogOut className="w-4 h-4 text-slate-400" />
            <span className="hidden sm:inline">Sair</span>
          </button>
        </div>
      </div>
    </header>
  );
}