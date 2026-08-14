import { useState, useEffect, useCallback } from 'react';
import { getMyRestaurants, createRestaurant } from '../services/restaurant-service';
import type { Restaurant } from '../types';

export function useOwnerRestaurant() {
  const [restaurants, setRestaurants] = useState<Restaurant[]>([]);
  const [isLoading, setIsLoading] = useState(true);
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const fetchMyRestaurants = useCallback(async () => {
    try {
      setIsLoading(true);
      setError(null);
      const data = await getMyRestaurants();
      setRestaurants(data.restaurants);
    } catch (err: any) {
      const message = err.response?.data?.detail || 'Erro ao carregar seus restaurantes.';
      setError(message);
    } finally {
      setIsLoading(false);
    }
  }, []);

  useEffect(() => {
    fetchMyRestaurants();
  }, [fetchMyRestaurants]);

  async function handleCreateRestaurant(data: { name: string; description: string }) {
    try {
      setIsSubmitting(true);
      setError(null);
      await createRestaurant(data);
      await fetchMyRestaurants();
    } catch (err: any) {
      const message = err.response?.data?.detail || 'Erro ao cadastrar restaurante.';
      setError(message);
      throw err;
    } finally {
      setIsSubmitting(false);
    }
  }

  return {
    restaurants,
    isLoading,
    isSubmitting,
    error,
    createRestaurant: handleCreateRestaurant,
    refetch: fetchMyRestaurants,
  };
}