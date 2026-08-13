export type Restaurant = {
  id: string;
  name: string;
  description: string;
  rating_average: number;
  total_reviews: number;
}

export type GetRestaurantsResponse = {
  restaurants: Restaurant[];
}

export type GetRestaurantsParams = {
  limit?: number;
  offset?: number;
  name?: string;
}
