import { useState } from 'react';
import { RefreshCw, ShoppingBag, Loader2, Clock, CheckCircle2 } from 'lucide-react';
import { CustomerHeader } from '../components/customer-header';
import { useCustomerOrders } from '../hooks/use-customer-orders';
import type { CustomerOrder } from '../types/order';
import { ReviewModal } from '../components/review-modal';
import { OrderCard } from '../components/order-card';

export function CustomerOrdersPage() {
  const { orders, isLoading, error, refetch, cancelOrder, submitReview } = useCustomerOrders();
  const [activeTab, setActiveTab] = useState<'active' | 'history'>('active');
  const [selectedOrderForReview, setSelectedOrderForReview] = useState<CustomerOrder | null>(null);
  const [cancelingId, setCancelingId] = useState<string | null>(null);

  const activeOrders = orders.filter((o) => ['created', 'accepted', 'delivering'].includes(o.status));
  const historyOrders = orders.filter((o) => ['delivered', 'canceled', 'rejected'].includes(o.status));

  const displayedOrders = activeTab === 'active' ? activeOrders : historyOrders;

  const handleCancel = async (orderId: string) => {
    if (!confirm('Tem certeza que deseja cancelar este pedido?')) return;
    setCancelingId(orderId);
    const result = await cancelOrder(orderId);
    if (!result.success) alert(result.message);
    setCancelingId(null);
  };

  return (
    <div className="h-dvh w-full flex flex-col bg-slate-950 text-slate-100 font-sans overflow-hidden">
      <CustomerHeader />

      <main className="w-full max-w-3xl mx-auto px-4 py-6 flex-1 flex flex-col min-h-0">
        <div className="flex items-center justify-between mb-4 shrink-0">
          <div>
            <h1 className="text-xl font-bold text-white">Meus Pedidos</h1>
            <p className="text-xs text-slate-400">Acompanhe suas refeições em tempo real</p>
          </div>
          <button
            onClick={() => refetch()}
            className="p-2 bg-slate-900 border border-slate-800 hover:border-slate-700 text-slate-400 hover:text-white rounded-xl transition"
            title="Atualizar"
          >
            <RefreshCw className={`w-4 h-4 ${isLoading ? 'animate-spin text-orange-500' : ''}`} />
          </button>
        </div>

        <div className="flex bg-slate-900/80 p-1 rounded-xl border border-slate-800/80 mb-5 shrink-0">
          <button
            onClick={() => setActiveTab('active')}
            className={`flex-1 flex items-center justify-center gap-2 py-2 text-xs font-bold rounded-lg transition ${
              activeTab === 'active'
                ? 'bg-orange-500 text-white shadow-lg shadow-orange-500/20'
                : 'text-slate-400 hover:text-slate-200'
            }`}
          >
            <Clock className="w-3.5 h-3.5" />
            <span>Em Andamento ({activeOrders.length})</span>
          </button>

          <button
            onClick={() => setActiveTab('history')}
            className={`flex-1 flex items-center justify-center gap-2 py-2 text-xs font-bold rounded-lg transition ${
              activeTab === 'history'
                ? 'bg-orange-500 text-white shadow-lg shadow-orange-500/20'
                : 'text-slate-400 hover:text-slate-200'
            }`}
          >
            <CheckCircle2 className="w-3.5 h-3.5" />
            <span>Histórico ({historyOrders.length})</span>
          </button>
        </div>

        {error && (
          <div className="p-3 rounded-xl bg-red-500/10 border border-red-500/20 text-red-400 text-xs mb-4 shrink-0">
            {error}
          </div>
        )}

        <div className="flex-1 min-h-0 overflow-y-auto space-y-3 pr-1 no-scrollbar">
          {isLoading && orders.length === 0 ? (
            <div className="flex flex-col items-center justify-center py-16 text-slate-500">
              <Loader2 className="w-6 h-6 text-orange-500 animate-spin mb-2" />
              <span className="text-xs">Buscando pedidos...</span>
            </div>
          ) : displayedOrders.length === 0 ? (
            <div className="text-center py-16 bg-slate-900/30 border border-slate-800/60 rounded-2xl flex flex-col items-center justify-center">
              <ShoppingBag className="w-10 h-10 text-slate-700 mb-2" />
              <p className="text-xs font-semibold text-slate-400">
                {activeTab === 'active' ? 'Nenhum pedido em andamento' : 'Seu histórico está vazio'}
              </p>
            </div>
          ) : (
            displayedOrders.map((order) => (
              <OrderCard
                key={order.id}
                order={order}
                cancelingId={cancelingId}
                onCancel={handleCancel}
                onReview={setSelectedOrderForReview}
              />
            ))
          )}
        </div>
      </main>

      {selectedOrderForReview && (
        <ReviewModal
          isOpen={!!selectedOrderForReview}
          onClose={() => setSelectedOrderForReview(null)}
          restaurantName={selectedOrderForReview.restaurant.name}
          onSubmit={(rating, comment) => submitReview(selectedOrderForReview.id, rating, comment)}
        />
      )}
    </div>
  );
}