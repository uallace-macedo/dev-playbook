export type CreateOrderItemPayload = {
  product_id: string;
  quantity: number;
};

export type CreateOrderPayload = {
  restaurant_id: string;
  items: CreateOrderItemPayload[];
};

export type OrderStatus = 'created' | 'accepted' | 'rejected' | 'delivered';

export type CustomerOrder = {
  id: string;
  restaurant_id: string;
  restaurant_name?: string;
  status: OrderStatus;
  created_at?: string;
  total_price?: number;
};
