export type Product = {
  id: string;
  name: string;
  price: number;
  restaurant_id: string;
};

export type GetProductsParams = {
  name?: string;
  limit?: number;
  offset?: number;
};

export type GetProductsResponse = {
  products: Product[];
};

export type CreateProductDTO = {
  name: string;
  price: number;
};

export type UpdateProductDTO = Partial<CreateProductDTO>;
