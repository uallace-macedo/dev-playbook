import { api } from '@/lib/api';
import type { CreateOrderPayload } from '../types/order';

export async function createCustomerOrder(payload: CreateOrderPayload) {
  const response = await api.post(`/api/v1/restaurants/${payload.restaurant_id}/orders`, payload);
  return response.data;
}
