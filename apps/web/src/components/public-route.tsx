import { Navigate, Outlet } from 'react-router-dom';
import { storage } from '@/utils/storage';
import { ROUTES } from '@/config/routes';

export function PublicRoute() {
  const user = storage.getUserFromToken();

  if (user) {
    if (user.role === 'customer') {
      return <Navigate to={ROUTES.CUSTOMER.HOME} replace />;
    }

    if (user.role === 'restaurant_owner') {
      return <Navigate to={ROUTES.RESTAURANT.HOME} replace />;
    }

    return <Navigate to={ROUTES.CUSTOMER.HOME} replace />;
  }

  return <Outlet />;
}