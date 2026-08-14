import { api } from '@/lib/api';
import type { GetOrdersResponse, Order, OrderStatus } from '../types/order';

export async function getRestaurantOrders(restaurantId: string): Promise<GetOrdersResponse> {
  const response = await api.get<GetOrdersResponse>(
    `/api/v1/restaurants/${restaurantId}/orders`
  );
  return response.data;
}

export async function updateOrderStatus(
  orderId: string,
  status: OrderStatus
): Promise<Order> {
  const response = await api.patch<Order>(`/api/v1/orders/${orderId}/status`, {
    status,
  });
  return response.data;
}
