import { Plus, Minus, Trash2 } from 'lucide-react';
import type { CartItem } from '@/context/cart-context';

type CartItemCardProps = {
  item: CartItem;
  onUpdateQuantity: (productId: string, quantity: number) => void;
  onRemove: (productId: string) => void;
};

export function CartItemCard({ item, onUpdateQuantity, onRemove }: CartItemCardProps) {
  const { product, quantity } = item;

  return (
    <div className="p-3 bg-slate-950 border border-slate-800 rounded-xl flex items-center justify-between gap-3">
      <div className="min-w-0 flex-1">
        <h4 className="text-sm font-bold text-white truncate">{product.name}</h4>
        <p className="text-xs text-orange-400 font-semibold mt-0.5">
          {new Intl.NumberFormat('pt-BR', {
            style: 'currency',
            currency: 'BRL',
          }).format(product.price * quantity)}
        </p>
      </div>

      <div className="flex items-center gap-2">
        <div className="flex items-center bg-slate-900 border border-slate-800 rounded-lg p-1">
          <button
            onClick={() => onUpdateQuantity(product.id, quantity - 1)}
            className="p-1 text-slate-400 hover:text-white transition"
          >
            <Minus className="w-3.5 h-3.5" />
          </button>
          <span className="text-xs font-bold px-2 text-white">{quantity}</span>
          <button
            onClick={() => onUpdateQuantity(product.id, quantity + 1)}
            className="p-1 text-slate-400 hover:text-white transition"
          >
            <Plus className="w-3.5 h-3.5" />
          </button>
        </div>

        <button
          onClick={() => onRemove(product.id)}
          className="p-1.5 text-red-400 hover:bg-red-500/10 rounded-lg transition"
        >
          <Trash2 className="w-4 h-4" />
        </button>
      </div>
    </div>
  );
}