import { useState, useEffect, useCallback } from "react";
import { tablesApi, bookingsApi } from "../api";

function TableCard({ table, onBook }) {
  const available = table.is_available && !table.is_booked_today;
  const booked = table.is_booked_today;
  const canBook = available && !booked;

  let statusLabel, statusClass;
  if (!available) {
    statusLabel = "Недоступен"; statusClass = "bg-red-100 text-red-600";
  } else if (booked) {
    statusLabel = "Занят"; statusClass = "bg-orange-100 text-orange-600";
  } else {
    statusLabel = "Свободен"; statusClass = "bg-green-100 text-green-700";
  }

  return (
    <div
      className={`bg-white rounded-2xl border-2 p-5 transition-all ${
        canBook
          ? "border-amber-200 hover:border-amber-500 hover:shadow-md cursor-pointer"
          : "border-stone-200 opacity-60 cursor-not-allowed"
      }`}
      onClick={() => canBook && onBook(table)}
    >
      <div className="flex justify-between items-start mb-3">
        <div className="text-3xl">🪑</div>
        <span className={`text-xs px-2 py-1 rounded-full font-medium ${statusClass}`}>
          {statusLabel}
        </span>
      </div>
      <h3 className="font-semibold text-stone-800 text-lg">
        Столик №{table.number}
      </h3>
      <p className="text-stone-500 text-sm">{table.name}</p>
      <div className="mt-3 flex gap-3 text-sm text-stone-500">
        <span>👥 {table.capacity} чел.</span>
        <span>📍 {table.location}</span>
      </div>
      {table.description && (
        <p className="mt-2 text-xs text-stone-400 italic">{table.description}</p>
      )}
      {canBook && (
        <button className="mt-4 w-full bg-amber-700 hover:bg-amber-600 text-white py-2 rounded-lg text-sm font-medium transition-colors">
          Забронировать
        </button>
      )}
    </div>
  );
}

function BookingModal({ table, onClose, onSuccess }) {
  const today = new Date().toISOString().split("T")[0];
  const [form, setForm] = useState({
    date: today,
    start_time: "12:00",
    guests_count: 1,
    comment: "",
  });
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);

  async function handleSubmit(e) {
    e.preventDefault();
    setError("");
    setLoading(true);
    try {
      await bookingsApi.create({ ...form, table_id: table.id });
      onSuccess();
      onClose();
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  }

  return (
    <div className="fixed inset-0 bg-black/50 flex items-center justify-center z-50 p-4">
      <div className="bg-white rounded-2xl shadow-xl w-full max-w-md">
        <div className="p-6 border-b border-stone-100">
          <h2 className="text-xl font-bold text-stone-800">
            Бронирование — Столик №{table.number}
          </h2>
          <p className="text-stone-500 text-sm mt-1">
            {table.name} · {table.location} · до {table.capacity} чел.
          </p>
        </div>
        <form onSubmit={handleSubmit} className="p-6 space-y-4">
          <label className="block">
            <span className="text-sm font-medium text-stone-700">Дата</span>
            <input
              type="date"
              required
              min={today}
              value={form.date}
              onChange={(e) => setForm({ ...form, date: e.target.value })}
              className="mt-1 block w-full border border-stone-300 rounded-lg px-3 py-2 focus:outline-none focus:ring-2 focus:ring-amber-500"
            />
          </label>
          <label className="block">
            <span className="text-sm font-medium text-stone-700">Время прихода</span>
            <input
              type="time"
              required
              value={form.start_time}
              onChange={(e) => setForm({ ...form, start_time: e.target.value })}
              className="mt-1 block w-full border border-stone-300 rounded-lg px-3 py-2 focus:outline-none focus:ring-2 focus:ring-amber-500"
            />
          </label>
          <label className="block">
            <span className="text-sm font-medium text-stone-700">
              Количество гостей (макс. {table.capacity})
            </span>
            <input
              type="number"
              required
              min={1}
              max={table.capacity}
              value={form.guests_count}
              onChange={(e) => setForm({ ...form, guests_count: parseInt(e.target.value) })}
              className="mt-1 block w-full border border-stone-300 rounded-lg px-3 py-2 focus:outline-none focus:ring-2 focus:ring-amber-500"
            />
          </label>
          <label className="block">
            <span className="text-sm font-medium text-stone-700">Комментарий</span>
            <textarea
              value={form.comment}
              onChange={(e) => setForm({ ...form, comment: e.target.value })}
              rows={2}
              placeholder="Пожелания к столику..."
              className="mt-1 block w-full border border-stone-300 rounded-lg px-3 py-2 focus:outline-none focus:ring-2 focus:ring-amber-500 resize-none"
            />
          </label>
          {error && <p className="text-red-500 text-sm">{error}</p>}
          <div className="flex gap-3 pt-2">
            <button
              type="button"
              onClick={onClose}
              className="flex-1 border border-stone-300 text-stone-700 py-2.5 rounded-lg hover:bg-stone-50 font-medium"
            >
              Отмена
            </button>
            <button
              type="submit"
              disabled={loading}
              className="flex-1 bg-amber-700 hover:bg-amber-600 text-white py-2.5 rounded-lg font-medium disabled:opacity-60 transition-colors"
            >
              {loading ? "Бронирование..." : "Забронировать"}
            </button>
          </div>
        </form>
      </div>
    </div>
  );
}

