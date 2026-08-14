import { useParams, useNavigate } from 'react-router-dom';
import { ArrowLeft, Star } from 'lucide-react';
import { useRestaurantMenu } from '../hook/use-restaurant-menu';
import { CustomerHeader } from '../components/customer-header';
import { ProductCard } from '../components/product-card';

export function RestaurantDetailsPage() {
  const { id } = useParams<{ id: string }>();
  const navigate = useNavigate();

  const {
    restaurant,
    products,
    isLoading,
    error,
    searchTerm,
    page,
    setSearch,
    nextPage,
    prevPage,
  } = useRestaurantMenu(id || '');

  return (
    <div className="h-dvh w-full flex flex-col bg-slate-950 text-slate-100 font-sans overflow-hidden">
      <CustomerHeader />
      <main className="w-full max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 pt-4 pb-4 flex-1 flex flex-col min-h-0">
        <button
          onClick={() => navigate(-1)}
          className="flex items-center gap-2 text-xs font-medium text-slate-400 hover:text-white mb-4 transition w-fit"
        >
          <ArrowLeft className="w-4 h-4" />
          <span>Voltar para restaurantes</span>
        </button>

        {restaurant && (
          <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4 mb-6 pb-6 border-b border-slate-800/80 shrink-0">
            <div>
              <div className="flex items-center gap-3">
                <h1 className="text-2xl sm:text-3xl font-bold text-white">{restaurant.name}</h1>
                <div className="flex items-center gap-1 bg-amber-500/10 border border-amber-500/20 px-2.5 py-0.5 rounded-full text-xs font-semibold text-amber-400">
                  <Star className="w-3.5 h-3.5 fill-amber-400" />
                  <span>{restaurant.rating_average.toFixed(1)}</span>
                  <span className="text-slate-500">({restaurant.total_reviews})</span>
                </div>
              </div>
              <p className="text-xs sm:text-sm text-slate-400 mt-1">
                {restaurant.description || 'Sem descrição informada.'}
              </p>
            </div>

            <div className="relative w-full sm:w-72">
              <input
                type="text"
                value={searchTerm || ''}
                onChange={(e) => setSearch(e.target.value)}
                placeholder="Buscar no cardápio..."
                className="w-full px-4 py-2 rounded-xl bg-slate-900 border border-slate-800 text-white placeholder-slate-500 focus:outline-none focus:border-orange-500 transition text-sm"
              />
            </div>
          </div>
        )}

        {error && (
          <div className="p-3 rounded-xl bg-red-500/10 border border-red-500/30 text-red-400 text-xs sm:text-sm mb-4 shrink-0">
            {error}
          </div>
        )}

        <div className="flex-1 min-h-0 overflow-y-auto no-scrollbar pr-1">
          {isLoading ? (
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4 pb-4">
              {[...Array(6)].map((_, i) => (
                <div key={i} className="h-20 bg-slate-900/50 border border-slate-800/50 rounded-2xl animate-pulse" />
              ))}
            </div>
          ) : products.length === 0 ? (
            <div className="text-center py-16 bg-slate-900/50 border border-slate-800 rounded-2xl">
              <p className="text-slate-400 text-sm">Nenhum produto encontrado neste cardápio.</p>
            </div>
          ) : (
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4 pb-4">
              {products.map((product) => (
                <ProductCard
                  key={product.id}
                  product={product}
                  onAddToCart={(item) => console.log('Adicionou:', item)}
                />
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
            disabled={products.length < 10 || isLoading}
            className="px-4 py-2 bg-slate-900 border border-slate-800 hover:border-slate-700 disabled:opacity-40 disabled:cursor-not-allowed text-xs sm:text-sm text-white rounded-xl transition font-medium"
          >
            Próxima →
          </button>
        </footer>
      </main>
    </div>
  );
}