import { api } from '@/lib/api';
import type { Product, GetProductsResponse, GetProductsParams, CreateProductDTO, UpdateProductDTO } from '../types/product';

export async function getRestaurantProducts(
  restaurantId: string,
  params?: GetProductsParams
): Promise<GetProductsResponse> {
  const response = await api.get<GetProductsResponse>(
    `/api/v1/restaurants/${restaurantId}/products`,
    { params }
  );
  return response.data;
}

export async function createProduct(
  restaurantId: string,
  data: CreateProductDTO
): Promise<Product> {
  const response = await api.post<Product>(
    `/api/v1/restaurants/${restaurantId}/products`,
    data
  );
  return response.data;
}

export async function updateProduct(
  restaurantId: string,
  productId: string,
  data: UpdateProductDTO
): Promise<Product> {
  const response = await api.patch<Product>(
    `/api/v1/restaurants/${restaurantId}/products/${productId}`,
    data,
    { params: { restaurant_id: restaurantId }}
  );
  return response.data;
}

export async function deleteProduct(
  restaurantId: string,
  productId: string,
): Promise<void> {
  await api.delete(`/api/v1/restaurants/${restaurantId}/products/${productId}`);
}