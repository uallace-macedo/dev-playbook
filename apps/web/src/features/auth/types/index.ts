import { z } from 'zod';

export const userRoleSchema = z.enum(['customer', 'restaurant_owner']);
export type UserRole = z.infer<typeof userRoleSchema>;

export const authRegisterSchema = z.object({
  name: z.string().min(1, 'O nome é obrigatório'),
  email: z.email('Digite um e-mail válido'),
  role: userRoleSchema,
  password: z.string().min(6, 'A senha deve conter no mínimo 6 caracteres'),
});

export type AuthRegisterInput = z.infer<typeof authRegisterSchema>;

export const authLoginSchema = z.object({
  username: z.string().min(1, 'Informe seu e-mail'),
  password: z.string().min(1, 'Informe sua senha'),
  grant_type: z.literal('password').default('password'),
  scope: z.string().default('').optional(),
  client_id: z.string().default(''),
  client_secret: z.string().default(''),
});
export type AuthLoginInput = z.infer<typeof authLoginSchema>;

export type AuthLoginResponse = {
  access_token: string;
  token_type: string;
};

export type JWTPayload = {
  sub: string;
  role: UserRole;
}
