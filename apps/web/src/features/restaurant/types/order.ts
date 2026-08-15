export type OrderStatus = 'created' | 'accepted' | 'rejected' | 'delivered';

export type OrderItem = {
  id: string;
  product_id: string;
  product_name?: string;
  quantity: number;
  unit_price?: number;
};

export type Order = {
  id: string;
  customer: OrderCustomer;
  status: OrderStatus;
  created_at?: string;
  items: OrderItem[];
  total_price?: number;
};

export type GetOrdersResponse = {
  orders: Order[];
};

export type UpdateOrderStatusDTO = {
  status: OrderStatus;
};

export type OrderCustomer = {
  id: string;
  name: string;
}