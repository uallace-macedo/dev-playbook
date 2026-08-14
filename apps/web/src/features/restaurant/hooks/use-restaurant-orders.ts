import { useState, useEffect, useCallback } from 'react';
import { getRestaurantOrders, updateOrderStatus } from '../services/order-service';
import type { Order, OrderStatus } from '../types/order';

export function useRestaurantOrders(restaurantId: string) {
  const [orders, setOrders] = useState<Order[]>([]);
  const [isLoading, setIsLoading] = useState(true);
  const [updatingOrderId, setUpdatingOrderId] = useState<string | null>(null);
  const [error, setError] = useState<string | null>(null);

  const fetchOrders = useCallback(async () => {
    if (!restaurantId) return;
    try {
      setError(null);
      const data = await getRestaurantOrders(restaurantId);
      setOrders(data.orders || []);
    } catch (err: any) {
      const message = err.response?.data?.detail || 'Erro ao carregar pedidos.';
      setError(message);
    } finally {
      setIsLoading(false);
    }
  }, [restaurantId]);

  useEffect(() => {
    fetchOrders();
    const interval = setInterval(() => {
      fetchOrders();
    }, 10000);

    return () => clearInterval(interval);
  }, [fetchOrders]);

  async function handleStatusChange(orderId: string, newStatus: OrderStatus) {
    try {
      setUpdatingOrderId(orderId);
      setError(null);
      await updateOrderStatus(orderId, newStatus);
      await fetchOrders();
    } catch (err: any) {
      const message = err.response?.data?.detail || 'Erro ao atualizar status do pedido.';
      setError(message);
    } finally {
      setUpdatingOrderId(null);
    }
  }

  return {
    orders,
    isLoading,
    updatingOrderId,
    error,
    changeStatus: handleStatusChange,
    refetch: fetchOrders,
  };
}
