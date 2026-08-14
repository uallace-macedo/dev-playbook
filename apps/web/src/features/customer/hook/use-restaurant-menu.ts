import { useCallback, useEffect, useState } from "react";
import type { Product, Restaurant } from "../types";
import { useDebounce } from "@/hooks/use-debounce";
import { getRestaurantByIdRequest, getRestaurantProductsRequest } from "../services/customer-service";

const PAGE_SIZE = 10;

export function useRestaurantMenu(restaurantId: string) {
  const [restaurant, setRestaurant] = useState<Restaurant | null>(null);
  const [products, setProducts] = useState<Product[]>([]);
  const [isLoading, setIsLoading] = useState<boolean>(false);
  const [error, setError] = useState<string | null>(null);

  const [searchTerm, setSearchTerm] = useState('');
  const [page, setPage] = useState(0);

  const debouncedSearch = useDebounce(searchTerm, 400);

  useEffect(() => {
    async function loadRestaurant() {
      try {
        const data = await getRestaurantByIdRequest(restaurantId);
        setRestaurant(data);
      } catch (error: any) {
        setError('Não foi possível carregar as informações do restaurante.');
      }
    }

    if (restaurantId) loadRestaurant();
  }, [restaurantId]);

  const fetchProducts = useCallback(async () => {
    if (!restaurantId) return;

    try {
      setIsLoading(true);
      setError(null);

      const data = await getRestaurantProductsRequest(restaurantId, {
        limit: PAGE_SIZE,
        offset: page * PAGE_SIZE,
        name: debouncedSearch.trim() !== '' ? debouncedSearch : undefined
      });

      setProducts(data.products);
    } catch (error: any) {
      setError('Erro ao carregar o cardápio.');
    } finally {
      setIsLoading(false);
    }
  }, [restaurantId, page, debouncedSearch]);

  useEffect(() => {
    fetchProducts()
  }, [fetchProducts]);

  function handleSearch(term: string) {
    setSearchTerm(term);
    setPage(0);
  }

  return {
    restaurant,
    products,
    isLoading,
    error,
    searchTerm,
    page,
    setSearch: handleSearch,
    nextPage: () => setPage(prev => prev + 1),
    prevPage: () => setPage(prev => Math.max(0, prev - 1)),
  }
}