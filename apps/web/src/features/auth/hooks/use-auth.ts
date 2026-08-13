import { useState } from "react";
import { useForm } from "react-hook-form";
import { authLoginSchema, authRegisterSchema } from "../types";
import type { AuthRegisterInput, AuthLoginInput } from "../types";
import { zodResolver } from "@hookform/resolvers/zod";
import { loginRequest, registerRequest } from "../services/auth-service";
import { storage } from "@/utils/storage";
import { useNavigate } from "react-router-dom";
import { ROUTES } from "@/config/routes";

export function useAuth() {
  const navigate = useNavigate();
  const [apiError, setApiError] = useState<string | null>(null);
  const [isSuccess, setIsSuccess] = useState<boolean>(false);
  
  const loginForm = useForm({
    resolver: zodResolver(authLoginSchema),
    defaultValues: { grant_type: 'password' }
  })

  const registerForm = useForm<AuthRegisterInput>({
    resolver: zodResolver(authRegisterSchema)
  })

  async function handleLogin(data: AuthLoginInput) {

    try {
      setApiError(null);
      const response = await loginRequest(data);
      storage.setToken(response.access_token);
      
      const user = storage.getUserFromToken();
      if(user?.role == 'customer') {
        navigate(ROUTES.CUSTOMER.HOME);
      } else if (user?.role == 'restaurant_owner') {
        navigate(ROUTES.RESTAURANT.HOME);
      }
    } catch (error: any) {
      const message = error.response?.data?.detail || 'Erro ao realizar login.';
      setApiError(message);
    }
  }

  async function handleRegister(data: AuthRegisterInput) {
    try {
      setApiError(null);
      await registerRequest(data);
      setIsSuccess(true)
    } catch (error: any) {
      const message = error.response?.data?.detail || 'Erro ao criar conta.';
      setApiError(message);
    }
  }

  return {
    apiError,
    
    login: {
      register: loginForm.register,
      handleSubmit: loginForm.handleSubmit(handleLogin),
      errors: loginForm.formState.errors,
      isSubmitting: loginForm.formState.isSubmitting
    },

    signup: {
      register: registerForm.register,
      handleSubmit: registerForm.handleSubmit(handleRegister),
      errors: registerForm.formState.errors,
      isSubmitting: registerForm.formState.isSubmitting,
      isSuccess
    }
  }
}
