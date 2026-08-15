import { useState } from 'react';
import { useCart } from '@/context/cart-context';
import { createCustomerOrder } from '../services/customer-order-service';

export function useCartDrawer(onClose: () => void, onOrderCreated?: () => void) {
  const { items, restaurantId, totalAmount, updateQuantity, removeFromCart, clearCart } = useCart();
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [success, setSuccess] = useState(false);

  async function handleCheckout() {
    if (!restaurantId || items.length === 0) return;

    try {
      setIsSubmitting(true);
      setError(null);

      const payload = {
        restaurant_id: restaurantId,
        items: items.map((item) => ({
          product_id: item.product.id,
          quantity: item.quantity,
        })),
      };

      await createCustomerOrder(payload);
      setSuccess(true);
      clearCart();

      setTimeout(() => {
        setSuccess(false);
        onClose();
        if (onOrderCreated) onOrderCreated();
      }, 2000);
    } catch (err: any) {
      const message = err.response?.data?.detail || 'Erro ao realizar o pedido.';
      setError(message);
    } finally {
      setIsSubmitting(false);
    }
  }

  return {
    items,
    totalAmount,
    isSubmitting,
    error,
    success,
    updateQuantity,
    removeFromCart,
    handleCheckout,
  };
}