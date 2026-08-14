import type { Product } from '../types';
import { Plus } from 'lucide-react';

type ProductCardProps = {
  product: Product;
  onAddToCart?: (product: Product) => void;
};

export function ProductCard({ product, onAddToCart }: ProductCardProps) {
  const formattedPrice = new Intl.NumberFormat('pt-BR', {
    style: 'currency',
    currency: 'BRL',
  }).format(product.price);

  return (
    <div className="bg-slate-900 border border-slate-800 hover:border-slate-700/80 rounded-2xl p-4 flex items-center justify-between gap-4 transition">
      <div className="flex-1 min-w-0">
        <h4 className="text-base font-semibold text-white truncate">
          {product.name}
        </h4>
        <span className="text-sm font-bold text-orange-400 mt-1 block">
          {formattedPrice}
        </span>
      </div>

      <button
        onClick={() => onAddToCart?.(product)}
        className="p-2.5 rounded-xl bg-orange-500/10 border border-orange-500/20 hover:bg-orange-500 text-orange-500 hover:text-white transition group"
        title="Adicionar à sacola"
      >
        <Plus className="w-5 h-5 transition-transform group-hover:scale-110" />
      </button>
    </div>
  );
}