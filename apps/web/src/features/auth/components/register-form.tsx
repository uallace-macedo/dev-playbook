import { Link } from 'react-router-dom';
import { useAuth } from '../hooks/use-auth';
import { ROUTES } from '@/config/routes';

export function RegisterForm() {
  const { signup, apiError } = useAuth();

  if (signup.isSuccess) {
    return (
      <div className="w-full max-w-md mx-auto p-6 bg-slate-900 border border-slate-800 rounded-2xl shadow-xl text-center text-slate-100">
        <h3 className="text-xl font-bold text-green-400 mb-2">Conta criada com sucesso! 🎉</h3>
        <p className="text-sm text-slate-400 mb-4">Agora você pode fazer login na sua conta.</p>
      </div>
    );
  }

  return (
    <div className="w-full max-w-md mx-auto p-6 bg-slate-900 border border-slate-800 rounded-2xl shadow-xl text-slate-100">
      <div className="mb-6 text-center">
        <h2 className="text-2xl font-bold tracking-tight text-white">Criar uma conta 🚀</h2>
        <p className="text-sm text-slate-400 mt-1">Preencha os dados abaixo para se cadastrar</p>
      </div>

      {apiError && (
        <div className="mb-4 p-3 rounded-lg bg-red-500/10 border border-red-500/30 text-red-400 text-sm">
          {apiError}
        </div>
      )}

      <form onSubmit={signup.handleSubmit} className="space-y-4">
        <div>
          <label className="block text-xs font-medium text-slate-300 uppercase tracking-wider mb-1">Nome</label>
          <input
            type="text"
            placeholder="Seu nome completo"
            {...signup.register('name')}
            className="w-full px-4 py-2.5 rounded-lg bg-slate-950 border border-slate-800 text-white placeholder-slate-500 focus:outline-none focus:border-orange-500 transition text-sm"
          />
          {signup.errors.name && <p className="mt-1 text-xs text-red-400">{signup.errors.name.message}</p>}
        </div>

        <div>
          <label className="block text-xs font-medium text-slate-300 uppercase tracking-wider mb-1">E-mail</label>
          <input
            type="email"
            placeholder="seu@email.com"
            {...signup.register('email')}
            className="w-full px-4 py-2.5 rounded-lg bg-slate-950 border border-slate-800 text-white placeholder-slate-500 focus:outline-none focus:border-orange-500 transition text-sm"
          />
          {signup.errors.email && <p className="mt-1 text-xs text-red-400">{signup.errors.email.message}</p>}
        </div>

        <div>
          <label className="block text-xs font-medium text-slate-300 uppercase tracking-wider mb-1">Tipo de Conta</label>
          <select
            {...signup.register('role')}
            className="w-full px-4 py-2.5 rounded-lg bg-slate-950 border border-slate-800 text-white focus:outline-none focus:border-orange-500 transition text-sm"
          >
            <option value="customer">Cliente</option>
            <option value="restaurant_owner">Dono de Restaurante</option>
          </select>
          {signup.errors.role && <p className="mt-1 text-xs text-red-400">{signup.errors.role.message}</p>}
        </div>

        <div>
          <label className="block text-xs font-medium text-slate-300 uppercase tracking-wider mb-1">Senha</label>
          <input
            type="password"
            placeholder="••••••••"
            {...signup.register('password')}
            className="w-full px-4 py-2.5 rounded-lg bg-slate-950 border border-slate-800 text-white placeholder-slate-500 focus:outline-none focus:border-orange-500 transition text-sm"
          />
          {signup.errors.password && <p className="mt-1 text-xs text-red-400">{signup.errors.password.message}</p>}
        </div>

        <button
          type="submit"
          disabled={signup.isSubmitting}
          className="w-full mt-2 py-3 px-4 bg-orange-600 hover:bg-orange-500 disabled:opacity-50 text-white font-medium rounded-lg transition text-sm cursor-pointer"
        >
          {signup.isSubmitting ? 'Cadastrando...' : 'Criar Conta'}
        </button>
      </form>
      <div className="mt-4 text-center">
        <p className="text-sm text-slate-400">
          Já possui uma conta?{' '}
          <Link
            to={ROUTES.AUTH.LOGIN}
            className="text-orange-500 hover:text-orange-400 font-medium transition underline"
          >
            Faça login
          </Link>
        </p>
      </div>
    </div>
  );
}