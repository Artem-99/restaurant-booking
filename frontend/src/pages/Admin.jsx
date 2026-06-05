import { useState, useEffect, useCallback } from "react";
import { tablesApi, bookingsApi, authApi } from "../api";

const TABS = [
  { key: "bookings", label: "Все бронирования" },
  { key: "tables", label: "Столики" },
  { key: "users", label: "Пользователи" },
];

export default function Admin() {
  const [tab, setTab] = useState("bookings");
  const [bookings, setBookings] = useState([]);
  const [tables, setTables] = useState([]);
  const [users, setUsers] = useState([]);
  const [error, setError] = useState("");
  const [newTable, setNewTable] = useState({
    number: "",
    name: "",
    capacity: "",
    location: "Основной зал",
    description: "",
  });

  const loadAll = useCallback(async () => {
    try {
      const [b, t, u] = await Promise.all([
        bookingsApi.list(),
        tablesApi.list(),
        authApi.listUsers(),
      ]);
      setBookings(b);
      setTables(t);
      setUsers(u);
    } catch (err) {
      setError(err.message);
    }
  }, []);

  useEffect(() => { loadAll(); }, [loadAll]);

  async function cancelBooking(id) {
    try { await bookingsApi.cancel(id); loadAll(); }
    catch (err) { setError(err.message); }
  }

  async function deleteTable(id) {
    try { await tablesApi.remove(id); loadAll(); }
    catch (err) { setError(err.message); }
  }

  async function toggleTable(t) {
    try { await tablesApi.update(t.id, { is_available: !t.is_available }); loadAll(); }
    catch (err) { setError(err.message); }
  }

  async function toggleUserRole(user) {
    try { await authApi.toggleRole(user.id); loadAll(); }
    catch (err) { setError(err.message); }
  }

  async function addTable(e) {
    e.preventDefault();
    setError("");
    try {
      await tablesApi.create({
        ...newTable,
        number: Number(newTable.number),
        capacity: Number(newTable.capacity),
      });
      setNewTable({ number: "", name: "", capacity: "", location: "Основной зал", description: "" });
      loadAll();
    } catch (err) {
      setError(err.message);
    }
  }

  return (
    <div className="space-y-6">
      <h1 className="text-2xl font-bold text-stone-800">Панель администратора</h1>
      {error && (
        <div className="bg-red-50 border border-red-200 text-red-600 rounded-lg px-4 py-3 text-sm">
          {error}
        </div>
      )}

      <div className="flex gap-1 border-b border-stone-200">
        {TABS.map((t) => (
          <button
            key={t.key}
            onClick={() => setTab(t.key)}
            className={`px-5 py-2.5 text-sm font-medium border-b-2 transition-colors ${
              tab === t.key
                ? "border-amber-700 text-amber-700"
                : "border-transparent text-stone-500 hover:text-stone-700"
            }`}
          >
            {t.label}
          </button>
        ))}
      </div>

      {tab === "bookings" && (
        <div className="space-y-3">
          {bookings.length === 0 && (
            <p className="text-stone-400">Бронирований нет</p>
          )}
          {bookings.map((b) => (
            <div
              key={b.id}
              className="bg-white border border-stone-200 rounded-2xl p-4 flex justify-between items-center gap-4"
            >
              <div>
                <p className="font-semibold text-stone-800">
                  🪑 Столик №{b.table.number} — {b.table.name}
                </p>
                <p className="text-sm text-stone-500 mt-1">
                  👤 {b.user.first_name} ({b.user.email}) · 📅 {b.date} · ⏰ {b.start_time.slice(0, 5)} – {b.end_time.slice(0, 5)} · 👥 {b.guests_count} чел.
                </p>
                {b.comment && <p className="text-xs italic text-stone-400">{b.comment}</p>}
              </div>
              <div className="flex items-center gap-3 shrink-0">
                <span
                  className={`text-xs px-2 py-1 rounded-full font-medium ${
                    b.status === "confirmed"
                      ? "bg-green-100 text-green-700"
                      : "bg-stone-100 text-stone-500"
                  }`}
                >
                  {b.status === "confirmed" ? "Активно" : "Отменено"}
                </span>
                {b.status === "confirmed" && (
                  <button
                    onClick={() => cancelBooking(b.id)}
                    className="text-sm text-red-500 hover:text-red-700 hover:underline"
                  >
                    Отменить
                  </button>
                )}
              </div>
            </div>
          ))}
        </div>
      )}

      {tab === "tables" && (
        <div className="space-y-6">
          <form
            onSubmit={addTable}
            className="bg-white border border-stone-200 rounded-2xl p-5 space-y-3"
          >
            <h3 className="font-semibold text-stone-700">Добавить столик</h3>
            <div className="grid sm:grid-cols-3 gap-3">
              <input
                placeholder="Номер"
                type="number"
                required
                value={newTable.number}
                onChange={(e) => setNewTable({ ...newTable, number: e.target.value })}
                className="border border-stone-300 rounded-lg px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-amber-500"
              />
              <input
                placeholder="Название (напр. «У окна»)"
                required
                value={newTable.name}
                onChange={(e) => setNewTable({ ...newTable, name: e.target.value })}
                className="border border-stone-300 rounded-lg px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-amber-500"
              />
              <input
                placeholder="Вместимость"
                type="number"
                required
                value={newTable.capacity}
                onChange={(e) => setNewTable({ ...newTable, capacity: e.target.value })}
                className="border border-stone-300 rounded-lg px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-amber-500"
              />
              <input
                placeholder="Расположение"
                value={newTable.location}
                onChange={(e) => setNewTable({ ...newTable, location: e.target.value })}
                className="border border-stone-300 rounded-lg px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-amber-500"
              />
              <input
                placeholder="Описание"
                value={newTable.description}
                onChange={(e) => setNewTable({ ...newTable, description: e.target.value })}
                className="sm:col-span-2 border border-stone-300 rounded-lg px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-amber-500"
              />
            </div>
            <button
              type="submit"
              className="bg-amber-700 hover:bg-amber-600 text-white py-2 px-5 rounded-lg text-sm font-medium transition-colors"
            >
              Добавить столик
            </button>
          </form>

          <div className="space-y-3">
            {tables.map((t) => (
              <div
                key={t.id}
                className="bg-white border border-stone-200 rounded-2xl p-4 flex justify-between items-center"
              >
                <div>
                  <p className="font-semibold text-stone-800">
                    №{t.number} — {t.name}
                  </p>
                  <p className="text-sm text-stone-500">
                    👥 {t.capacity} чел. · 📍 {t.location}
                    {t.description && ` · ${t.description}`}
                  </p>
                </div>
                <div className="flex gap-3 shrink-0">
                  <button
                    onClick={() => toggleTable(t)}
                    className={`text-sm px-3 py-1 rounded-lg border transition-colors ${
                      t.is_available
                        ? "text-orange-600 border-orange-300 hover:bg-orange-50"
                        : "text-green-600 border-green-300 hover:bg-green-50"
                    }`}
                  >
                    {t.is_available ? "Отключить" : "Включить"}
                  </button>
                  <button
                    onClick={() => deleteTable(t.id)}
                    className="text-sm text-red-500 hover:text-red-700 hover:underline"
                  >
                    Удалить
                  </button>
                </div>
              </div>
            ))}
          </div>
        </div>
      )}

      {tab === "users" && (
        <div className="space-y-3">
          {users.map((u) => (
            <div
              key={u.id}
              className="bg-white border border-stone-200 rounded-2xl p-4 flex justify-between items-center"
            >
              <div>
                <p className="font-semibold text-stone-800">{u.first_name}</p>
                <p className="text-sm text-stone-500">{u.email}</p>
              </div>
              <div className="flex items-center gap-3 shrink-0">
                <span
                  className={`text-xs px-2 py-1 rounded-full font-medium ${
                    u.is_staff
                      ? "bg-amber-100 text-amber-700"
                      : "bg-stone-100 text-stone-600"
                  }`}
                >
                  {u.is_staff ? "Администратор" : "Пользователь"}
                </span>
                <button
                  onClick={() => toggleUserRole(u)}
                  className="text-sm text-amber-700 hover:underline"
                >
                  {u.is_staff ? "Снять права" : "Сделать админом"}
                </button>
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}
