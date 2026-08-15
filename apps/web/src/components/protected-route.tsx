import { storage } from "@/utils/storage";
import { Navigate, Outlet } from "react-router-dom";

export function ProtectedRoute() {
  const token = storage.getToken();

  if(!token) {
    return <Navigate to='/login' replace />
  }

  return <Outlet />
}
