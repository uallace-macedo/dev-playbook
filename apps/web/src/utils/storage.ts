import { STORAGE_KEYS } from "@/config/constants";
import type { JWTPayload } from "@/features/auth/types";
import { jwtDecode } from "jwt-decode";

export const storage = {
  getToken: () => localStorage.getItem(STORAGE_KEYS.TOKEN),
  setToken: (token: string) => localStorage.setItem(STORAGE_KEYS.TOKEN, token),
  removeToken: () => localStorage.removeItem(STORAGE_KEYS.TOKEN),

  getUserFromToken: (): JWTPayload | null => {
    const token = localStorage.getItem(STORAGE_KEYS.TOKEN);
    if(!token) return null;

    try {
      return jwtDecode<JWTPayload>(token);
    } catch (error) {
      return null;
    }
  },

  clearSession: () => {
    localStorage.removeItem(STORAGE_KEYS.TOKEN);
  },
}
