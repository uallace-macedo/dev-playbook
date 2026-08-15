import { Link } from 'react-router-dom';
import type { Restaurant } from '../types';

type RestaurantCardProps = {
  restaurant: Restaurant;
};

export function RestaurantCard({ restaurant }: RestaurantCardProps) {
  return (
    <Link
      to={`/customer/restaurant/${restaurant.id}`}
      className="group bg-slate-900 border border-slate-800 hover:border-orange-500/50 rounded-2xl p-5 transition duration-200 flex flex-col justify-between"
    >
      <div>
        <div className="flex items-start justify-between gap-2 mb-2">
          <h3 className="text-lg font-bold text-white group-hover:text-orange-400 transition">
            {restaurant.name}
          </h3>
          <div className="flex items-center gap-1 bg-amber-500/10 border border-amber-500/20 px-2 py-0.5 rounded-full text-xs font-semibold text-amber-400">
            <span>★</span>
            <span>{restaurant.rating_average.toFixed(1)}</span>
            <span className="text-slate-500">({restaurant.total_reviews})</span>
          </div>
        </div>

        <p className="text-sm text-slate-400 line-clamp-2 mb-4">
          {restaurant.description || 'Sem descrição informada.'}
        </p>
      </div>

      <div className="text-xs font-medium text-orange-500 group-hover:translate-x-1 transition-transform flex items-center gap-1">
        Ver cardápio →
      </div>
    </Link>
  );
}