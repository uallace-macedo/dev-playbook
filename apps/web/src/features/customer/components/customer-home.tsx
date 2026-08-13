import { useRestaurants } from '../hook/use-restaurants';
import { RestaurantCard } from './restaurant-card';

export function CustomerHome() {
  const {
    restaurants,
    isLoading,
    error,
    searchTerm,
    page,
    setSearch,
    nextPage,
    prevPage,
  } = useRestaurants();

  return (
    <div className="w-full max-w-6xl mx-auto px-4 py-8">
      <div className="flex flex-col md:flex-row md:items-center justify-between gap-4 mb-8">
        <div>
          <h1 className="text-3xl font-bold text-white">Restaurantes 🍽️</h1>
          <p className="text-sm text-slate-400 mt-1">
            Encontre os melhores estabelecimentos da sua região
          </p>
        </div>

        <div className="w-full md:w-80">
          <input
            type="text"
            value={searchTerm}
            onChange={(e) => setSearch(e.target.value)}
            placeholder="Buscar por nome..."
            className="w-full px-4 py-2.5 rounded-xl bg-slate-900 border border-slate-800 text-white placeholder-slate-500 focus:outline-none focus:border-orange-500 transition text-sm"
          />
        </div>
      </div>

      {error && (
        <div className="p-4 rounded-xl bg-red-500/10 border border-red-500/30 text-red-400 text-sm mb-6">
          {error}
        </div>
      )}

      {isLoading ? (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
          {[...Array(6)].map((_, i) => (
            <div key={i} className="h-40 bg-slate-900/50 border border-slate-800/50 rounded-2xl animate-pulse" />
          ))}
        </div>
      ) : restaurants.length === 0 ? (
        <div className="text-center py-16 bg-slate-900/50 border border-slate-800 rounded-2xl">
          <p className="text-slate-400">Nenhum restaurante encontrado.</p>
        </div>
      ) : (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4 mb-8">
          {restaurants.map((restaurant) => (
            <RestaurantCard key={restaurant.id} restaurant={restaurant} />
          ))}
        </div>
      )}

      <div className="flex items-center justify-between pt-4 border-t border-slate-800">
        <button
          onClick={prevPage}
          disabled={page === 0 || isLoading}
          className="px-4 py-2 bg-slate-900 border border-slate-800 hover:border-slate-700 disabled:opacity-40 disabled:cursor-not-allowed text-sm text-white rounded-lg transition"
        >
          ← Anterior
        </button>

        <span className="text-xs text-slate-400 font-medium">
          Página {page + 1}
        </span>

        <button
          onClick={nextPage}
          disabled={restaurants.length < 10 || isLoading}
          className="px-4 py-2 bg-slate-900 border border-slate-800 hover:border-slate-700 disabled:opacity-40 disabled:cursor-not-allowed text-sm text-white rounded-lg transition"
        >
          Próxima →
        </button>
      </div>
    </div>
  );
}