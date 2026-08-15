import { CheckCircle2 } from 'lucide-react';
import { useCartDrawer } from '@/features/customer/hooks/use-cart-drawer';
import { CartDrawerHeader } from './cart-drawer-header';
import { CartItemCard } from './cart-item-card';
import { CartDrawerFooter } from './cart-drawer-footer';

type CartDrawerProps = {
  isOpen: boolean;
  onClose: () => void;
  onOrderCreated?: () => void;
};

export function CartDrawer({ isOpen, onClose, onOrderCreated }: CartDrawerProps) {
  const {
    items,
    totalAmount,
    isSubmitting,
    error,
    success,
    updateQuantity,
    removeFromCart,
    handleCheckout,
  } = useCartDrawer(onClose, onOrderCreated);

  if (!isOpen) return null;

  return (
    <div className="fixed inset-0 z-50 flex justify-end bg-slate-950/80 backdrop-blur-sm animate-fadeIn">
      <div className="w-full max-w-md bg-slate-900 border-l border-slate-800 h-full flex flex-col justify-between shadow-2xl p-6 relative">
        <CartDrawerHeader onClose={onClose} />

        {success ? (
          <div className="flex-1 flex flex-col items-center justify-center p-6 text-center">
            <div className="w-16 h-16 rounded-full bg-emerald-500/10 border border-emerald-500/20 text-emerald-500 flex items-center justify-center mb-4">
              <CheckCircle2 className="w-8 h-8" />
            </div>
            <h3 className="text-xl font-bold text-white mb-2">Pedido Enviado!</h3>
            <p className="text-xs text-slate-400">
              O restaurante recebeu seu pedido e iniciará o preparo em breve.
            </p>
          </div>
        ) : (
          <>
            <div className="flex-1 overflow-y-auto my-4 space-y-3 no-scrollbar pr-1">
              {error && (
                <div className="p-3 rounded-xl bg-red-500/10 border border-red-500/30 text-red-400 text-xs mb-3">
                  {error}
                </div>
              )}

              {items.length === 0 ? (
                <div className="h-full flex flex-col items-center justify-center text-center p-6">
                  <p className="text-sm text-slate-400">Seu carrinho está vazio.</p>
                </div>
              ) : (
                items.map((item) => (
                  <CartItemCard
                    key={item.product.id}
                    item={item}
                    onUpdateQuantity={updateQuantity}
                    onRemove={removeFromCart}
                  />
                ))
              )}
            </div>

            <CartDrawerFooter
              totalAmount={totalAmount}
              isDisabled={items.length === 0}
              isSubmitting={isSubmitting}
              onSubmit={handleCheckout}
            />
          </>
        )}
      </div>
    </div>
  );
}