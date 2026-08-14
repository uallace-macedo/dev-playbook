import { BrowserRouter, Navigate, Route, Routes } from 'react-router-dom';
import { LoginForm } from './features/auth/components/login-form';
import { RegisterForm } from './features/auth/components/register-form';
import { ProtectedRoute } from './components/protected-route';
import { PublicRoute } from './components/public-route';
import { CustomerHome } from './features/customer/pages/customer-home';
import { RestaurantDetailsPage } from './features/customer/pages/restaurant-details';

import { ROUTES } from './config/routes';
import { RestaurantHomePage } from './features/restaurant/pages/restaurant-home-page';

export default function App() {
  return (
    <BrowserRouter>
      <div className="bg-slate-950 min-h-screen font-sans text-slate-100">
        <Routes>
          
          <Route element={<PublicRoute />}>
            <Route path={ROUTES.AUTH.LOGIN} element={
              <div className="min-h-screen flex items-center justify-center p-4">
                <LoginForm />
              </div>
            } />
            <Route path={ROUTES.AUTH.REGISTER} element={
              <div className="min-h-screen flex items-center justify-center p-4">
                <RegisterForm />
              </div>
            } />
          </Route>
          
          <Route element={<ProtectedRoute />}>
            <Route path={ROUTES.CUSTOMER.HOME} element={<CustomerHome />} />
            <Route path={ROUTES.CUSTOMER.RESTAURANT} element={<RestaurantDetailsPage />} />

            <Route path={ROUTES.RESTAURANT.HOME} element={<RestaurantHomePage />} />
          </Route>

          <Route path="*" element={<Navigate to={ROUTES.AUTH.LOGIN} replace />} />
        </Routes>
      </div>
    </BrowserRouter>
  );
}