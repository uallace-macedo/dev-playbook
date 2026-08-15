import { Loader2 } from 'lucide-react';

type CartDrawerFooterProps = {
  totalAmount: number;
  isDisabled: boolean;
  isSubmitting: boolean;
  onSubmit: () => void;
};

export function CartDrawerFooter({
  totalAmount,
  isDisabled,
  isSubmitting,
  onSubmit,
}: CartDrawerFooterProps) {
  return (
    <div className="border-t border-slate-800 pt-4 space-y-4">
      <div className="flex justify-between items-center">
        <span className="text-xs text-slate-400 font-medium">Total</span>
        <span className="text-xl font-bold text-white">
          {new Intl.NumberFormat('pt-BR', {
            style: 'currency',
            currency: 'BRL',
          }).format(totalAmount)}
        </span>
      </div>

      <button
        onClick={onSubmit}
        disabled={isDisabled || isSubmitting}
        className="w-full py-3.5 px-4 bg-orange-500 hover:bg-orange-600 disabled:opacity-50 disabled:cursor-not-allowed text-white font-bold rounded-xl transition flex items-center justify-center gap-2 text-sm shadow-lg shadow-orange-500/20"
      >
        {isSubmitting ? (
          <>
            <Loader2 className="w-4 h-4 animate-spin" />
            <span>Enviando Pedido...</span>
          </>
        ) : (
          <span>Enviar Pedido para o Restaurante</span>
        )}
      </button>
    </div>
  );
}