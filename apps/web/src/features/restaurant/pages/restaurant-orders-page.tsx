import { useState } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { ArrowLeft, ClipboardList, Loader2, RefreshCw } from 'lucide-react';
import { useRestaurantOrders } from '../hooks/use-restaurant-orders';
import { OrderCard } from '../components/order-card';
import type { OrderStatus } from '../types/order';
import { ROUTES } from '@/config/routes';

export function RestaurantOrdersPage() {
  const { restaurantId } = useParams<{ restaurantId: string }>();
  const navigate = useNavigate();
  
  const { orders, isLoading, updatingOrderId, error, changeStatus, refetch } =
    useRestaurantOrders(restaurantId || '');

  const [activeTab, setActiveTab] = useState<'all' | OrderStatus>('all');

  const filteredOrders = orders.filter((order) => {
    if (activeTab === 'all') return true;
    return order.status === activeTab;
  });

  return (
    <div className="h-dvh w-full flex flex-col bg-slate-950 text-slate-100 font-sans overflow-hidden">
      
      {/* Header */}
      <header className="border-b border-slate-800/80 bg-slate-950/80 backdrop-blur-md shrink-0">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 h-16 flex items-center justify-between gap-4">
          <div className="flex items-center gap-3">
            <button
              onClick={() => navigate(ROUTES.RESTAURANT.HOME)}
              className="p-2 rounded-xl bg-slate-900 border border-slate-800 text-slate-400 hover:text-white hover:bg-slate-800 transition"
              title="Voltar aos restaurantes"
            >
              <ArrowLeft className="w-5 h-5" />
            </button>

            <div className="flex items-center gap-2">
              <div className="p-2 rounded-xl bg-orange-500/10 border border-orange-500/20 text-orange-500">
                <ClipboardList className="w-5 h-5" />
              </div>
              <span className="font-bold text-lg text-white tracking-tight">
                Gestão de<span className="text-orange-500"> Pedidos</span>
              </span>
            </div>
          </div>

          <button
            onClick={() => refetch()}
            className="p-2.5 bg-slate-900 hover:bg-slate-800 border border-slate-800 text-slate-300 hover:text-white rounded-xl transition flex items-center gap-2 text-xs font-semibold"
            title="Atualizar pedidos"
          >
            <RefreshCw className="w-4 h-4 text-orange-500" />
            <span className="hidden sm:inline">Atualizar</span>
          </button>
        </div>
      </header>

      <main className="w-full max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8 flex-1 flex flex-col min-h-0 overflow-y-auto no-scrollbar">
        <div className="flex items-center gap-2 border-b border-slate-800 pb-4 mb-6 overflow-x-auto no-scrollbar">
          {[
            { id: 'all', label: 'Todos', count: orders.length },
            {
              id: 'created',
              label: 'Pendentes',
              count: orders.filter((o) => o.status === 'created').length,
            },
            {
              id: 'accepted',
              label: 'Em Preparo',
              count: orders.filter((o) => o.status === 'accepted').length,
            },
            {
              id: 'delivered',
              label: 'Entregues',
              count: orders.filter((o) => o.status === 'delivered').length,
            },
          ].map((tab) => (
            <button
              key={tab.id}
              onClick={() => setActiveTab(tab.id as any)}
              className={`py-2 px-4 rounded-xl text-xs font-bold transition flex items-center gap-2 whitespace-nowrap ${
                activeTab === tab.id
                  ? 'bg-orange-500 text-white shadow-lg shadow-orange-500/20'
                  : 'bg-slate-900 text-slate-400 hover:text-white border border-slate-800'
              }`}
            >
              <span>{tab.label}</span>
              <span
                className={`px-1.5 py-0.5 rounded-md text-[10px] ${
                  activeTab === tab.id ? 'bg-orange-600 text-white' : 'bg-slate-800 text-slate-400'
                }`}
              >
                {tab.count}
              </span>
            </button>
          ))}
        </div>

        {error && (
          <div className="p-4 rounded-xl bg-red-500/10 border border-red-500/30 text-red-400 text-sm mb-6">
            {error}
          </div>
        )}

        {isLoading ? (
          <div className="flex-1 flex flex-col items-center justify-center gap-3 py-12">
            <Loader2 className="w-8 h-8 text-orange-500 animate-spin" />
            <p className="text-sm text-slate-400">Buscando pedidos do restaurante...</p>
          </div>
        ) : filteredOrders.length === 0 ? (
          <div className="flex-1 flex flex-col items-center justify-center p-8 text-center bg-slate-900/50 border border-dashed border-slate-800 rounded-3xl my-auto max-w-md mx-auto w-full">
            <div className="w-16 h-16 rounded-2xl bg-orange-500/10 border border-orange-500/20 flex items-center justify-center text-orange-500 mb-4">
              <ClipboardList className="w-8 h-8" />
            </div>
            <h2 className="text-xl font-bold text-white mb-2">Nenhum pedido aqui</h2>
            <p className="text-sm text-slate-400">
              Não há nenhum pedido na categoria selecionada no momento.
            </p>
          </div>
        ) : (
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6 pb-6">
            {filteredOrders.map((order) => (
              <OrderCard
                key={order.id}
                order={order}
                onStatusChange={changeStatus}
                isUpdating={updatingOrderId === order.id}
              />
            ))}
          </div>
        )}
      </main>
    </div>
  );
}