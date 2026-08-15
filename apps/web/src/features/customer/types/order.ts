export type CreateOrderItemPayload = {
  product_id: string;
  quantity: number;
};

export type CreateOrderPayload = {
  restaurant_id: string;
  items: CreateOrderItemPayload[];
};

export type OrderStatus = 'created' | 'accepted' | 'rejected' | 'delivered' | 'canceled';

export interface OrderItem {
  id: string;
  product_id: string;
  product_name: string;
  quantity: number;
  unit_price: number;
  subtotal: number;
}

export interface CustomerOrder {
  id: string;
  status: OrderStatus;
  total_price: number;
  created_at: string;
  updated_at: string;
  reviewed: boolean;
  customer: {
    id: string;
    name: string;
  };
  restaurant: {
    id: string;
    name: string;
  };
  items: OrderItem[];
}
