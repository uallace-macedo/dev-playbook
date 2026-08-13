import { api } from "@/lib/api";
import type { GetRestaurantsParams, GetRestaurantsResponse } from "../types";

export async function getRestaurants(params?: GetRestaurantsParams): Promise<GetRestaurantsResponse> {
  const response = await api.get<GetRestaurantsResponse>('/api/v1/restaurants', { params });
  return response.data;
}
