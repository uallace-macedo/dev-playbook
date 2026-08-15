import { ShoppingBag, X } from 'lucide-react';

type CartDrawerHeaderProps = {
  onClose: () => void;
};

export function CartDrawerHeader({ onClose }: CartDrawerHeaderProps) {
  return (
    <div className="flex items-center justify-between border-b border-slate-800 pb-4">
      <div className="flex items-center gap-2">
        <div className="p-2 rounded-xl bg-orange-500/10 border border-orange-500/20 text-orange-500">
          <ShoppingBag className="w-5 h-5" />
        </div>
        <h2 className="text-lg font-bold text-white">Seu Carrinho</h2>
      </div>
      <button
        onClick={onClose}
        className="p-2 text-slate-400 hover:text-white rounded-lg hover:bg-slate-800 transition"
      >
        <X className="w-5 h-5" />
      </button>
    </div>
  );
}