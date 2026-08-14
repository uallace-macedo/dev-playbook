import { useState } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { ArrowLeft, Search, Plus, Utensils, Pencil, Trash2, Loader2, UtensilsCrossed } from 'lucide-react';
import { useRestaurantProducts } from '../hooks/use-restaurant-products';
import { ProductModal } from '../components/product-modal';
import type { Product, CreateProductDTO } from '../types/product';
import { ROUTES } from '@/config/routes';

export function RestaurantProductsPage() {
  const { restaurantId } = useParams<{ restaurantId: string }>();
  const navigate = useNavigate();

  const {
    products,
    isLoading,
    isSubmitting,
    error,
    search,
    setSearch,
    createProduct,
    updateProduct,
    deleteProduct,
  } = useRestaurantProducts(restaurantId || '');

  const [isModalOpen, setIsModalOpen] = useState(false);
  const [editingProduct, setEditingProduct] = useState<Product | null>(null);

  function handleOpenCreate() {
    setEditingProduct(null);
    setIsModalOpen(true);
  }

  function handleOpenEdit(product: Product) {
    setEditingProduct(product);
    setIsModalOpen(true);
  }

  async function handleSubmitModal(data: CreateProductDTO) {
    if (editingProduct) {
      await updateProduct(editingProduct.id, data);
    } else {
      await createProduct(data);
    }
  }

  async function handleDelete(product: Product) {
    if (confirm('Tem certeza que deseja remover este item do cardápio?')) {
      await deleteProduct(product.restaurant_id, product.id);
    }
  }

  return (
    <div className="h-dvh w-full flex flex-col bg-slate-950 text-slate-100 font-sans overflow-hidden">
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
                <Utensils className="w-5 h-5" />
              </div>
              <span className="font-bold text-lg text-white tracking-tight">
                Gestão do<span className="text-orange-500"> Cardápio</span>
              </span>
            </div>
          </div>

          <button
            onClick={handleOpenCreate}
            className="py-2 px-4 bg-orange-500 hover:bg-orange-600 text-white font-semibold rounded-xl transition flex items-center gap-2 text-xs sm:text-sm shadow-lg shadow-orange-500/20"
          >
            <Plus className="w-4 h-4" />
            <span>Novo Item</span>
          </button>
        </div>
      </header>

      <main className="w-full max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8 flex-1 flex flex-col min-h-0 overflow-y-auto no-scrollbar">
        <div className="mb-6 flex flex-col sm:flex-row items-center justify-between gap-4">
          <div className="relative w-full sm:w-80">
            <Search className="w-4 h-4 absolute left-3.5 top-1/2 -translate-y-1/2 text-slate-500" />
            <input
              type="text"
              value={search}
              onChange={(e) => setSearch(e.target.value)}
              placeholder="Buscar item pelo nome..."
              className="w-full pl-10 pr-4 py-2.5 rounded-xl bg-slate-900 border border-slate-800 text-white placeholder-slate-500 focus:outline-none focus:border-orange-500 transition text-sm"
            />
          </div>

          <span className="text-xs font-semibold text-slate-400">
            Total de itens: <strong className="text-white">{products.length}</strong>
          </span>
        </div>

        {isLoading ? (
          <div className="flex-1 flex flex-col items-center justify-center gap-3 py-12">
            <Loader2 className="w-8 h-8 text-orange-500 animate-spin" />
            <p className="text-sm text-slate-400">Carregando cardápio...</p>
          </div>
        ) : products.length === 0 ? (
          <div className="flex-1 flex flex-col items-center justify-center p-8 text-center bg-slate-900/50 border border-dashed border-slate-800 rounded-3xl my-auto max-w-md mx-auto w-full">
            <div className="w-16 h-16 rounded-2xl bg-orange-500/10 border border-orange-500/20 flex items-center justify-center text-orange-500 mb-4">
              <UtensilsCrossed className="w-8 h-8" />
            </div>
            <h2 className="text-xl font-bold text-white mb-2">Nenhum item encontrado</h2>
            <p className="text-sm text-slate-400 mb-6">
              {search
                ? `Nenhum produto bate com a busca "${search}".`
                : 'Seu cardápio ainda está vazio. Comece a adicionar produtos!'}
            </p>
            <button
              onClick={handleOpenCreate}
              className="py-3 px-6 bg-orange-500 hover:bg-orange-600 text-white font-semibold rounded-xl transition flex items-center gap-2 text-sm shadow-lg shadow-orange-500/20"
            >
              <Plus className="w-4 h-4" />
              <span>Adicionar Primeiro Item</span>
            </button>
          </div>
        ) : (
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4 pb-6">
            {products.map((product) => (
              <div
                key={product.id}
                className="bg-slate-900 border border-slate-800 rounded-2xl p-5 shadow-xl flex items-center justify-between gap-4 hover:border-slate-700 transition"
              >
                <div className="min-w-0 flex-1">
                  <h3 className="text-lg font-bold text-white truncate">{product.name}</h3>
                  <p className="text-sm font-semibold text-orange-400 mt-1">
                    {new Intl.NumberFormat('pt-BR', { style: 'currency', currency: 'BRL' }).format(product.price)}
                  </p>
                </div>

                <div className="flex items-center gap-2 shrink-0">
                  <button
                    onClick={() => handleOpenEdit(product)}
                    className="p-2.5 rounded-xl bg-slate-800 hover:bg-slate-700 text-slate-300 hover:text-white border border-slate-700 transition"
                    title="Editar produto"
                  >
                    <Pencil className="w-4 h-4" />
                  </button>
                  <button
                    onClick={() => handleDelete(product)}
                    className="p-2.5 rounded-xl bg-red-500/10 hover:bg-red-500/20 text-red-400 border border-red-500/20 transition"
                    title="Remover produto"
                  >
                    <Trash2 className="w-4 h-4" />
                  </button>
                </div>
              </div>
            ))}
          </div>
        )}
      </main>

      <ProductModal
        isOpen={isModalOpen}
        onClose={() => setIsModalOpen(false)}
        onSubmit={handleSubmitModal}
        isSubmitting={isSubmitting}
        productToEdit={editingProduct}
        error={error}
      />
    </div>
  );
}