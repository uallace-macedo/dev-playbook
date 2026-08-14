import { CheckCircle2, XCircle, Truck, Loader2, Utensils } from 'lucide-react';
import type { Order, OrderStatus } from '../types/order';

type OrderCardProps = {
  order: Order;
  onStatusChange: (orderId: string, newStatus: OrderStatus) => Promise<void>;
  isUpdating: boolean;
};

type BadgeConfig = {
  label: string;
  bg: string;
};

const STATUS_BADGES: Record<string, BadgeConfig> = {
  created: {
    label: 'Pendente',
    bg: 'bg-amber-500/10 border-amber-500/30 text-amber-400',
  },
  accepted: {
    label: 'Em Preparo',
    bg: 'bg-blue-500/10 border-blue-500/30 text-blue-400',
  },
  delivered: {
    label: 'Entregue',
    bg: 'bg-emerald-500/10 border-emerald-500/30 text-emerald-400',
  },
  rejected: {
    label: 'Recusado',
    bg: 'bg-red-500/10 border-red-500/30 text-red-400',
  },
};

export function OrderCard({ order, onStatusChange, isUpdating }: OrderCardProps) {
  const statusBadge = STATUS_BADGES[order.status] ?? {
    label: order.status,
    bg: 'bg-slate-800 border-slate-700 text-slate-300',
  };

  const calculatedTotal =
    order.total_price ??
    order.items?.reduce((acc, item) => acc + (item.unit_price || 0) * item.quantity, 0) ??
    0;

  return (
    <div className="bg-slate-900 border border-slate-800 rounded-2xl p-5 shadow-xl flex flex-col justify-between hover:border-slate-700 transition">
      <div>
        <div className="flex items-center justify-between gap-2 pb-3 mb-4 border-b border-slate-800">
          <div>
            <span className="text-xs text-slate-500 font-mono">
              #{order.id.slice(0, 8)}
            </span>
            {order.customer_name && (
              <h4 className="text-sm font-bold text-white mt-0.5">
                {order.customer_name}
              </h4>
            )}
          </div>
          <span
            className={`text-xs font-bold px-2.5 py-1 rounded-full border uppercase tracking-wider ${statusBadge.bg}`}
          >
            {statusBadge.label}
          </span>
        </div>

        <div className="space-y-2 mb-6">
          <p className="text-xs font-semibold text-slate-400 uppercase tracking-wider flex items-center gap-1.5">
            <Utensils className="w-3.5 h-3.5" />
            Itens do Pedido
          </p>
          <ul className="space-y-1.5 pl-1">
            {order.items?.map((item) => (
              <li
                key={item.id || item.product_id}
                className="text-sm text-slate-200 flex justify-between items-center"
              >
                <span>
                  <strong className="text-orange-400 mr-2">{item.quantity}x</strong>
                  {item.product_name || `Produto #${item.product_id.slice(0, 5)}`}
                </span>
                {item.unit_price ? (
                  <span className="text-xs text-slate-400">
                    {new Intl.NumberFormat('pt-BR', {
                      style: 'currency',
                      currency: 'BRL',
                    }).format(item.unit_price * item.quantity)}
                  </span>
                ) : null}
              </li>
            ))}
          </ul>
        </div>
      </div>

      <div className="pt-4 border-t border-slate-800 flex flex-col gap-3">
        <div className="flex justify-between items-center">
          <span className="text-xs font-medium text-slate-400">Total do Pedido</span>
          <span className="text-lg font-bold text-white">
            {new Intl.NumberFormat('pt-BR', {
              style: 'currency',
              currency: 'BRL',
            }).format(calculatedTotal)}
          </span>
        </div>

        {isUpdating ? (
          <div className="py-2.5 bg-slate-950/50 rounded-xl flex items-center justify-center gap-2 text-slate-400 text-xs">
            <Loader2 className="w-4 h-4 animate-spin text-orange-500" />
            <span>Atualizando status...</span>
          </div>
        ) : (
          <div className="flex items-center gap-2">
            {order.status === 'created' && (
              <>
                <button
                  onClick={() => onStatusChange(order.id, 'rejected')}
                  className="flex-1 py-2 px-3 bg-red-500/10 hover:bg-red-500/20 text-red-400 border border-red-500/20 rounded-xl text-xs font-bold transition flex items-center justify-center gap-1.5"
                >
                  <XCircle className="w-4 h-4" />
                  <span>Recusar</span>
                </button>
                <button
                  onClick={() => onStatusChange(order.id, 'accepted')}
                  className="flex-1 py-2.5 px-3 bg-orange-500 hover:bg-orange-600 text-white font-bold rounded-xl text-xs transition flex items-center justify-center gap-1.5 shadow-md shadow-orange-500/20"
                >
                  <CheckCircle2 className="w-4 h-4" />
                  <span>Aceitar</span>
                </button>
              </>
            )}

            {order.status === 'accepted' && (
              <button
                onClick={() => onStatusChange(order.id, 'delivered')}
                className="w-full py-2.5 px-3 bg-emerald-600 hover:bg-emerald-500 text-white font-bold rounded-xl text-xs transition flex items-center justify-center gap-2 shadow-md shadow-emerald-600/20"
              >
                <Truck className="w-4 h-4" />
                <span>Marcar como Entregue</span>
              </button>
            )}

            {(order.status === 'delivered' || order.status === 'rejected') && (
              <div className="w-full py-2 text-center text-xs text-slate-500 font-medium bg-slate-950/40 rounded-xl border border-slate-800/50">
                Pedido Finalizado
              </div>
            )}
          </div>
        )}
      </div>
    </div>
  );
}