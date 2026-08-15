export const ROUTES = {
  AUTH: {
    LOGIN: '/login',
    REGISTER: '/register',
  },
  CUSTOMER: {
    HOME: '/',
    RESTAURANT: '/customer/restaurant/:id',
    ORDERS: '/customer/orders',
  },
  RESTAURANT: {
    HOME: '/restaurant',
    PRODUCTS: '/restaurant/:restaurantId/products',
    ORDERS: '/restaurant/:restaurantId/orders',
  },
} as const;