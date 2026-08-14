import { useNavigate } from 'react-router-dom';
import { Store, ShoppingBag, ClipboardList, ArrowRight } from 'lucide-react';
import type { Restaurant } from '../types';

type RestaurantCardProps = {
  restaurant: Restaurant;
};

export function RestaurantCard({ restaurant }: RestaurantCardProps) {
  const navigate = useNavigate();

  return (
    <div className="bg-slate-900 border border-slate-800 rounded-2xl p-6 shadow-xl flex flex-col justify-between hover:border-slate-700 transition">
      <div>
        <div className="flex items-start justify-between gap-4 mb-4">
          <div className="p-3 bg-slate-950 border border-slate-800 rounded-2xl text-orange-500">
            <Store className="w-6 h-6" />
          </div>
          <span className="text-[10px] font-bold text-orange-400 bg-orange-500/10 border border-orange-500/20 px-2.5 py-1 rounded-full uppercase tracking-wider">
            Ativo
          </span>
        </div>

        <h3 className="text-xl font-bold text-white mb-2">{restaurant.name}</h3>
        <p className="text-sm text-slate-400 line-clamp-2 mb-6">
          {restaurant.description || 'Nenhuma descrição cadastrada.'}
        </p>
      </div>

      <div className="pt-4 border-t border-slate-800/80 flex flex-col gap-2">
        <button
          onClick={() => navigate(`/restaurant/${restaurant.id}/orders`)}
          className="w-full py-2.5 px-4 bg-orange-500 hover:bg-orange-600 text-white font-semibold rounded-xl transition flex items-center justify-center gap-2 text-sm shadow-md shadow-orange-500/10"
        >
          <ClipboardList className="w-4 h-4" />
          <span>Ver Pedidos</span>
          <ArrowRight className="w-4 h-4 ml-auto" />
        </button>

        <button
          onClick={() => navigate(`/restaurant/${restaurant.id}/products`)}
          className="w-full py-2.5 px-4 bg-slate-800 hover:bg-slate-700 text-slate-200 font-semibold rounded-xl transition flex items-center justify-center gap-2 text-sm border border-slate-700"
        >
          <ShoppingBag className="w-4 h-4" />
          <span>Gerenciar Cardápio</span>
        </button>
      </div>
    </div>
  );
}