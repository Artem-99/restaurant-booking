import { Routes, Route, Navigate, Link } from "react-router-dom";
import { useAuth } from "./context/AuthContext";
import Login from "./pages/Login";
import Register from "./pages/Register";
import Home from "./pages/Home";
import Admin from "./pages/Admin";

function Navbar() {
  const { user, logout } = useAuth();
  return (
    <nav className="bg-amber-800 text-white shadow-lg">
      <div className="max-w-6xl mx-auto px-4 py-3 flex items-center justify-between">
        <Link to="/" className="text-xl font-bold tracking-wide">
          🍽 ЗабГУ
        </Link>
        <div className="flex items-center gap-4">
          {user && user.is_staff && (
            <Link to="/admin" className="text-amber-200 hover:text-white text-sm">
              Панель администратора
            </Link>
          )}
          {user ? (
            <>
              <span className="text-amber-200 text-sm">{user.first_name}</span>
              <button
                onClick={logout}
                className="bg-amber-700 hover:bg-amber-600 px-3 py-1 rounded text-sm"
              >
                Выйти
              </button>
            </>
          ) : (
            <Link to="/login" className="bg-amber-700 hover:bg-amber-600 px-3 py-1 rounded text-sm">
              Войти
            </Link>
          )}
        </div>
      </div>
    </nav>
  );
}

function PrivateRoute({ children }) {
  const { user, loading } = useAuth();
  if (loading) return <div className="flex justify-center p-20 text-gray-400">Загрузка...</div>;
  return user ? children : <Navigate to="/login" replace />;
}

function AdminRoute({ children }) {
  const { user, loading } = useAuth();
  if (loading) return null;
  if (!user) return <Navigate to="/login" replace />;
  if (!user.is_staff) return <Navigate to="/" replace />;
  return children;
}

export default function App() {
  return (
    <div className="min-h-screen bg-stone-50">
      <Navbar />
      <main className="max-w-6xl mx-auto px-4 py-8">
        <Routes>
          <Route path="/login" element={<Login />} />
          <Route path="/register" element={<Register />} />
          <Route path="/" element={<PrivateRoute><Home /></PrivateRoute>} />
          <Route path="/admin" element={<AdminRoute><Admin /></AdminRoute>} />
        </Routes>
      </main>
    </div>
  );
}
