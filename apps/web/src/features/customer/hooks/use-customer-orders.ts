import { useState, useEffect, useCallback, useRef } from 'react';
import { api } from '@/lib/api';
import type { CustomerOrder } from '../types/order';

export function useCustomerOrders() {
  const [orders, setOrders] = useState<CustomerOrder[]>([]);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  const ordersRef = useRef<CustomerOrder[]>([]);
  ordersRef.current = orders;

  const fetchOrders = useCallback(async () => {
    try {
      const response = await api.get<{ orders: CustomerOrder[] }>('/api/v1/orders/me');
      setOrders(response.data.orders || []);
      setError(null);
    } catch (err: any) {
      setError(err?.response?.data?.message || 'Erro ao carregar pedidos.');
    } finally {
      setIsLoading(false);
    }
  }, []);

  useEffect(() => {
    fetchOrders();
    const interval = setInterval(fetchOrders, 10000);
    return () => clearInterval(interval);
  }, [fetchOrders]);

  const cancelOrder = async (orderId: string) => {
    try {
      await api.post(`/api/v1/orders/${orderId}/cancel`);
      setOrders((prev) =>
        prev.map((ord) => (ord.id === orderId ? { ...ord, status: 'canceled' } : ord))
      );
      return { success: true };
    } catch (err: any) {
      return {
        success: false,
        message: err?.response?.data?.message || 'Não foi possível cancelar o pedido.',
      };
    }
  };

  const submitReview = async (orderId: string, rating: number, comment: string) => {
    try {
      await api.post(`/api/v1/orders/${orderId}/reviews`, { rating, comment });
      setOrders((prev) =>
        prev.map((ord) => (ord.id === orderId ? { ...ord, reviewed: true } : ord))
      );
      return { success: true };
    } catch (err: any) {
      return {
        success: false,
        message: err?.response?.data?.message || 'Erro ao enviar avaliação.',
      };
    }
  };

  return {
    orders,
    isLoading,
    error,
    refetch: fetchOrders,
    cancelOrder,
    submitReview,
  };
}