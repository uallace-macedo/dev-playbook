import { useRestaurants } from '../hooks/use-restaurants';
import { RestaurantCard } from '../components/restaurant-card';
import { CustomerHeader } from '../components/customer-header';

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
    <div className="h-dvh w-screen bg-slate-950 flex flex-col text-slate-100 font-sans overflow-hidden">      
      <CustomerHeader />

      <main className="w-full max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 pt-6 pb-4 flex-1 flex flex-col min-h-0">
        <div className="flex flex-col gap-4 mb-6 shrink-0">
          <div>
            <h1 className="text-2xl sm:text-3xl font-bold text-white">Restaurantes 🍽️</h1>
            <p className="text-xs sm:text-sm text-slate-400 mt-1">
              Encontre os melhores estabelecimentos da sua região
            </p>
          </div>

          <div className="relative w-full max-w-lg">
            <input
              type="text"
              value={searchTerm || ''}
              onChange={(e) => setSearch(e.target.value)}
              placeholder="Buscar restaurante por nome..."
              className="w-full px-4 py-2.5 sm:py-3 rounded-xl bg-slate-900 border border-slate-800 text-white placeholder-slate-500 focus:outline-none focus:border-orange-500 transition text-sm shadow-sm"
            />
          </div>
        </div>

        {error && (
          <div className="p-3 rounded-xl bg-red-500/10 border border-red-500/30 text-red-400 text-xs sm:text-sm mb-4 shrink-0">
            {error}
          </div>
        )}

        <div className="flex-1 min-h-0 overflow-y-auto no-scrollbar pr-1">
          {isLoading ? (
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4 pb-4">
              {[...Array(6)].map((_, i) => (
                <div key={i} className="h-36 bg-slate-900/50 border border-slate-800/50 rounded-2xl animate-pulse" />
              ))}
            </div>
          ) : restaurants.length === 0 ? (
            <div className="text-center py-12 bg-slate-900/50 border border-slate-800 rounded-2xl">
              <p className="text-slate-400 text-sm">Nenhum restaurante encontrado.</p>
            </div>
          ) : (
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4 pb-4">
              {restaurants.map((restaurant) => (
                <RestaurantCard key={restaurant.id} restaurant={restaurant} />
              ))}
            </div>
          )}
        </div>

        <footer className="flex items-center justify-between pt-4 mt-2 border-t border-slate-800/80 shrink-0">
          <button
            onClick={prevPage}
            disabled={page === 0 || isLoading}
            className="px-4 py-2 bg-slate-900 border border-slate-800 hover:border-slate-700 disabled:opacity-40 disabled:cursor-not-allowed text-xs sm:text-sm text-white rounded-xl transition font-medium"
          >
            ← Anterior
          </button>

          <span className="text-xs text-slate-400 font-medium tracking-wide">
            Página <strong className="text-white">{page + 1}</strong>
          </span>

          <button
            onClick={nextPage}
            disabled={restaurants.length < 10 || isLoading}
            className="px-4 py-2 bg-slate-900 border border-slate-800 hover:border-slate-700 disabled:opacity-40 disabled:cursor-not-allowed text-xs sm:text-sm text-white rounded-xl transition font-medium"
          >
            Próxima →
          </button>
        </footer>
      </main>
    </div>
  );
}