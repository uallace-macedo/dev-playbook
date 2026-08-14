import { useCallback, useEffect, useState } from "react";
import type { Restaurant } from "../types";
import { getRestaurants } from "../services/customer-service";
import { useDebounce } from "@/hooks/use-debounce";

const PAGE_SIZE = 10;

export function useRestaurants() {
  const [restaurants, setRestaurants] = useState<Restaurant[]>([]);
  const [isLoading, setIsLoading] = useState<boolean>(true);
  const [error, setError] = useState<string | null>(null);
  
  const [page, setPage] = useState<number>(0);
  const [searchTerm, setSearchTerm] = useState<string>('');
  
  const debouncedSearch = useDebounce(searchTerm, 400);

  const fetchRestaurants = useCallback(async () => {
    try {
      setIsLoading(true);
      setError(null);

      const data = await getRestaurants({
        limit: PAGE_SIZE,
        offset: page * PAGE_SIZE,
        name: debouncedSearch || undefined,
      });
  
      setRestaurants(data.restaurants);
    } catch (err: any) {
      const message = err.response?.data?.detail || 'Erro ao carregar restaurantes';
      setError(message);
    } finally {
      setIsLoading(false);
    }
  }, [page, debouncedSearch]);

  useEffect(() => {
    fetchRestaurants();
  }, [fetchRestaurants])

  function handleSearch(term: string) {
    setSearchTerm(term);
    setPage(0);
  }

  return {
    restaurants,
    isLoading,
    error,
    searchTerm,
    page,

    setSearch: handleSearch,
    nextPage: () => setPage((prev) => prev + 1),
    prevPage: () => setPage((prev) => Math.max(prev - 1, 0)),
    refetch: fetchRestaurants,
  }
}