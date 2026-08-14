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

export type Product = {
  id: string;
  name: string;
  price: number;
};

export type GetProductsParams = {
  limit?: number;
  offset?: number;
  name?: string;
};

export type GetProductsResponse = {
  products: Product[];
};