import { api } from '@/lib/api';
import type { Restaurant, Order, OrderStatus, GetRestaurantsResponse } from '../types';

export async function getMyRestaurants(): Promise<GetRestaurantsResponse> {
  const response = await api.get<GetRestaurantsResponse>('/api/v1/restaurants');
  return response.data;
}

export async function createRestaurant(data: { name: string; description: string }): Promise<Restaurant> {
  const response = await api.post<Restaurant>('/api/v1/restaurants', data);
  return response.data;
}

export async function createProduct(restaurantId: string, data: { name: string; price: number }) {
  return await api.post(`/api/v1/restaurants/${restaurantId}/products`, data);
}

export async function getRestaurantOrders(restaurantId: string) {
  const response = await api.get<{ orders: Order[] }>(`/api/v1/restaurants/${restaurantId}/orders`);
  return response.data;
}

export async function updateOrderStatus(orderId: string, status: OrderStatus) {
  return await api.patch(`/api/v1/orders/${orderId}/status`, { status });
}
