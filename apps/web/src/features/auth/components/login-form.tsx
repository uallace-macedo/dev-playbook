import { Link } from "react-router-dom";
import { ROUTES } from "@/config/routes";
import { useAuth } from "../hooks/use-auth";

export function LoginForm() {
  const { login, apiError } = useAuth();

  return (
    <div className="w-full max-w-md mx-auto p-6 bg-slate-900 border border-slate-800 rounded-2xl shadow-xl text-slate-100">
      <div className="mb-6 text-center">
        <h2 className="text-2xl font-bold tracking-tight text-white">
          Bem-vindo de volta! 👋
        </h2>
        <p className="text-sm text-slate-400 mt-1">
          Acesse sua conta para continuar no VFDelivery
        </p>
      </div>

      {apiError && (
        <div className="mb-4 p-3 rounded-lg bg-red-500/10 border border-red-500/30 text-red-400 text-sm">
          {apiError}
        </div>
      )}

      <form onSubmit={login.handleSubmit} className="space-y-4">
        <div>
          <label className="block text-xs font-medium text-slate-300 uppercase tracking-wider mb-1">
            E-mail
          </label>
          <input
            type="email"
            placeholder="seu@email.com"
            {...login.register('username')}
            className="w-full px-4 py-2.5 rounded-lg bg-slate-950 border border-slate-800 text-white placeholder-slate-500 focus:outline-none focus:border-orange-500 focus:ring-1 focus:ring-orange-500 transition text-sm"
          />
          {login.errors.username && (
            <p className="mt-1 text-xs text-red-400">
              {login.errors.username.message as string}
            </p>
          )}
        </div>

        <div>
          <label className="block text-xs font-medium text-slate-300 uppercase tracking-wider mb-1">
            Senha
          </label>
          <input
            type="password"
            placeholder="••••••••"
            {...login.register('password')}
            className="w-full px-4 py-2.5 rounded-lg bg-slate-950 border border-slate-800 text-white placeholder-slate-500 focus:outline-none focus:border-orange-500 focus:ring-1 focus:ring-orange-500 transition text-sm"
          />
          {login.errors.password && (
            <p className="mt-1 text-xs text-red-400">
              {login.errors.password.message as string}
            </p>
          )}
        </div>

        <button
          type="submit"
          disabled={login.isSubmitting}
          className="w-full mt-2 py-3 px-4 bg-orange-600 hover:bg-orange-500 disabled:opacity-50 disabled:cursor-not-allowed text-white font-medium rounded-lg shadow-lg shadow-orange-600/20 transition cursor-pointer text-sm"
        >
          {login.isSubmitting ? 'Entrando...' : 'Entrar'}
        </button>
      </form>
      <div className="mt-4 text-center">
        <p className="text-sm text-slate-400">
          Não tem uma conta?{' '}
          <Link
            to={ROUTES.AUTH.REGISTER}
            className="text-orange-500 hover:text-orange-400 font-medium transition underline"
          >
            Cadastre-se
          </Link>
        </p>
      </div>
    </div>
  )

}