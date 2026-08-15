import { useState } from 'react';
import { Plus, Loader2, UtensilsCrossed } from 'lucide-react';
import { useOwnerRestaurant } from '../hooks/use-owner-restaurant';
import { RestaurantCard } from '../components/restaurant-card';
import { CreateRestaurantModal } from '../components/create-restaurant-modal';
import { RestaurantHeader } from '../components/restaurant-header';

export function RestaurantHomePage() {
  const { restaurants, isLoading, isSubmitting, error, createRestaurant } = useOwnerRestaurant();
  const [isModalOpen, setIsModalOpen] = useState(false);

  return (
    <div className="h-dvh w-full flex flex-col bg-slate-950 text-slate-100 font-sans overflow-hidden">
      <RestaurantHeader onOpenCreateModal={() => setIsModalOpen(true)} />
      <main className="w-full max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8 flex-1 flex flex-col min-h-0 overflow-y-auto no-scrollbar">
        <div className="mb-8 flex flex-col sm:flex-row sm:items-center justify-between gap-4">
          <div>
            <h1 className="text-2xl font-bold text-white">Meus Estabelecimentos 🏪</h1>
            <p className="text-sm text-slate-400 mt-1">
              Selecione um restaurante para gerenciar pedidos e produtos.
            </p>
          </div>
        </div>

        {isLoading ? (
          <div className="flex-1 flex flex-col items-center justify-center gap-3 py-12">
            <Loader2 className="w-8 h-8 text-orange-500 animate-spin" />
            <p className="text-sm text-slate-400">Carregando seus estabelecimentos...</p>
          </div>
        ) : restaurants.length === 0 ? (
          <div className="flex-1 flex flex-col items-center justify-center p-8 text-center bg-slate-900/50 border border-dashed border-slate-800 rounded-3xl my-auto max-w-md mx-auto w-full">
            <div className="w-16 h-16 rounded-2xl bg-orange-500/10 border border-orange-500/20 flex items-center justify-center text-orange-500 mb-4">
              <UtensilsCrossed className="w-8 h-8" />
            </div>
            <h2 className="text-xl font-bold text-white mb-2">Nenhum restaurante cadastrado</h2>
            <p className="text-sm text-slate-400 mb-6">
              Você ainda não possui nenhum estabelecimento. Cadastre seu primeiro restaurante para começar!
            </p>
            <button
              onClick={() => setIsModalOpen(true)}
              className="py-3 px-6 bg-orange-500 hover:bg-orange-600 text-white font-semibold rounded-xl transition flex items-center gap-2 text-sm shadow-lg shadow-orange-500/20"
            >
              <Plus className="w-4 h-4" />
              <span>Cadastrar Primeiro Restaurante</span>
            </button>
          </div>
        ) : (
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6 pb-6">
            {restaurants.map((restaurant) => (
              <RestaurantCard key={restaurant.id} restaurant={restaurant} />
            ))}
          </div>
        )}
      </main>

      <CreateRestaurantModal
        isOpen={isModalOpen}
        onClose={() => setIsModalOpen(false)}
        onSubmit={createRestaurant}
        isSubmitting={isSubmitting}
        error={error}
      />
    </div>
  );
}