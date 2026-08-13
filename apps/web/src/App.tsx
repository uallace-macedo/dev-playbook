import { BrowserRouter, Navigate, Route, Routes } from 'react-router-dom';
import { LoginForm } from './features/auth/components/login-form';
import { RegisterForm } from './features/auth/components/register-form';
import { ProtectedRoute } from './components/protected-route';
import { ROUTES } from './config/routes';
import { PublicRoute } from './components/public-route';


function CustomerDashboard() {
  return (
    <div className="p-8 text-white">
      <h1 className="text-2xl font-bold text-orange-500">Área do Cliente 🍕</h1>
      <p className="mt-2 text-slate-400">Em breve: Lista de pratos e criação de pedidos.</p>
    </div>
  );
}

function RestaurantDashboard() {
  return (
    <div className="p-8 text-white">
      <h1 className="text-2xl font-bold text-orange-500">Área do Restaurante 👨‍🍳</h1>
      <p className="mt-2 text-slate-400">Em breve: Gestão de pedidos recebidos.</p>
    </div>
  );
}

export default function App() {
  return (
    <BrowserRouter>
      <main className="min-h-screen bg-slate-950 flex items-center justify-center p-4 font-sans">
        <Routes>
          {/* Public Routes */}
          <Route element={<PublicRoute />}>
            <Route path={ROUTES.AUTH.LOGIN} element={<LoginForm />} />
            <Route path={ROUTES.AUTH.REGISTER} element={<RegisterForm />} />
          </Route>
          
          {/* Private Routes */}
          <Route element={<ProtectedRoute />}>
            <Route path={ROUTES.CUSTOMER.HOME} element={<CustomerDashboard />} />
            <Route path={ROUTES.RESTAURANT.HOME} element={<RestaurantDashboard />} />
          </Route>

          <Route path="*" element={<Navigate to={ROUTES.AUTH.LOGIN} replace />} />
        </Routes>
      </main>
    </BrowserRouter>
  );
}
