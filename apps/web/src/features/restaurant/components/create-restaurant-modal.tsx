import { useState } from 'react';
import { Utensils, Plus, Loader2, X } from 'lucide-react';

type CreateRestaurantModalProps = {
  isOpen: boolean;
  onClose: () => void;
  onSubmit: (data: { name: string; description: string }) => Promise<void>;
  isSubmitting: boolean;
  error?: string | null;
};

export function CreateRestaurantModal({
  isOpen,
  onClose,
  onSubmit,
  isSubmitting,
  error,
}: CreateRestaurantModalProps) {
  const [name, setName] = useState('');
  const [description, setDescription] = useState('');

  if (!isOpen) return null;

  async function handleSubmit(e: React.SubmitEvent) {
    e.preventDefault();
    if (!name.trim()) return;
    await onSubmit({ name: name.trim(), description: description.trim() });
    setName('');
    setDescription('');
    onClose();
  }

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-slate-950/80 backdrop-blur-sm animate-fadeIn">
      <div className="w-full max-w-lg bg-slate-900 border border-slate-800 rounded-2xl p-6 shadow-2xl relative">
        <button
          onClick={onClose}
          className="absolute top-4 right-4 p-2 text-slate-400 hover:text-white rounded-lg hover:bg-slate-800 transition"
        >
          <X className="w-5 h-5" />
        </button>

        <div className="mb-6">
          <div className="w-10 h-10 rounded-xl bg-orange-500/10 border border-orange-500/20 flex items-center justify-center text-orange-500 mb-3">
            <Utensils className="w-5 h-5" />
          </div>
          <h2 className="text-xl font-bold text-white">Novo Restaurante</h2>
          <p className="text-sm text-slate-400 mt-1">
            Cadastre um novo estabelecimento para gerenciar cardápio e pedidos.
          </p>
        </div>

        {error && (
          <div className="p-3.5 rounded-xl bg-red-500/10 border border-red-500/30 text-red-400 text-sm mb-5">
            {error}
          </div>
        )}

        <form onSubmit={handleSubmit} className="space-y-4">
          <div>
            <label className="block text-xs font-semibold text-slate-300 uppercase tracking-wider mb-2">
              Nome do Estabelecimento *
            </label>
            <input
              type="text"
              required
              value={name}
              onChange={(e) => setName(e.target.value)}
              placeholder="Ex: Burger House"
              className="w-full px-4 py-3 rounded-xl bg-slate-950 border border-slate-800 text-white placeholder-slate-500 focus:outline-none focus:border-orange-500 transition text-sm"
            />
          </div>

          <div>
            <label className="block text-xs font-semibold text-slate-300 uppercase tracking-wider mb-2">
              Descrição / Especialidade
            </label>
            <textarea
              rows={3}
              value={description}
              onChange={(e) => setDescription(e.target.value)}
              placeholder="Ex: Hambúrgueres artesanais e porções."
              className="w-full px-4 py-3 rounded-xl bg-slate-950 border border-slate-800 text-white placeholder-slate-500 focus:outline-none focus:border-orange-500 transition text-sm resize-none"
            />
          </div>

          <div className="flex gap-3 pt-2">
            <button
              type="button"
              onClick={onClose}
              className="flex-1 py-3 px-4 bg-slate-800 hover:bg-slate-700 text-slate-300 font-semibold rounded-xl transition text-sm"
            >
              Cancelar
            </button>
            <button
              type="submit"
              disabled={isSubmitting || !name.trim()}
              className="flex-1 py-3 px-4 bg-orange-500 hover:bg-orange-600 disabled:opacity-50 disabled:cursor-not-allowed text-white font-semibold rounded-xl transition flex items-center justify-center gap-2 text-sm shadow-lg shadow-orange-500/20"
            >
              {isSubmitting ? (
                <>
                  <Loader2 className="w-4 h-4 animate-spin" />
                  <span>Criando...</span>
                </>
              ) : (
                <>
                  <Plus className="w-4 h-4" />
                  <span>Cadastrar</span>
                </>
              )}
            </button>
          </div>
        </form>
      </div>
    </div>
  );
}