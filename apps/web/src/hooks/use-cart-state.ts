import { useState, useEffect } from 'react';
import type { Product } from '@/features/restaurant/types/product';
import type { CartItem } from '@/context/cart-context';
import { STORAGE_KEYS } from '@/config/constants';

const CART_STORAGE_KEY = STORAGE_KEYS.CART_STORAGE;
const CART_RESTAURANT_KEY = STORAGE_KEYS.CART_RESTAURANT;

export function useCartState() {
  const [items, setItems] = useState<CartItem[]>(() => {
    const saved = localStorage.getItem(CART_STORAGE_KEY);
    return saved ? JSON.parse(saved) : [];
  });

  const [restaurantId, setRestaurantId] = useState<string | null>(() => {
    return localStorage.getItem(CART_RESTAURANT_KEY);
  });

  const [restaurantName, setRestaurantName] = useState<string | null>(null);

  useEffect(() => {
    localStorage.setItem(CART_STORAGE_KEY, JSON.stringify(items));
    if (restaurantId) {
      localStorage.setItem(CART_RESTAURANT_KEY, restaurantId);
    } else {
      localStorage.removeItem(CART_RESTAURANT_KEY);
    }
  }, [items, restaurantId]);

  function addToCart(product: Product, newRestaurantId: string, newRestaurantName: string) {
    if (restaurantId && restaurantId !== newRestaurantId && items.length > 0) {
      const confirmChange = confirm(
        'Você já possui itens de outro restaurante no carrinho. Deseja esvaziar o carrinho atual?'
      );
      if (!confirmChange) return;
      setItems([]);
    }

    setRestaurantId(newRestaurantId);
    setRestaurantName(newRestaurantName);

    setItems((prevItems) => {
      const existingIndex = prevItems.findIndex((item) => item.product.id === product.id);

      if (existingIndex >= 0) {
        return prevItems.map((item, index) => {
          if (index === existingIndex) {
            return {
              ...item,
              quantity: item.quantity + 1,
            };
          }
          return item;
        });
      }

      return [...prevItems, { product, quantity: 1 }];
    });
  }

  function removeFromCart(productId: string) {
    setItems((prev) => {
      const updated = prev.filter((item) => item.product.id !== productId);
      if (updated.length === 0) setRestaurantId(null);
      return updated;
    });
  }

  function updateQuantity(productId: string, quantity: number) {
    if (quantity <= 0) {
      removeFromCart(productId);
      return;
    }

    setItems((prev) =>
      prev.map((item) => (item.product.id === productId ? { ...item, quantity } : item))
    );
  }

  function clearCart() {
    setItems([]);
    setRestaurantId(null);
    setRestaurantName(null);
    localStorage.removeItem(CART_STORAGE_KEY);
    localStorage.removeItem(CART_RESTAURANT_KEY);
  }

  const totalAmount = items.reduce((acc, item) => acc + item.product.price * item.quantity, 0);
  const totalItemsCount = items.reduce((acc, item) => acc + item.quantity, 0);

  return {
    items,
    restaurantId,
    restaurantName,
    totalAmount,
    totalItemsCount,
    addToCart,
    removeFromCart,
    updateQuantity,
    clearCart,
  };
}