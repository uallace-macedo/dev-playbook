import {
  Clock,
  CheckCircle2,
  Truck,
  XCircle,
  Star,
  Loader2,
  AlertTriangle,
  RefreshCw,
  ChevronDown,
  ChevronUp,
} from 'lucide-react';
import { useState } from 'react';
import type { CustomerOrder, OrderStatus } from '../types/order';

interface OrderCardProps {
  order: CustomerOrder;
  cancelingId: string | null;
  onCancel: (orderId: string) => void;
  onReview: (order: CustomerOrder) => void;
}

export function OrderCard({ order, cancelingId, onCancel, onReview }: OrderCardProps) {
  const [showItems, setShowItems] = useState(false);
  const renderStatus = (status: OrderStatus) => {
    const config = {
      created: {
        bg: 'bg-amber-500/10 text-amber-400 border-amber-500/20',
        icon: Clock,
        label: 'Aguardando restaurante',
      },
      accepted: {
        bg: 'bg-blue-500/10 text-blue-400 border-blue-500/20',
        icon: RefreshCw,
        label: 'Em preparo',
      },
      delivering: {
        bg: 'bg-purple-500/10 text-purple-400 border-purple-500/20',
        icon: Truck,
        label: 'Saiu para entrega',
      },
      delivered: {
        bg: 'bg-emerald-500/10 text-emerald-400 border-emerald-500/20',
        icon: CheckCircle2,
        label: 'Entregue',
      },
      canceled: {
        bg: 'bg-red-500/10 text-red-400 border-red-500/20',
        icon: XCircle,
        label: 'Cancelado',
      },
      rejected: {
        bg: 'bg-rose-500/10 text-rose-400 border-rose-500/20',
        icon: AlertTriangle,
        label: 'Recusado',
      },
    }[status];

    const Icon = config.icon;

    return (
      <span className={`inline-flex items-center gap-1.5 px-3 py-1 rounded-full text-xs font-medium border ${config.bg}`}>
        <Icon className={`w-3.5 h-3.5 ${status === 'accepted' ? 'animate-spin' : ''}`} />
        <span>{config.label}</span>
      </span>
    );
  };

  return (
    <div className="bg-slate-900/60 border border-slate-800 hover:border-slate-700/80 rounded-2xl p-4 transition-all space-y-3">
      <div className="flex items-center justify-between gap-3">
        <div>
          <h3 className="font-bold text-base text-white">{order.restaurant.name}</h3>
          <p className="text-[11px] text-slate-500">
            {new Date(order.created_at).toLocaleDateString('pt-BR')} às{' '}
            {new Date(order.created_at).toLocaleTimeString('pt-BR', { hour: '2-digit', minute: '2-digit' })}
          </p>
        </div>
        {renderStatus(order.status)}
      </div>

      <div className="pt-2 border-t border-slate-800/60">
        <button
          onClick={() => setShowItems(!showItems)}
          className="w-full flex items-center justify-between text-xs text-slate-400 hover:text-slate-200 transition py-1"
        >
          <span>{order.items.reduce((acc, item) => acc + item.quantity, 0)} itens no pedido</span>
          <span className="flex items-center gap-1 text-[11px] text-orange-400 font-medium">
            {showItems ? 'Ocultar detalhes' : 'Ver detalhes'}
            {showItems ? <ChevronUp className="w-3.5 h-3.5" /> : <ChevronDown className="w-3.5 h-3.5" />}
          </span>
        </button>

        {showItems && (
          <div className="mt-2 space-y-1.5 pl-2 border-l-2 border-slate-800 py-1">
            {order.items.map((item) => (
              <div key={item.id} className="flex justify-between text-xs text-slate-300">
                <span>
                  <strong className="text-orange-400 font-semibold mr-1.5">{item.quantity}x</strong>
                  {item.product_name}
                </span>
                <span className="text-slate-500">
                  {new Intl.NumberFormat('pt-BR', { style: 'currency', currency: 'BRL' }).format(item.subtotal)}
                </span>
              </div>
            ))}
          </div>
        )}
      </div>

      <div className="flex items-center justify-between pt-2 border-t border-slate-800/60">
        <div>
          <span className="text-[10px] text-slate-500 uppercase tracking-wider block">Total</span>
          <span className="text-sm font-bold text-white">
            {new Intl.NumberFormat('pt-BR', { style: 'currency', currency: 'BRL' }).format(order.total_price)}
          </span>
        </div>

        {order.status === 'created' && (
          <button
            onClick={() => onCancel(order.id)}
            disabled={cancelingId === order.id}
            className="px-3 py-1.5 bg-red-500/10 hover:bg-red-500/20 text-red-400 border border-red-500/20 rounded-xl text-xs font-semibold transition flex items-center gap-1.5 disabled:opacity-50"
          >
            {cancelingId === order.id ? <Loader2 className="w-3.5 h-3.5 animate-spin" /> : <XCircle className="w-3.5 h-3.5" />}
            <span>Cancelar</span>
          </button>
        )}

        {order.status === 'delivered' && !order.reviewed && (
          <button
            onClick={() => onReview(order)}
            className="px-3 py-1.5 bg-amber-500 hover:bg-amber-600 text-slate-950 font-bold rounded-xl text-xs transition flex items-center gap-1.5"
          >
            <Star className="w-3.5 h-3.5 fill-slate-950" />
            <span>Avaliar</span>
          </button>
        )}

        {order.status === 'delivered' && order.reviewed && (
          <span className="text-[11px] text-emerald-400 font-medium flex items-center gap-1">
            <CheckCircle2 className="w-3.5 h-3.5" />
            Avaliado
          </span>
        )}
      </div>
    </div>
  );
}