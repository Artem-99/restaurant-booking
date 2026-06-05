import { useState } from "react";
import { Link, useNavigate } from "react-router-dom";
import { authApi } from "../api";

export default function Register() {
  const navigate = useNavigate();
  const [form, setForm] = useState({ email: "", first_name: "", password: "" });
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);

  async function handleSubmit(e) {
    e.preventDefault();
    setError("");
    setLoading(true);
    try {
      await authApi.register(form);
      navigate("/login");
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  }

  return (
    <div className="max-w-sm mx-auto mt-16">
      <div className="bg-white rounded-2xl shadow-md border border-stone-200 p-8">
        <div className="text-center mb-6">
          <div className="text-4xl mb-2">🍽</div>
          <h1 className="text-2xl font-bold text-stone-800">Регистрация</h1>
          <p className="text-stone-500 text-sm mt-1">Создайте аккаунт для бронирования</p>
        </div>
        <form onSubmit={handleSubmit} className="space-y-4">
          <label className="block">
            <span className="text-sm font-medium text-stone-700">Имя</span>
            <input
              type="text"
              required
              value={form.first_name}
              onChange={(e) => setForm({ ...form, first_name: e.target.value })}
              className="mt-1 block w-full border border-stone-300 rounded-lg px-3 py-2 focus:outline-none focus:ring-2 focus:ring-amber-500"
            />
          </label>
          <label className="block">
            <span className="text-sm font-medium text-stone-700">Email</span>
            <input
              type="email"
              required
              value={form.email}
              onChange={(e) => setForm({ ...form, email: e.target.value })}
              className="mt-1 block w-full border border-stone-300 rounded-lg px-3 py-2 focus:outline-none focus:ring-2 focus:ring-amber-500"
            />
          </label>
          <label className="block">
            <span className="text-sm font-medium text-stone-700">Пароль</span>
            <input
              type="password"
              required
              value={form.password}
              onChange={(e) => setForm({ ...form, password: e.target.value })}
              className="mt-1 block w-full border border-stone-300 rounded-lg px-3 py-2 focus:outline-none focus:ring-2 focus:ring-amber-500"
            />
          </label>
          {error && <p className="text-red-500 text-sm">{error}</p>}
          <button
            type="submit"
            disabled={loading}
            className="w-full bg-amber-700 hover:bg-amber-600 text-white py-2.5 rounded-lg font-medium disabled:opacity-60 transition-colors"
          >
            {loading ? "Создание аккаунта..." : "Зарегистрироваться"}
          </button>
        </form>
        <p className="mt-4 text-sm text-center text-stone-500">
          Уже есть аккаунт?{" "}
          <Link to="/login" className="text-amber-700 hover:underline font-medium">
            Войти
          </Link>
        </p>
      </div>
    </div>
  );
}
