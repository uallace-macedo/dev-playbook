import { useState, useEffect, useCallback } from 'react';
import {
  getRestaurantProducts,
  createProduct,
  updateProduct,
  deleteProduct,
} from '../services/product-service';
import type { Product, CreateProductDTO, UpdateProductDTO } from '../types/product';

export function useRestaurantProducts(restaurantId: string) {
  const [products, setProducts] = useState<Product[]>([]);
  const [isLoading, setIsLoading] = useState(true);
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [search, setSearch] = useState('');

  const fetchProducts = useCallback(async () => {
    if (!restaurantId) return;
    try {
      setIsLoading(true);
      setError(null);
      const data = await getRestaurantProducts(restaurantId, { name: search || undefined });
      setProducts(data.products || []);
    } catch (err: any) {
      const message = err.response?.data?.detail || 'Erro ao carregar cardápio.';
      setError(message);
    } finally {
      setIsLoading(false);
    }
  }, [restaurantId, search]);

  useEffect(() => {
    fetchProducts();
  }, [fetchProducts]);

  async function handleCreateProduct(data: CreateProductDTO) {
    try {
      setIsSubmitting(true);
      setError(null);
      await createProduct(restaurantId, data);
      await fetchProducts();
    } catch (err: any) {
      const message = err.response?.data?.detail || 'Erro ao criar produto.';
      setError(message);
      throw err;
    } finally {
      setIsSubmitting(false);
    }
  }

  async function handleUpdateProduct(productId: string, data: UpdateProductDTO) {
    try {
      setIsSubmitting(true);
      setError(null);
      await updateProduct(restaurantId, productId, data);
      await fetchProducts();
    } catch (err: any) {
      const message = err.response?.data?.detail || 'Erro ao atualizar produto.';
      setError(message);
      throw err;
    } finally {
      setIsSubmitting(false);
    }
  }

  async function handleDeleteProduct(restaurant_id: string, productId: string) {
    try {
      setIsSubmitting(true);
      setError(null);
      await deleteProduct(restaurant_id, productId);
      await fetchProducts();
    } catch (err: any) {
      const message = err.response?.data?.detail || 'Erro ao excluir produto.';
      setError(message);
      throw err;
    } finally {
      setIsSubmitting(false);
    }
  }

  return {
    products,
    isLoading,
    isSubmitting,
    error,
    search,
    setSearch,
    createProduct: handleCreateProduct,
    updateProduct: handleUpdateProduct,
    deleteProduct: handleDeleteProduct,
    refetch: fetchProducts,
  };
}