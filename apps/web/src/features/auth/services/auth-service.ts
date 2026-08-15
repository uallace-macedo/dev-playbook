import { api } from "@/lib/api";
import type { AuthRegisterInput, AuthLoginInput, AuthLoginResponse } from "../types";

export async function registerRequest(data: AuthRegisterInput) {
  const response = await api.post('/api/v1/auth/register', data);
  return response.data;
}

export async function loginRequest(data: AuthLoginInput): Promise<AuthLoginResponse> {
  const response = await api.post<AuthLoginResponse>(
    '/api/v1/auth/login', data, {
      headers: { 'Content-Type': 'application/x-www-form-urlencoded' }
    }
  );
  return response.data;
}