export default function Home() {
  const [tables, setTables] = useState([]);
  const [bookings, setBookings] = useState([]);
  const [selectedTable, setSelectedTable] = useState(null);
  const [error, setError] = useState("");

  const loadData = useCallback(async () => {
    try {
      const [t, b] = await Promise.all([tablesApi.list(), bookingsApi.list()]);
      setTables(t);
      setBookings(b);
    } catch (err) {
      setError(err.message);
    }
  }, []);

  useEffect(() => { loadData(); }, [loadData]);

  async function handleCancel(id) {
    try {
      await bookingsApi.cancel(id);
      loadData();
    } catch (err) {
      setError(err.message);
    }
  }

  const activeBookings = bookings.filter((b) => b.status === "confirmed");

  return (
    <div className="space-y-10">
      <section>
        <h2 className="text-2xl font-bold text-stone-800 mb-2">Столики ресторана</h2>
        <p className="text-stone-500 mb-5">Выберите столик и забронируйте удобное время</p>
        {error && <p className="text-red-500 mb-4">{error}</p>}
        {tables.length === 0 ? (
          <p className="text-stone-400 py-8 text-center">Столики пока не добавлены</p>
        ) : (
          <div className="grid sm:grid-cols-2 lg:grid-cols-3 gap-4">
            {tables.map((t) => (
              <TableCard key={t.id} table={t} onBook={setSelectedTable} />
            ))}
          </div>
        )}
      </section>

      <section>
        <h2 className="text-2xl font-bold text-stone-800 mb-5">Мои бронирования</h2>
        {activeBookings.length === 0 ? (
          <p className="text-stone-400">У вас нет активных бронирований</p>
        ) : (
          <div className="space-y-3">
            {activeBookings.map((b) => (
              <div
                key={b.id}
                className="bg-white border border-stone-200 rounded-2xl p-4 flex justify-between items-center gap-4"
              >
                <div>
                  <p className="font-semibold text-stone-800">
                    🪑 Столик №{b.table.number} — {b.table.name}
                  </p>
                  <p className="text-sm text-stone-500 mt-1">
                    📅 {b.date} · ⏰ {b.start_time.slice(0, 5)} · 👥 {b.guests_count} чел.
                  </p>
                  {b.comment && (
                    <p className="text-sm italic text-stone-400 mt-1">{b.comment}</p>
                  )}
                </div>
                <div className="flex items-center gap-3 shrink-0">
                  <span className="text-xs bg-green-100 text-green-700 px-2 py-1 rounded-full font-medium">
                    Подтверждено
                  </span>
                  <button
                    onClick={() => handleCancel(b.id)}
                    className="text-sm text-red-500 hover:text-red-700 hover:underline"
                  >
                    Отменить
                  </button>
                </div>
              </div>
            ))}
          </div>
        )}
      </section>

      {selectedTable && (
        <BookingModal
          table={selectedTable}
          onClose={() => setSelectedTable(null)}
          onSuccess={loadData}
        />
      )}
    </div>
  );
}
