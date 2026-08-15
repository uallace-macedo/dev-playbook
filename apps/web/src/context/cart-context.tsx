import { createContext, useContext, type ReactNode } from 'react';
import type { Product } from '@/features/restaurant/types/product';
import { useCartState } from '@/hooks/use-cart-state';

export type CartItem = {
  product: Product;
  quantity: number;
};

type CartContextData = {
  items: CartItem[];
  restaurantId: string | null;
  restaurantName: string | null;
  totalAmount: number;
  totalItemsCount: number;
  addToCart: (product: Product, restaurantId: string, restaurantName: string) => void;
  removeFromCart: (productId: string) => void;
  updateQuantity: (productId: string, quantity: number) => void;
  clearCart: () => void;
};

const CartContext = createContext<CartContextData>({} as CartContextData);

export function CartProvider({ children }: { children: ReactNode }) {
  const cartState = useCartState();

  return (
    <CartContext.Provider value={cartState}>
      {children}
    </CartContext.Provider>
  );
}

export function useCart() {
  return useContext(CartContext);
}