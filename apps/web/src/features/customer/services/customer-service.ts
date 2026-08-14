import { api } from "@/lib/api";
import type { Restaurant, GetRestaurantsParams, GetRestaurantsResponse, GetProductsParams, GetProductsResponse } from "../types";

export async function getRestaurants(params?: GetRestaurantsParams): Promise<GetRestaurantsResponse> {
  const response = await api.get<GetRestaurantsResponse>('/api/v1/restaurants', { params });
  return response.data;
}

export async function getRestaurantByIdRequest(restaurantId: string): Promise<Restaurant> {
  const response = await api.get<Restaurant>(`/api/v1/restaurants/${restaurantId}`);
  return response.data;
}

export async function getRestaurantProductsRequest(
  restaurantId: string,
  params?: GetProductsParams
): Promise<GetProductsResponse> {
  const response = await api.get<GetProductsResponse>(
    `/api/v1/restaurants/${restaurantId}/products`,
    { params }
  );
  return response.data;
}
