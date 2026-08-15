export type OrderStatus = 'created' | 'accepted' | 'rejected' | 'delivered';

export type OrderItem = {
  id: string;
  product_id: string;
  product_name: string;
  quantity: number;
  unit_price: number;
  subtotal: number;
};

export type Order = {
  id: string;
  status: OrderStatus;
  total_price: number;
  created_at: string;
  customer: { id: string; name: string };
  items: OrderItem[];
};

export type Restaurant = {
  id: string;
  name: string;
  description: string;
  rating_average?: number;
  total_reviews?: number;
};

export type GetRestaurantsResponse = {
  restaurants: Restaurant[];
};