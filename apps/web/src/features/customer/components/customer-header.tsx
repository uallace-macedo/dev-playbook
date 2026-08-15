import { useNavigate } from 'react-router-dom';
import { LogOut, UtensilsCrossed, ReceiptText } from 'lucide-react';
import { useAuth } from '@/features/auth/hooks/use-auth';
import { ROUTES } from '@/config/routes';

export function CustomerHeader() {
  const { logout } = useAuth();
  const navigate = useNavigate();

  return (
    <header className="sticky top-0 z-50 w-full border-b border-slate-800/80 bg-slate-950/80 backdrop-blur-md shrink-0">
      <div className="w-full max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 h-16 flex items-center justify-between">
        <button
          onClick={() => navigate(ROUTES.CUSTOMER.HOME)}
          className="flex items-center gap-2.5 focus:outline-none"
        >
          <div className="p-2 rounded-xl bg-orange-500/10 border border-orange-500/20 text-orange-500">
            <UtensilsCrossed className="w-5 h-5" />
          </div>
          <span className="font-bold text-lg text-white tracking-tight">
            VF<span className="text-orange-500">Delivery</span>
          </span>
        </button>

        <div className="flex items-center gap-3">
          <button
            onClick={() => navigate(ROUTES.CUSTOMER.ORDERS)}
            className="flex items-center gap-2 px-3 py-1.5 rounded-lg border border-slate-800 bg-slate-900/50 hover:bg-slate-800 text-slate-300 hover:text-white text-xs font-medium transition"
          >
            <ReceiptText className="w-4 h-4 text-orange-500" />
            <span>Meus Pedidos</span>
          </button>

          <button
            onClick={logout}
            className="flex items-center gap-2 px-3 py-1.5 rounded-lg border border-slate-800 bg-slate-900/50 hover:bg-slate-800 text-slate-300 hover:text-white text-xs font-medium transition"
          >
            <LogOut className="w-4 h-4 text-slate-400" />
            <span>Sair</span>
          </button>
        </div>
      </div>
    </header>
  );
}